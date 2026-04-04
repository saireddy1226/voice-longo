// Main Application Logic - Voice-Lingo Call Management

class VoiceLingoApp {
    constructor() {
        this.currentUser = null;
        this.signalingManager = null;
        this.webrtcManager = null;
        this.translationManager = null;
        this.remoteUserId = null;
        this.remoteUserLanguage = null;
        this.callState = 'idle';
        this.callStartTime = null;
    }

    async initialize(user) {
        this.currentUser = user;
        this.signalingManager = new SignalingManager(user.user_id);
        this.webrtcManager = new WebRTCManager(this.signalingManager);
        await this.signalingManager.connect();
        console.log('App initialized for user:', user.name);
        this.setupSignalingHandlers();
    }

    setupSignalingHandlers() {
        this.signalingManager.on('incoming_call', (data) => {
            this.handleIncomingCall(data);
        });
        this.signalingManager.on('call_accepted', (data) => {
            this.handleCallAccepted(data);
        });
        this.signalingManager.on('call_confirmed', (data) => {
            this.handleCallConfirmed(data);
        });
        this.signalingManager.on('call_rejected', (data) => {
            this.handleCallRejected(data);
        });
        this.signalingManager.on('call_failed', (data) => {
            this.handleCallFailed(data);
        });
        this.signalingManager.on('call_ended', (data) => {
            this.handleCallEnded(data);
        });
        this.signalingManager.on('offer', (data) => {
            this.handleWebRTCOffer(data);
        });
        this.signalingManager.on('answer', (data) => {
            this.handleWebRTCAnswer(data);
        });
        this.signalingManager.on('ice_candidate', (data) => {
            this.handleICECandidate(data);
        });
    }

    async callUser(targetUserId, targetLanguage = 'English') {
        try {
            if (this.callState !== 'idle') {
                console.warn('Already in a call or call pending');
                return;
            }
            this.remoteUserId = targetUserId;
            this.remoteUserLanguage = targetLanguage;
            this.callState = 'calling';
            await this.webrtcManager.getLocalStream(true, false);
            this.webrtcManager.createPeerConnection();
            this.setupWebRTCHandlers();
            this.signalingManager.initiateCall(targetUserId);
            console.log('Call initiated to user:', targetUserId);
        } catch (error) {
            console.error('Error initiating call:', error);
            this.callState = 'idle';
        }
    }

    handleIncomingCall(data) {
        this.callState = 'receiving';
        this.remoteUserId = data.caller_id;
        this.remoteUserLanguage = data.caller_language;
        console.log('Incoming call from:', data.caller_name);
        if (this.onIncomingCall) {
            this.onIncomingCall({
                caller_id: data.caller_id,
                caller_name: data.caller_name,
                caller_language: data.caller_language,
                target_language: data.target_language
            });
        }
    }

    async acceptCall() {
        try {
            await this.webrtcManager.getLocalStream(true, false);
            this.webrtcManager.createPeerConnection();
            this.setupWebRTCHandlers();
            this.signalingManager.acceptCall();
            this.callState = 'active';
            console.log('Call accepted');
        } catch (error) {
            console.error('Error accepting call:', error);
        }
    }

    rejectCall(reason = 'User declined') {
        this.signalingManager.rejectCall();
        this.callState = 'idle';
        this.remoteUserId = null;
    }

    async handleCallAccepted(data) {
        this.remoteUserId = data.callee_id;
        console.log("Call accepted → opening call screen (caller)");

        // ✅ FIXED: added isCaller = true
        sessionStorage.setItem("receiverId", this.remoteUserId);
        sessionStorage.setItem("receiverLanguage", this.remoteUserLanguage || "English");
        sessionStorage.setItem("isCaller", "true");

        window.location.href = "call.html";
    }

    async handleCallConfirmed(data) {
        console.log("Call confirmed (receiver side)");
        this.callState = 'active';
    }

    handleCallRejected(data) {
        this.callState = 'idle';
        if (this.onCallRejected) {
            this.onCallRejected({
                user_id: data.callee_id,
                reason: data.reason
            });
        }
        this.webrtcManager.cleanup();
    }

    handleCallFailed(data) {
        this.callState = 'idle';
        if (this.onCallFailed) {
            this.onCallFailed({
                target_id: data.target_id,
                reason: data.reason
            });
        }
        this.webrtcManager.cleanup();
    }

    handleCallEnded(data) {
        this.callState = 'idle';
        if (this.onCallEnded) {
            this.onCallEnded({
                user_id: this.remoteUserId,
                duration: 0
            });
        }
        this.cleanup();
    }

    setupWebRTCHandlers() {
        this.webrtcManager.onRemoteStreamReady = (remoteStream) => {
            console.log('Remote stream ready');
            if (this.onRemoteStreamReady) {
                this.onRemoteStreamReady(remoteStream);
            }
        };
        this.webrtcManager.onConnectionEstablished = () => {
            console.log('WebRTC connection established');
            if (this.onConnectionEstablished) {
                this.onConnectionEstablished();
            }
        };
        this.webrtcManager.onConnectionFailed = () => {
            console.log('WebRTC connection failed');
            this.endCall();
        };
    }

    async initializeTranslation() {
        try {
            this.translationManager = new TranslationManager(this.currentUser.user_id);
            await this.translationManager.connect(
                this.currentUser.language,
                this.remoteUserLanguage
            );
            this.translationManager.onTranslationReceived = (data) => {
                if (this.onTranslationReceived) {
                    this.onTranslationReceived(data);
                }
            };
            await this.translationManager.startAudioCapture();
            console.log('Translation initialized');
        } catch (error) {
            console.error('Error initializing translation:', error);
        }
    }

    async handleWebRTCOffer(data) {
        try {
            await this.webrtcManager.handleOffer(data.offer);
        } catch (error) {
            console.error('Error handling offer:', error);
        }
    }

    async handleWebRTCAnswer(data) {
        try {
            await this.webrtcManager.handleAnswer(data.answer);
        } catch (error) {
            console.error('Error handling answer:', error);
        }
    }

    async handleICECandidate(data) {
        try {
            await this.webrtcManager.addIceCandidate(data.candidate);
        } catch (error) {
            console.error('Error adding ICE candidate:', error);
        }
    }

    endCall() {
        if (this.callState === 'active' || this.callState === 'calling' || this.callState === 'receiving') {
            this.signalingManager.endCall();
        }
        this.cleanup();
    }

    cleanup() {
        this.callState = 'idle';
        this.remoteUserId = null;
        this.remoteUserLanguage = null;
        if (this.translationManager) {
            this.translationManager.disconnect();
            this.translationManager = null;
        }
        if (this.webrtcManager) {
            this.webrtcManager.cleanup();
        }
    }

    disconnect() {
        this.cleanup();
        if (this.signalingManager) {
            this.signalingManager.disconnect();
        }
    }
}

let voiceLingoApp = null;

async function startVoiceLingo(user) {
    voiceLingoApp = new VoiceLingoApp();
    await voiceLingoApp.initialize(user);
    return voiceLingoApp;
}