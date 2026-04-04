# Voice-Lingo - Complete Setup Guide

A real-time voice communication platform with AI-powered translation, enabling seamless conversations across language barriers using WebRTC and WebSocket technology.

## ✨ Key Features

### 1. **User Registration & Authentication**
- Register with unique user ID generation
- Email-based user identification
- Multiple language preference support
- User profile management

### 2. **Call by User ID**
- Search and call any registered user by their unique ID
- Real-time call status updates
- Call history tracking
- Support for calling offline users with notifications

### 3. **Real-time Multilingual Translation**
- **Dual-direction Translation**: Both caller and callee receive translated messages
- **Support for 8+ Languages**: English, Spanish, French, German, Hindi, Chinese, Japanese, Portuguese
- **Custom Language Selection**: Choose target language based on call context
- **Live Translation Display**: See translations in real-time during calls
- **Groq AI Integration**: Fast and cost-effective translation service

### 4. **WebRTC Audio Communication**
- Peer-to-peer audio calls (no server overhead)
- Automatic ICE candidate handling
- Multiple STUN servers for NAT traversal
- Connection state monitoring

### 5. **WebSocket Signaling**
- Efficient call signaling protocol
- Real-time messaging between peers
- Proper connection state management
- Automatic cleanup on disconnection

## 📋 Prerequisites

### Backend Requirements
- Python 3.8 or higher
- pip (Python package manager)
- Virtual environment (recommended)

### Frontend Requirements
- Modern web browser with WebRTC support
- No additional installations needed (pure HTML/CSS/JS)

