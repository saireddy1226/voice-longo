// WebSocket Signaling Manager

class SignalingManager {

    constructor(user_id) {
        this.user_id = user_id
        this.ws = null
        this.isConnected = false
        this.callbacks = {}
        this.connectedToUser = sessionStorage.getItem("receiverId") || null
        this.callState = sessionStorage.getItem("isCaller") !== null ? "active" : "idle"
    }

    async connect(){
        return new Promise((resolve, reject)=>{
            // ✅ FIXED: use CONFIG.WS_URL instead of localhost
            this.ws = new WebSocket(`${CONFIG.WS_URL}/ws/signaling/${this.user_id}`)

            this.ws.onopen = () => {
                console.log("Signaling connected")
                this.isConnected = true
                resolve()
            }

            this.ws.onmessage = (event)=>{
                const data = JSON.parse(event.data)
                this.handleMessage(data)
            }

            this.ws.onerror = (err)=>{
                console.error("WebSocket error", err)
                reject(err)
            }

            this.ws.onclose = ()=>{
                console.log("WebSocket closed")
                this.isConnected = false
            }
        })
    }

    handleMessage(data){
        const type = data.type

        if(this.callbacks[type]){
            this.callbacks[type].forEach(cb => cb(data))
        }

        switch(type){
            case "incoming_call":
                this.callState = "receiving"
                break
            case "call_ringing":
                this.callState = "calling"
                break
            case "call_accepted":
                this.callState = "active"
                this.connectedToUser = data.callee_id
                break
            case "call_confirmed":
                this.callState = "active"
                this.connectedToUser = data.caller_id
                break
            case "call_active":
                this.callState = "active"
                this.connectedToUser = data.connected_to
                break
            case "call_rejected":
            case "call_failed":
            case "call_ended":
            case "call_closed":
                this.callState = "idle"
                this.connectedToUser = null
                break
        }
    }

    on(event, callback){
        if(!this.callbacks[event]){
            this.callbacks[event] = []
        }
        this.callbacks[event].push(callback)
    }

    initiateCall(targetUserId){
        if(!this.isConnected){
            console.error("WebSocket not connected")
            return
        }
        this.callState = "calling"
        this.connectedToUser = targetUserId
        this.ws.send(JSON.stringify({
            type: "call_request",
            target_id: targetUserId
        }))
    }

    acceptCall(){
        if(!this.isConnected) return
        this.ws.send(JSON.stringify({
            type: "call_accept"
        }))
    }

    rejectCall(){
        if(!this.isConnected) return
        this.ws.send(JSON.stringify({
            type: "call_reject"
        }))
    }

    sendWebRTCMessage(type, data={}){
        if(!this.isConnected){
            console.error("WebSocket not connected")
            return
        }
        const msg = { type: type, ...data }
        this.ws.send(JSON.stringify(msg))
    }

    endCall(){
        if(!this.isConnected) return
        this.ws.send(JSON.stringify({
            type: "end_call"
        }))
        this.callState = "idle"
        this.connectedToUser = null
    }

    disconnect(){
        if(this.ws){
            this.ws.close()
        }
    }
}