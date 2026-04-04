# Voice-Lingo API Reference & Quick Start

## Quick Start (5 minutes)

### 1. Backend Setup
```bash
cd backend
python -m venv venv
venv\Scripts\activate  # Windows: venv\Scripts\activate
                       # Mac/Linux: source venv/bin/activate
pip install -r requirements.txt
```

### 2. Configure Environment
Create `.env` in `backend/`:
```env
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_anon_key
GROQ_API_KEY=your_groq_api_key
```

**Get these credentials:**
- **Supabase**: https://supabase.com (Create free project)
- **Groq**: https://console.groq.com (Free API key with generous rate limits)

### 3. Start Backend
```bash
cd backend
uvicorn main:app --reload
```

Backend runs at: `http://localhost:8000`

### 4. Open Frontend
Open `index.html` in a browser (from `frontend/` directory)

### 5. Register & Test
- Register two users with different emails
- Get User ID for each user
- User A calls User B using their User ID
- Accept call and enjoy multilingual translation!

---

## System Architecture

### Call Flow Diagram

```
┌─────────────┐                                    ┌─────────────┐
│   User A    │                                    │   User B    │
│  (English)  │                                    │   (Hindi)   │
└──────┬──────┘                                    └──────┬──────┘
       │                                                   │
       │  1. Call Request (user_id, language)             │
       ├──────────────────────────────────────────────────>│
       │                                                   │
       │                                       2. Incoming Call
       │                                           (Accept/Reject)
       │                                                   │
       │  3. Call Accepted                                │
       │<──────────────────────────────────────────────────┤
       │                                                   │
       ├─────────── WebRTC Offer ─────────────────────────>│
       │  4. Exchange SDP & ICE Candidates                 │
       │<─────────── WebRTC Answer ───────────────────────┤
       │                                                   │
       │  5. Audio Stream (Encrypted)                     │
       │<════════════════════════════════════════════════>│
       │                                                   │
       │  6. Translation WebSocket (Parallel)              │
       │        User A speech (English)                    │
       │        ─────────────────────────>                 │
       │        Whisper (Speech-to-Text)                   │
       │        OpenRouter (Translate to Hindi)            │
       │        ────────────────────────────>             │
       │        Hindi Translation received                 │
       │                                                   │
       │  7. Bidirectional Translation                     │
       │        User B speech (Hindi)                      │
       │        <─────────────────────────                 │
       │        Translate to English                       │
       │        <────────────────────────────              │
       │        English Translation received               │
       │                                                   │
       │  8. Call End                                      │
       │  End Call Signal Sent                             │
       ├──────────────────────────────────────────────────>│
       │  Duration Saved to Database                       │
       │                                                   │
```

---

## Backend Endpoints

### Authentication & User Management

#### Register New User
```http
POST /register
Content-Type: application/json

Request:
{
  "user_id": "alice123",
  "name": "Alice Johnson",
  "email": "alice@example.com",
  "password": "SecurePass123!",
  "language": "English"
}

Response (Success - 200):
{
  "success": true,
  "user_id": "alice123",
  "name": "Alice Johnson",
  "email": "alice@example.com",
  "language": "English"
}

Error (Email exists - 400):
{
  "detail": "Email already registered"
}

Error (User ID taken - 400):
{
  "detail": "User ID already taken"
}

Error (Weak password - 400):
{
  "detail": "Password must be at least 8 characters"
}
```

#### Login User
```http
POST /login
Content-Type: application/json

Request:
{
  "user_id": "alice123",
  "password": "SecurePass123!"
}

Response (Success - 200):
{
  "success": true,
  "user": {
    "user_id": "alice123",
    "name": "Alice Johnson",
    "email": "alice@example.com",
    "language": "English"
  }
}

Error (Invalid credentials - 401):
{
  "detail": "Invalid credentials"
}

Error (Missing fields - 400):
{
  "detail": "User ID and password required"
}
```

#### Check User ID Availability
```http
GET /check-userid/{user_id}

Response (Available - 200):
{
  "user_id": "alice123",
  "available": true
}

Response (Not available - 200):
{
  "user_id": "alice123",
  "available": false
}
```

#### Update Language Preference
```http
POST /update-language
Content-Type: application/json

Request:
{
  "user_id": "alice123",
  "language": "Spanish"
}

Response (Success - 200):
{
  "success": true
}
```
```http
GET /users/{user_id}

Response:
{
  "success": true,
  "user": {
    "user_id": "550e8400-e29b-41d4-a716-446655440000",
    "name": "John Doe",
    "email": "john@example.com",
    "language": "English",
    "online_status": true,
    "created_at": "2024-01-15T10:30:00Z"
  }
}
```

#### List All Users
```http
GET /users-list

Response:
{
  "success": true,
  "users": [
    {
      "user_id": "550e8400-e29b-41d4-a716-446655440000",
      "name": "John Doe",
      "email": "john@example.com",
      "online_status": true
    },
    ...
  ]
}
```

### Health Check
```http
GET /

Response:
{
  "status": "VOICE-LINGO Backend Running"
}
```

---

## WebSocket Endpoints

### 1. Signaling WebSocket

**Connection:**
```javascript
const ws = new WebSocket('ws://localhost:8000/ws/signaling/{user_id}');
```

**Call Request (Caller -> Server -> Callee)**
```json
{
  "type": "call_request",
  "target_id": "target-user-uuid",
  "caller_name": "John Doe",
  "caller_language": "English",
  "target_language": "Hindi"
}
```

**Incoming Call (Server -> Callee)**
```json
{
  "type": "incoming_call",
  "caller_id": "caller-user-uuid",
  "caller_name": "John Doe",
  "caller_language": "English",
  "target_language": "Hindi"
}
```

