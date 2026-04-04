from fastapi import WebSocket, WebSocketDisconnect
from signaling import active_users
import httpx
import os
import base64
import asyncio
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

translation_users = {}
user_languages = {}

# ✅ buffer for mobile audio
mobile_audio_buffers = {}

SAMPLE_RATE = 16000
CHUNK_DURATION = 2
BUFFER_SIZE = SAMPLE_RATE * CHUNK_DURATION * 2

LANG_CODE_MAP = {
    "English": "en", "Hindi": "hi", "Telugu": "te",
    "Tamil": "ta", "Spanish": "es", "French": "fr",
    "German": "de", "Chinese": "zh", "Japanese": "ja",
    "Portuguese": "pt", "Arabic": "ar", "Russian": "ru", "Korean": "ko"
}

async def safe_send_translation(ws, data):
    try:
        await ws.send_json(data)
    except:
        pass

async def translate_text(text, target_lang):
    try:
        async with httpx.AsyncClient(timeout=10) as client:
            response = await client.post(
                "https://api.groq.com/openai/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {GROQ_API_KEY}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": "llama-3.1-8b-instant",
                    "messages": [
                        {
                            "role": "system",
                            "content": f"You are a translator. Translate to {target_lang}. Return ONLY translated text."
                        },
                        {"role": "user", "content": text}
                    ],
                    "temperature": 0,
                    "max_tokens": 500
                }
            )
            response.raise_for_status()
            return response.json()["choices"][0]["message"]["content"].strip()
    except Exception as e:
        print(f"Translation error: {e}")
        return text

async def transcribe_audio(audio_buffer, source_lang=None):
    try:
        import struct, io, numpy as np

        # silence check
        audio_np = np.frombuffer(audio_buffer, np.int16).astype(np.float32) / 32768.0
        if np.abs(audio_np).mean() < 0.002:
            return ""

        # build WAV
        wav_buffer = io.BytesIO()
        wav_buffer.write(b'RIFF')
        wav_buffer.write(struct.pack('<I', 36 + len(audio_buffer)))
        wav_buffer.write(b'WAVE')
        wav_buffer.write(b'fmt ')
        wav_buffer.write(struct.pack('<I', 16))
        wav_buffer.write(struct.pack('<H', 1))
        wav_buffer.write(struct.pack('<H', 1))
        wav_buffer.write(struct.pack('<I', 16000))
        wav_buffer.write(struct.pack('<I', 32000))
        wav_buffer.write(struct.pack('<H', 2))
        wav_buffer.write(struct.pack('<H', 16))
        wav_buffer.write(b'data')
        wav_buffer.write(struct.pack('<I', len(audio_buffer)))
        wav_buffer.write(audio_buffer)
        wav_buffer.seek(0)
        wav_bytes = wav_buffer.read()

        files = {
            "file": ("audio.wav", wav_bytes, "audio/wav"),
            "model": (None, "whisper-large-v3-turbo"),
            "response_format": (None, "text")
        }
        if source_lang and source_lang in LANG_CODE_MAP:
            files["language"] = (None, LANG_CODE_MAP[source_lang])

        async with httpx.AsyncClient(timeout=15) as client:
            response = await client.post(
                "https://api.groq.com/openai/v1/audio/transcriptions",
                headers={"Authorization": f"Bearer {GROQ_API_KEY}"},
                files=files
            )
            response.raise_for_status()
            return response.text.strip()
    except Exception as e:
        print(f"Transcription error: {e}")
        return ""

async def send_translation(text, user_id, connected_user, translate_to, websocket):
    if not text:
        return
    if connected_user in translation_users:
        await safe_send_translation(
            translation_users[connected_user], {
                "type": "translated_text",
                "from_id": user_id,
                "text": text,
                "target_language": translate_to
            }
        )
    await safe_send_translation(websocket, {
        "type": "translation_sent",
        "text": text
    })

async def translation_socket(websocket: WebSocket, user_id: str):
    await websocket.accept()
    translation_users[user_id] = websocket
    mobile_audio_buffers[user_id] = b""

    my_language = "English"

    try:
        while True:
            data = await websocket.receive_json()
            msg_type = data.get("type")

            if msg_type == "set_languages":
                my_language = data.get("caller_language", "English")
                user_languages[user_id] = {"my_language": my_language}
                print(f"🌐 {user_id}: speaks={my_language}")
                await safe_send_translation(websocket, {"type": "languages_set"})

            # ✅ DESKTOP: text from Speech Recognition
            elif msg_type == "text_chunk":
                text = data.get("text", "").strip()
                if not text:
                    continue

                print(f"📝 {user_id} said: {text}")

                connected_user = active_users.get(user_id, {}).get("connected_to")
                if not connected_user:
                    continue

                translate_to = user_languages.get(connected_user, {}).get("my_language", "English")
                print(f"🔄 Translating to: {translate_to}")

                if my_language == translate_to:
                    translated = text
                else:
                    translated = await translate_text(text, translate_to)

                print(f"✅ Translated: {translated}")
                await send_translation(translated, user_id, connected_user, translate_to, websocket)

            # ✅ MOBILE: raw audio chunks → Whisper
            elif msg_type == "audio_chunk":
                audio_chunk = base64.b64decode(data.get("audio", ""))
                mobile_audio_buffers[user_id] += audio_chunk

                if len(mobile_audio_buffers[user_id]) >= BUFFER_SIZE:
                    buf = mobile_audio_buffers[user_id]
                    mobile_audio_buffers[user_id] = b""

                    connected_user = active_users.get(user_id, {}).get("connected_to")
                    if not connected_user:
                        continue

                    translate_to = user_languages.get(connected_user, {}).get("my_language", "English")

                    # process in background
                    asyncio.create_task(
                        process_mobile_audio(buf, user_id, connected_user, translate_to, my_language, websocket)
                    )

    except WebSocketDisconnect:
        print(f"Translation socket closed {user_id}")
    finally:
        translation_users.pop(user_id, None)
        user_languages.pop(user_id, None)
        mobile_audio_buffers.pop(user_id, None)

async def process_mobile_audio(buf, user_id, connected_user, translate_to, source_lang, websocket):
    try:
        transcript = await transcribe_audio(buf, source_lang)
        if not transcript or len(transcript.strip()) <= 1:
            return

        skip = ["there is no text to translate", "no text", "thank you"]
        if any(s in transcript.lower() for s in skip):
            return

        print(f"📱 Mobile transcribed: {transcript}")

        if source_lang == translate_to:
            translated = transcript
        else:
            translated = await translate_text(transcript, translate_to)

        print(f"✅ Mobile translated: {translated}")
        await send_translation(translated, user_id, connected_user, translate_to, websocket)
    except Exception as e:
        print(f"Mobile audio processing error: {e}")