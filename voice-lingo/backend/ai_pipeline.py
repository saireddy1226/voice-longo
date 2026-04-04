import os
import logging
import httpx
import numpy as np
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

SAMPLE_RATE = 16000
CHUNK_DURATION = 2
BUFFER_SIZE = SAMPLE_RATE * CHUNK_DURATION * 2

# ✅ language name to Whisper language code
LANG_CODE_MAP = {
    "English": "en",
    "Hindi": "hi",
    "Telugu": "te",
    "Tamil": "ta",
    "Spanish": "es",
    "French": "fr",
    "German": "de",
    "Chinese": "zh",
    "Japanese": "ja",
    "Portuguese": "pt",
    "Arabic": "ar",
    "Russian": "ru",
    "Korean": "ko"
}

async def process_stream(audio_buffer, target_lang, source_lang=None):
    try:
        if not audio_buffer or len(audio_buffer) < BUFFER_SIZE:
            return ""

        audio_np = np.frombuffer(audio_buffer, np.int16).astype(np.float32) / 32768.0
        volume = np.abs(audio_np).mean()

        if volume < 0.002:
            return ""

        # ✅ pass source language to Whisper for better accuracy
        transcript = await transcribe_audio(audio_buffer, source_lang)

        if not transcript or len(transcript.strip()) <= 1:
            return ""

        skip_words = [
            "there is no text to translate", "no text",
            "nothing to translate", "thank you for watching",
            "you", ".", ",", "i", "the"
        ]
        if transcript.strip().lower() in skip_words:
            return ""

        logger.info(f"Transcribed: {transcript[:80]}")

        translated = await translate_text(transcript, target_lang)

        useless = ["there is no text to translate", "no text", "nothing to translate"]
        if any(u in translated.lower() for u in useless):
            return ""

        if translated.strip().lower() == transcript.strip().lower():
            return ""

        return translated

    except Exception as e:
        logger.error(f"Error in process_stream: {e}")
        return ""


async def transcribe_audio(audio_buffer, source_lang=None):
    try:
        if not GROQ_API_KEY:
            return ""

        wav_bytes = pcm_to_wav(audio_buffer)

        # ✅ build files with optional language hint
        files = {
            "file": ("audio.wav", wav_bytes, "audio/wav"),
            "model": (None, "whisper-large-v3-turbo"),
            "response_format": (None, "text")
        }

        # ✅ give Whisper language hint for better accuracy
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
        logger.error(f"Transcription error: {e}")
        return ""


async def translate_text(text, target_lang):
    try:
        if not GROQ_API_KEY:
            return text

        async with httpx.AsyncClient(timeout=15) as client:
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
                            "content": f"You are a translator. Translate the given text to {target_lang}. Return ONLY the translated text. No explanations."
                        },
                        {
                            "role": "user",
                            "content": text
                        }
                    ],
                    "temperature": 0,
                    "max_tokens": 500
                }
            )
            response.raise_for_status()
            result = response.json()
            translated = result["choices"][0]["message"]["content"].strip()
            logger.info(f"✅ {target_lang}: {translated[:80]}")
            return translated

    except Exception as e:
        logger.error(f"Translation error: {e}")
        return text


def pcm_to_wav(pcm_bytes):
    import struct, io
    num_channels = 1
    sample_rate = 16000
    bits_per_sample = 16
    wav_buffer = io.BytesIO()
    wav_buffer.write(b'RIFF')
    wav_buffer.write(struct.pack('<I', 36 + len(pcm_bytes)))
    wav_buffer.write(b'WAVE')
    wav_buffer.write(b'fmt ')
    wav_buffer.write(struct.pack('<I', 16))
    wav_buffer.write(struct.pack('<H', 1))
    wav_buffer.write(struct.pack('<H', num_channels))
    wav_buffer.write(struct.pack('<I', sample_rate))
    wav_buffer.write(struct.pack('<I', sample_rate * num_channels * bits_per_sample // 8))
    wav_buffer.write(struct.pack('<H', num_channels * bits_per_sample // 8))
    wav_buffer.write(struct.pack('<H', bits_per_sample))
    wav_buffer.write(b'data')
    wav_buffer.write(struct.pack('<I', len(pcm_bytes)))
    wav_buffer.write(pcm_bytes)
    wav_buffer.seek(0)
    return wav_buffer.read()