### External Services
- **Supabase Account**: For user database and authentication
  - Create account at [supabase.com](https://supabase.com)
  - Create a project and get URL and API key
  - Create the following tables:
    - `users` (user_id, name, email, password_hash, language, online_status, created_at)
    - `call_history` (call_id, caller_id, callee_id, duration, status, timestamp)

- **Groq API Key**: For translation service
  - Get free API key at [console.groq.com](https://console.groq.com)
  - Free tier provides generous API rate limits for development

## 🚀 Installation & Setup

### Step 1: Prepare Environment

```bash
# Navigate to project directory
cd voice-lingo

# Create Python virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate
```

### Step 2: Install Backend Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### Step 3: Create `.env` File

Create a file named `.env` in the `backend` directory:

```env
# OpenAI/Groq Configuration
GROQ_API_KEY=your_groq_api_key_here

# Supabase Configuration
SUPABASE_URL=your_supabase_url_here
SUPABASE_KEY=your_supabase_api_key_here
```

**Get these credentials:**
- **Groq**: https://console.groq.com (Create account, get API key)
- **Supabase**: https://supabase.com (Create project, copy URL and anon key)

### Step 4: Setup Supabase Database

Create the following tables in Supabase:

#### Users Table
```sql
CREATE TABLE users (
  id BIGINT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
  user_id TEXT UNIQUE NOT NULL,
  name TEXT NOT NULL,
  email TEXT UNIQUE NOT NULL,
  password_hash TEXT NOT NULL,
  language TEXT DEFAULT 'English',
  online_status BOOLEAN DEFAULT FALSE,
  created_at TIMESTAMP DEFAULT NOW()
);
```

#### Call History Table
```sql
CREATE TABLE call_history (
  id BIGINT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
  call_id TEXT UNIQUE NOT NULL,
  caller_id TEXT,
  callee_id TEXT,
  duration INTEGER,
  status TEXT,
  timestamp TIMESTAMP DEFAULT NOW()
);
```

## 🎯 Running the Application

### Start Backend Server

```bash
cd backend
uvicorn main:app --reload
```

Backend will run at: `http://localhost:8000`

### Access Frontend

Open a web browser and navigate to:

```
file:///full/path/to/frontend/index.html
```

Or use Python's built-in server:

```bash
cd frontend
python -m http.server 8080
```

Then visit: `http://localhost:8080/index.html`

## 📱 How to Use

### Registration & Login

1. Visit the landing page (index.html)
2. Click "Create Account" or "Log In"
3. For new users:
   - Enter name, email, and preferred language
   - Click "Register"
   - User ID is automatically generated
4. For existing users:
   - Enter email
   - Click "Log In"

### Making a Call

1. After logging in, you're on the Dashboard
2. **Copy Your User ID**: Click the "📋 Copy My User ID" button to copy your unique identifier
3. **Share Your ID**: Send your user ID to the person you want to call
4. **Call Someone**: 
   - Enter their user ID in "Target User ID" field
   - Select the language they speak from "Target Language" dropdown
   - Click "Start Call"
5. **Accept/Reject**: When receiving a call, you'll see an alert with the caller's details
   - Click "Accept Call" to connect
   - Click "Reject Call" to decline

### During a Call

- **Real-time Translation**: See live translations of both parties' speech
- **Audio Communication**: Clear audio transmission between both users
- **Call Duration**: Monitor active call time
- **End Call**: Click "End Call" button to terminate the call

## 🏗️ Architecture

### Backend Structure

```
backend/
├── main.py              # FastAPI app with HTTP endpoints
├── signaling.py         # WebSocket signaling logic
├── translation.py       # Real-time translation WebSocket
├── database.py          # Supabase integration
├── ai_pipeline.py       # Speech-to-text and translation
├── config.py            # Configuration management
└── requirements.txt     # Python dependencies
```

### Frontend Structure

```
frontend/
├── index.html           # Registration/Login page
├── dashboard.html       # Main call interface
├── js/
│   ├── auth.js         # User registration and login
│   ├── app.js          # Main application logic
│   ├── signaling.js    # WebSocket signaling client
│   ├── webrtc.js       # WebRTC peer connection
│   └── translation.js  # Real-time translation
├── css/
│   └── style.css       # Global styles
└── js/
    └── (other js files)
```

## 📡 API Endpoints

### HTTP Endpoints

#### User Registration
```
POST /register
Content-Type: application/json

{
  "name": "John Doe",
  "email": "john@example.com",
  "language": "English"
}

Response: {
  "success": true,
  "user_id": "uuid-here",
  "message": "Registration successful"
}
```

#### Get User Info
```
GET /users/{user_id}

Response: {
  "success": true,
  "user": { user object }
}
```

#### List All Users
```
GET /users-list

Response: {
  "success": true,
  "users": [{ user object }, ...]
}
```

### WebSocket Endpoints

#### Signaling WebSocket
```
ws://localhost:8000/ws/signaling/{user_id}
```

Messages:
- `call_request`: Initiate a call to another user
- `call_accept`: Accept incoming call
- `call_reject`: Reject incoming call
- `offer`: WebRTC offer
- `answer`: WebRTC answer
- `ice_candidate`: ICE candidate
- `end_call`: End active call

#### Translation WebSocket
```
ws://localhost:8000/ws/translate/{user_id}
```

Messages:
- `set_languages`: Set caller and target languages
- `audio_chunk`: Send audio data for translation
- `translated_text`: Receive translated text

## 🔐 Security Considerations

- **HTTPS Required**: Use HTTPS in production for secure communication
- **Authentication**: Implement JWT tokens for API endpoints
- **CORS**: Configure CORS appropriately for your domain
- **Rate Limiting**: Add rate limiting to prevent abuse
- **Input Validation**: All inputs are validated on backend
- **WebRTC**: Encrypted by default (SRTP)

## 📊 Message Flow

### Call Initiation Flow

```
User A                          Server                      User B
  |                               |                           |
  |------ call_request ---------->|                           |
  |                               |------ incoming_call ----->|
  |<------ call_initiated --------|                           |
  |                               |<------ call_accept -------|
  |<----- call_accepted/confirmed-|                           |
  |                               |--- call_confirmed/accepted|
  |                               |                           |
  |---------- offer ------------->|---------- offer --------->|
  |<--------- answer --------------|<--------- answer ---------|
  |                               |                           |
  |--- ice_candidate ------------>|--- ice_candidate -------->|
  |<-- ice_candidate --------------|<-- ice_candidate ---------|
  |                               |                           |
  |====== WebRTC Audio Stream====>|<====WebRTC Audio Stream===|
  |                               |                           |
  |===Real-time Translation====>| |<===Real-time Translation===|
  |                               |                           |
  |------ end_call ------------->|------ call_ended -------->|
```

## 🐛 Troubleshooting

### Backend Issues

**ERROR: "ModuleNotFoundError: No module named 'faster_whisper'"**
```bash
pip install faster-whisper
```

**ERROR: "connect() got an unexpected keyword argument"**
- Ensure Supabase URL and key are correct in `.env`

**ERROR: "OPENROUTER_API_KEY not found"**
- Add OpenRouter API key to `.env` file

### Frontend Issues

**ERROR: "WebSocket connection failed"**
- Ensure backend is running on `http://localhost:8000`
- Check browser console for detailed errors
- Verify CORS is enabled (included in backend)

**ERROR: "Microphone access denied"**
- Check browser permissions for microphone access
- Use HTTPS in production (WebRTC requires secure context)

**ERROR: "No remote audio"**
- Check network connectivity
- Verify WebRTC ICE servers are accessible
- Check browser's WebRTC settings

## 📈 Performance Tips

1. **Audio Buffer**: Recommended 2-second chunks for optimal translation
2. **Sample Rate**: 16kHz for best speech-to-text accuracy
3. **Compression**: Consider audio compression for bandwidth savings
4. **Threading**: Backend uses async/await for non-blocking I/O

## 🔄 Future Enhancements

- [ ] Video call support
- [ ] Screen sharing
- [ ] Call recording and transcription
- [ ] Advanced codec support
- [ ] Load balancing for multiple servers
- [ ] Sentiment analysis in translations
- [ ] Call scheduling and invitations
- [ ] Mobile app (React Native/Flutter)
- [ ] End-to-end encryption for calls

## 📝 License

[Add your license information here]

## 🤝 Contributing

Contributions are welcome! Please follow these steps:
1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## 💬 Support

For issues, questions, or feedback, please:
- Open an issue on the GitHub repository
- Contact the development team
- Check the documentation for solutions

---

**Made with ❤️ for breaking language barriers in voice communication**
