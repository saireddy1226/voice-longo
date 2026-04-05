class TranslationManager {

constructor(user_id, isCaller=true){
    this.user_id = user_id
    this.isCaller = isCaller
    this.ws = null
    this.recognition = null
    this.audioContext = null
    this.processor = null
    this.mediaStream = null
    this.callbacks = {}
    this.isActive = false
    this.callerLanguage = "English"
    this.targetLanguage = "English"
    // ✅ detect mobile
    this.isMobile = /Android|iPhone|iPad|iPod/i.test(navigator.userAgent)
}

getLangCode(language){
    const map = {
        "English": "en-US",
        "Hindi": "hi-IN",
        "Telugu": "te-IN",
        "Tamil": "ta-IN",
        "Spanish": "es-ES",
        "French": "fr-FR",
        "German": "de-DE",
        "Chinese": "zh-CN",
        "Japanese": "ja-JP",
        "Portuguese": "pt-BR",
        "Arabic": "ar-SA",
        "Russian": "ru-RU",
        "Korean": "ko-KR"
    }
    return map[language] || "en-US"
}

async connect(callerLanguage="English", targetLanguage="English"){
    return new Promise((resolve, reject)=>{
        try{
            this.callerLanguage = callerLanguage
            this.targetLanguage = targetLanguage

            this.ws = new WebSocket(`${CONFIG.WS_URL}/ws/translate/${this.user_id}`)

            this.ws.onopen = ()=>{
                console.log("Translation WebSocket connected")
                this.ws.send(JSON.stringify({
                    type: "set_languages",
                    caller_language: this.callerLanguage,
                    callee_language: this.targetLanguage
                }))
                resolve()
            }

            this.ws.onmessage = (event)=>{
                const data = JSON.parse(event.data)
                this.handleMessage(data)
            }

            this.ws.onerror = (err)=>{
                console.error("Translation socket error", err)
                reject(err)
            }

            this.ws.onclose = ()=>{
                console.log("Translation socket closed")
                this.isActive = false
            }

        }catch(err){
            reject(err)
        }
    })
}

handleMessage(data){
    const type = data.type
    if(this.callbacks[type]){
        this.callbacks[type].forEach(cb => cb(data))
    }
    switch(type){
        case "translated_text":
            console.log("Translation received:", data.text)
            if(this.onTranslationReceived){
                this.onTranslationReceived(data)
            }
            break
        case "translation_sent":
            console.log("Translation sent:", data.text)
            break
        case "languages_set":
            console.log("Languages configured")
            break
    }
}

on(event, callback){
    if(!this.callbacks[event]) this.callbacks[event] = []
    this.callbacks[event].push(callback)
}

startAudioCapture(existingStream){
    if(this.isMobile){
        console.log("📱 Mobile detected — using audio capture")
        this.startMobileAudioCapture(existingStream)
    } else {
        console.log("💻 Desktop detected — using Speech Recognition")
        this.startSpeechRecognition()
    }
}

// ✅ DESKTOP: use Web Speech API
startSpeechRecognition(){
    try{
        const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition
        if(!SpeechRecognition){
            console.warn("Speech Recognition not supported — falling back to audio")
            this.startMobileAudioCapture(this.mediaStream)
            return
        }

        this.recognition = new SpeechRecognition()
        this.recognition.continuous = true
        this.recognition.interimResults = false
        this.recognition.lang = this.getLangCode(this.callerLanguage)

        console.log(`🎤 Listening in: ${this.callerLanguage} (${this.recognition.lang})`)

        this.recognition.onresult = (event) => {
            const transcript = event.results[event.results.length - 1][0].transcript.trim()
            console.log("🗣️ Heard:", transcript)
            if(transcript && this.ws && this.ws.readyState === WebSocket.OPEN){
                this.ws.send(JSON.stringify({
                    type: "text_chunk",
                    text: transcript
                }))
            }
        }

        this.recognition.onerror = (event) => {
            console.error("Speech recognition error:", event.error)
            if(event.error !== "aborted" && this.isActive){
                setTimeout(() => {
                    try { this.recognition.start() } catch(e) {}
                }, 1000)
            }
        }

        this.recognition.onend = () => {
            if(this.isActive){
                try { this.recognition.start() } catch(e) {}
            }
        }

        this.recognition.start()
        this.isActive = true
        console.log("✅ Browser Speech Recognition started")

    }catch(error){
        console.error("Speech recognition error:", error)
        throw error
    }
}

// ✅ MOBILE: use raw audio chunks (Whisper on backend)
startMobileAudioCapture(existingStream){
    try{
        this.mediaStream = existingStream

        this.audioContext = new (window.AudioContext || window.webkitAudioContext)({
            sampleRate: 16000
        })

        const source = this.audioContext.createMediaStreamSource(this.mediaStream)
        this.processor = this.audioContext.createScriptProcessor(8192, 1, 1)

        source.connect(this.processor)
        this.processor.connect(this.audioContext.destination)

        this.processor.onaudioprocess = (event) => {
            this.handleAudioChunk(event)
        }

        this.isActive = true
        console.log("✅ Mobile audio capture started")

    }catch(error){
        console.error("Mobile audio capture error:", error)
        throw error
    }
}

handleAudioChunk(event){
    if(!this.isActive) return
    if(!this.ws || this.ws.readyState !== WebSocket.OPEN) return

    const inputData = event.inputBuffer.getChannelData(0)

    const volume = inputData.reduce((sum, val) => sum + Math.abs(val), 0) / inputData.length
    if(volume < 0.003) return

    const pcmData = this.convertFloat32ToInt16(inputData)
    const base64Audio = this.arrayBufferToBase64(pcmData)

    this.ws.send(JSON.stringify({
        type: "audio_chunk",
        audio: base64Audio,
        is_caller: this.isCaller
    }))
}

convertFloat32ToInt16(buffer){
    let l = buffer.length
    const buf = new Int16Array(l)
    while(l--){
        buf[l] = Math.min(1, buffer[l]) * 0x7fff
    }
    return buf.buffer
}

arrayBufferToBase64(buffer){
    let binary = ""
    const bytes = new Uint8Array(buffer)
    for(let i=0; i<bytes.byteLength; i++){
        binary += String.fromCharCode(bytes[i])
    }
    return btoa(binary)
}

stopAudioCapture(){
    // stop speech recognition
    if(this.recognition){
        this.isActive = false
        this.recognition.stop()
        this.recognition = null
    }
    // stop audio processor
    if(this.processor){
        this.processor.disconnect()
        this.processor = null
    }
    this.mediaStream = null
    if(this.audioContext){
        this.audioContext.close()
        this.audioContext = null
    }
    this.isActive = false
}

disconnect(){
    this.stopAudioCapture()
    if(this.ws){
        this.ws.close()
        this.ws = null
    }
}

}