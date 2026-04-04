// WebRTC Peer Connection Manager

class WebRTCManager {

constructor(signalingManager){

this.signalingManager = signalingManager

this.peerConnection = null

this.localStream = null
this.remoteStream = null

this.dataChannels = {}

this.pendingIceCandidates = []

this.iceServers = [

{ urls:"stun:stun.l.google.com:19302" },
{ urls:"stun:stun1.l.google.com:19302" },
{ urls:"stun:stun2.l.google.com:19302" }

]

}

async getLocalStream(){

try{

this.localStream = await navigator.mediaDevices.getUserMedia({

audio:true,
video:false

})

console.log("📱 Local stream acquired:", this.localStream.getTracks())

return this.localStream

} catch(error) {

console.error("❌ Microphone permission denied:", error)

alert("Microphone access denied. Please enable microphone permissions.")

throw error

}

}

createPeerConnection(){

if(this.peerConnection) {

console.log("⚠️  Peer connection already exists, skipping creation")

return

}

this.peerConnection = new RTCPeerConnection({

iceServers:this.iceServers

})

console.log("🔗 Peer connection created")

if(this.localStream){

this.localStream.getTracks().forEach(track => {

this.peerConnection.addTrack(track,this.localStream)

console.log("✅ Added track to peer connection:", track.kind)

})

} else {

console.warn("⚠️  No local stream available yet - tracks will be added during offer/answer")

}

this.peerConnection.ontrack = (event)=>{

if(!this.remoteStream){

this.remoteStream = new MediaStream()

}

this.remoteStream.addTrack(event.track)

if(this.onRemoteStreamReady){

this.onRemoteStreamReady(this.remoteStream)

}

}

this.peerConnection.onicecandidate = (event)=>{

if(event.candidate){

this.signalingManager.sendWebRTCMessage("ice_candidate",{

candidate:event.candidate

})

}

}

this.peerConnection.onconnectionstatechange = ()=>{

console.log("Connection state:",this.peerConnection.connectionState)

if(this.peerConnection.connectionState==="connected"){

if(this.onConnectionEstablished){

this.onConnectionEstablished()

}

}

if(this.peerConnection.connectionState==="failed"){

if(this.onConnectionFailed){

this.onConnectionFailed()

}

}

}

this.peerConnection.ondatachannel = (event)=>{

this.setupDataChannel(event.channel)

}

}

createDataChannel(){

const channel = this.peerConnection.createDataChannel("data")

this.setupDataChannel(channel)

}

async createAndSendOffer(){

console.log("📞 Caller: Initiating offer...")

if(!this.localStream) {

await this.getLocalStream()

}

this.createPeerConnection()

this.createDataChannel()

const offer = await this.peerConnection.createOffer()

await this.peerConnection.setLocalDescription(offer)

console.log("📤 Sending offer")

this.signalingManager.sendWebRTCMessage("offer",{

offer:offer

})

}

async handleOffer(offerData){

console.log("📨 Callee: Received offer from caller")

try{

// Step 1: Get local stream if not already obtained
if(!this.localStream) {

console.log("📱 Getting local stream on callee side...")

await this.getLocalStream()

}

// Step 2: Create peer connection if not exists
if(!this.peerConnection) {

this.createPeerConnection()

// CRITICAL FIX: Add localStream tracks to PC BEFORE setRemoteDescription
// This ensures tracks are available when offer is processed
if(this.localStream) {

this.localStream.getTracks().forEach(track => {

if(!this.peerConnection.getSenders().some(s => s.track === track)) {

this.peerConnection.addTrack(track, this.localStream)

console.log("✅ Added local track to PC (callee):", track.kind)

}

})

}

}

// Step 3: Set remote description (caller's offer)
await this.peerConnection.setRemoteDescription(

new RTCSessionDescription(offerData)

)

console.log("✅ Remote description set")

// Step 4: Create and send answer
const answer = await this.peerConnection.createAnswer()

await this.peerConnection.setLocalDescription(answer)

console.log("📤 Sending answer")

this.signalingManager.sendWebRTCMessage("answer",{

answer:answer

})

} catch(error) {

console.error("❌ Error handling offer:", error)

throw error

}

}

async handleAnswer(answerData){

await this.peerConnection.setRemoteDescription(

new RTCSessionDescription(answerData)

)

this.flushIceCandidates()

}

async addIceCandidate(candidate){

try{

if(this.peerConnection.remoteDescription){

await this.peerConnection.addIceCandidate(

new RTCIceCandidate(candidate)

)

}else{

this.pendingIceCandidates.push(candidate)

}

}catch(e){

console.error("ICE error",e)

}

}

async flushIceCandidates(){

for(const c of this.pendingIceCandidates){

await this.peerConnection.addIceCandidate(

new RTCIceCandidate(c)

)

}

this.pendingIceCandidates = []

}

setupDataChannel(channel){

channel.onopen = ()=>{

console.log("Data channel open")

}

channel.onmessage = (event)=>{

if(this.onDataChannelMessage){

this.onDataChannelMessage(event.data)

}

}

channel.onclose = ()=>{

console.log("Data channel closed")

}

this.dataChannels[channel.label] = channel

}

sendData(data,label="data"){

const channel = this.dataChannels[label]

if(channel && channel.readyState==="open"){

channel.send(JSON.stringify(data))

}

}

stopLocalStream(){

if(this.localStream){

this.localStream.getTracks().forEach(t=>t.stop())

this.localStream = null

}

}

closePeerConnection(){

if(this.peerConnection){

this.peerConnection.close()

this.peerConnection = null

}

}

cleanup(){

this.stopLocalStream()

this.closePeerConnection()

this.remoteStream = null

this.dataChannels = {}

}

}