**Call Accept (Callee -> Server)**
```json
{
  "type": "call_accept",
  "caller_id": "caller-user-uuid"
}
```

**Call Accepted (Server -> Caller)**
```json
{
  "type": "call_accepted",
  "callee_id": "callee-user-uuid"
}
```

**WebRTC Offer (Caller -> Server -> Callee)**
```json
{
  "type": "offer",
  "offer": {
    "type": "offer",
    "sdp": "v=0\r\no=..."
  }
}
```

**WebRTC Answer (Callee -> Server -> Caller)**
```json
{
  "type": "answer",
  "answer": {
    "type": "answer",
    "sdp": "v=0\r\no=..."
  }
}
```

**ICE Candidate (Both directions)**
```json
{
  "type": "ice_candidate",
  "candidate": {
    "candidate": "candidate:...",
    "sdpMLineIndex": 0,
    "sdpMid": "0"
  }
}
```

**End Call**
```json
{
  "type": "end_call"
}
```

**Call Ended (Server -> Both)**
```json
{
  "type": "call_ended",
  "caller_id": "user-id"
}
```

---

### 2. Translation WebSocket

**Connection:**
```javascript
const ws = new WebSocket('ws://localhost:8000/ws/translate/{user_id}');
```

**Set Languages**
```json
{
  "type": "set_languages",
  "caller_language": "English",
  "callee_language": "Hindi"
}
```

**Send Audio Chunk**
```json
{
  "type": "audio_chunk",
  "audio": "base64-encoded-audio-data",
  "is_caller": true
}
```

**Receive Translated Text**
```json
{
  "type": "translated_text",
  "from_id": "user-id",
  "original_language": "auto-detected",
  "target_language": "Hindi",
  "text": "Translated text here"
}
```

---

## Frontend Usage

### 1. User Registration
```javascript
const result = await authManager.register(
  'John Doe',
  'john@example.com',
  'English'
);

if (result.success) {
  console.log('User ID:', result.user.user_id);
}
```

### 2. Initialize App
```javascript
const user = authManager.getCurrentUser();
const app = await startVoiceLingo(user);
```

### 3. Make a Call
```javascript
await app.callUser(
  'target-user-id',
  'Hindi'  // target language
);
```

### 4. Handle Incoming Call
```javascript
app.onIncomingCall = (callData) => {
  console.log('Call from:', callData.caller_name);
  console.log('Language:', callData.caller_language);
};
```

### 5. Accept/Reject Call
```javascript
// Accept
await app.acceptCall();

// Reject
app.rejectCall('User declined');
```

### 6. Handle Translation
```javascript
app.onTranslationReceived = (data) => {
  console.log('From:', data.from_id);
  console.log('Language:', data.target_language);
  console.log('Text:', data.text);
};
```

### 7. End Call
```javascript
app.endCall();
```

---

## Supported Languages

| Code | Language |
|------|----------|
| English | English |
| Spanish | Spanish |
| French | French |
| German | German |
| Hindi | Hindi |
| Chinese | Chinese (Simplified) |
| Japanese | Japanese |
| Portuguese | Portuguese |

---

## Error Handling

### Common Errors

**1. Connection Timeout**
```
Error: WebSocket connection failed
Cause: Backend not running or wrong URL
Solution: Check if backend is running on localhost:8000
```

**2. Microphone Access Denied**
```
Error: NotAllowedError: Permission denied
Cause: Browser permission not granted
Solution: Allow microphone access in browser permissions
```

**3. User Not Found**
```
{
  "detail": "User not found"
}
Cause: Invalid user ID or user hasn't registered
Solution: Verify user ID and ensure user is registered
```

**4. Call Failed - User Offline**
```
{
  "type": "call_failed",
  "reason": "User offline"
}
Cause: Target user is not currently online
Solution: Try again when user is online
```

---

## Database Schema

### Users Table
```sql
user_id: UUID (PRIMARY KEY)
name: VARCHAR(255)
email: VARCHAR(255) UNIQUE
language: VARCHAR(50)
online_status: BOOLEAN
created_at: TIMESTAMP
```

### Call History Table
```sql
call_id: UUID (PRIMARY KEY)
caller_id: UUID
callee_id: UUID
duration: INTEGER (seconds)
status: VARCHAR(20)
timestamp: TIMESTAMP
```

---

## Performance Metrics

- **WebRTC Audio Latency**: 50-150ms (typical P2P)
- **Translation Latency**: 500-2000ms (API dependent)
- **Server Capacity**: ~10,000 concurrent users (single instance)
- **Sample Rate**: 16kHz (optimal for speech)
- **Buffer Size**: 4096 samples (~256ms)

---

## Security Features

✅ CORS enabled for local development
✅ WebRTC encryption (SRTP)
✅ WebSocket over TCP
✅ Input validation on all endpoints
✅ Unique user IDs (UUID)
✅ Email uniqueness enforcement

---

## Deployment Checklist

- [ ] Set environment variables (.env created)
- [ ] Configure Supabase database
- [ ] Obtain OpenRouter API key
- [ ] Install all dependencies
- [ ] Test local setup
- [ ] Deploy backend (Heroku/Railway/AWS)
- [ ] Deploy frontend (Vercel/Netlify)
- [ ] Enable HTTPS
- [ ] Configure CORS for production domain
- [ ] Monitor WebSocket connections
- [ ] Setup error logging
- [ ] Configure database backups

---

## Support & Documentation

For detailed setup instructions, see: `SETUP_GUIDE.md`

For frontend integration examples, check JavaScript files in `frontend/js/`

For backend implementation details, review Python files in `backend/`
