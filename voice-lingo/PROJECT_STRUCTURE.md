# Voice-Lingo Project - Organized Structure

## 📋 Quick Overview

```
voice-lingo/
├── backend/              ← Python FastAPI server
│   ├── main.py           ← FastAPI app & HTTP endpoints
│   ├── signaling.py      ← WebSocket signaling logic
│   ├── translation.py    ← Real-time translation handler
│   ├── database.py       ← Supabase database operations
│   ├── ai_pipeline.py    ← Speech-to-text & translation
│   ├── config.py         ← Configuration management
│   ├── requirements.txt   ← Python dependencies
│   └── procfile          ← Deployment configuration
│
├── frontend/             ← Complete web application
│   ├── index.html        ← Entry point (splash + welcome)
│   ├── register.html     ← User registration step 1
│   ├── password.html     ← User registration step 2
│   ├── login.html        ← User login page
│   ├── dashboard.html    ← Main call interface hub
│   ├── call.html         ← Active call screen
│   ├── chat.html         ← Chat list page
│   ├── chatroom.html     ← Chat messaging page
│   ├── history.html      ← Call history page
│   ├── serve.py          ← Frontend development server
│   ├── STRUCTURE.md      ← Frontend architecture docs
│   ├── css/              ← Stylesheets
│   │   ├── style.css     ← Global & dashboard styles
│   │   ├── call.css      ← Call page styling
│   │   ├── chat.css      ← Chat list styling
│   │   ├── chatroom.css  ← Chat messaging styling
│   │   └── history.css   ← Call history styling
│   └── js/               ← JavaScript controllers
│       ├── app.js        ← Main app coordinator
│       ├── auth.js       ← User authentication manager
│       ├── signaling.js  ← WebSocket call signaling
│       ├── webrtc.js     ← Peer-to-peer audio manager
│       ├── translation.js ← Real-time translation manager
│       └── config.js     ← Configuration & constants
│
├── README.md             ← Project overview
├── QUICK_START.md        ← 5-minute setup guide
├── SETUP_GUIDE.md        ← Detailed setup instructions
├── API_REFERENCE.md      ← Complete API documentation
├── FRONTEND_GUIDE.md     ← Frontend implementation guide
├── IMPLEMENTATION_CHECKLIST.md ← Feature completion status
├── .env.example          ← Example environment variables
└── .git/                 ← Git repository
```

## 🚀 To Get Started

### 1. **Start the Backend**
```bash
cd backend
python -m venv venv
venv\Scripts\activate  # Windows
pip install -r requirements.txt
uvicorn main:app --reload
```

### 2. **Open the Frontend**
Open `index.html` in your browser

### 3. **Follow the User Journey**

```
index.html (Entry point)
   ↓ [Splash screen auto-hides after 2-3 seconds]
   
Welcome/Choice Page
   ├─ [Register] → register.html
   │              → password.html
   │              → dashboard.html
   │
   └─ [Login] → login.html
               → dashboard.html

Dashboard (Main Hub - Central navigation point)
   ├─ [Start Call] → Input user ID → call.html
   ├─ [💬 Chat] → chat.html
   │           → chatroom.html (select user)
   │
   └─ [📞 History] → history.html
                    ├─ [Call] → call.html
                    └─ [Chat] → chatroom.html
```

## 📂 Folder Structure Explained

### **frontend/index.html**
- Entry point to the application
- Shows splash screen (2-3 sec animation)
- Displays welcome/choice page (Register or Login buttons)
- Routes to: `register.html` and `login.html`

### **frontend/Register Flow** (Multi-step)
- `register.html` - Step 1: Enter name, email, language preference
- `password.html` - Step 2: Create password with validation (8+ chars, special char, digit)
- Auto-redirects to `dashboard.html` on success

### **frontend/Login**
- `login.html` - Enter User ID + Password
- Routes to `dashboard.html` on successful authentication

### **frontend/Main Application** (After Login)
- `dashboard.html` - Central hub with call input, profile dropdown, navigation
- `call.html` - Active call screen with timer, mic/speaker controls, translation display
- `chat.html` - Recent chats list with user selection
- `chatroom.html` - Real-time message thread with selected user
- `history.html` - Call logs with quick actions (call/chat buttons)

### **frontend/js/** (5 Controllers)
1. `app.js` - Main coordinator & event handler
2. `auth.js` - User registration & login manager
3. `signaling.js` - WebSocket call management
4. `webrtc.js` - Peer-to-peer audio connection
5. `translation.js` - Real-time speech translation handler
6. `config.js` - Configuration & API endpoints

### **frontend/css/** (5 Stylesheets)
1. `style.css` - Global styles, index, register, password, login, dashboard, profile dropdown
2. `call.css` - Call page styling (timer, controls, translation display)
3. `chat.css` - Chat list page styling
4. `chatroom.css` - Chat message thread styling
5. `history.css` - Call history page styling

## 🔗 Important File Relationships

### HTML File Navigation Flow
```
index.html (Entry point)
  ├─→ register.html (href="register.html")
  │    └─→ password.html (href="password.html")
  │         └─→ dashboard.html (href="dashboard.html")
  │
  └─→ login.html (href="login.html")
       └─→ dashboard.html (href="dashboard.html")

dashboard.html (Main hub)
  ├─→ call.html (window.location.href = 'call.html')
  ├─→ chat.html (onclick="location.href='chat.html'")
  └─→ history.html (onclick="location.href='history.html'")

chat.html
  └─→ chatroom.html (window.location.href = 'chatroom.html')

chatroom.html
  ├─→ chat.html (onclick="location.href='chat.html'")
  └─→ dashboard.html (onclick="location.href='dashboard.html'")

history.html
  ├─→ call.html (onclick="callUser(userId)")
  └─→ chatroom.html (onclick="chatUser(userId)")
```

### CSS/JS File Links
All HTML files are in the same directory, so they use direct paths:
- All CSS files: `css/style.css`, `css/call.css`, `css/chat.css`, `css/chatroom.css`, `css/history.css`
- All JS files: `js/app.js`, `js/auth.js`, `js/signaling.js`, `js/webrtc.js`, `js/translation.js`, `js/config.js`

## 💾 Data Storage

### localStorage
- `userId` - Current user ID
- `currentUser` - Full user object (JSON)
- `userPassword` - Password (demo only)
- `recentChats` - Array of chat user IDs
- `callHistory` - Array of call logs
- `chatMessages` - All messages between users

### sessionStorage
- `regName`, `regEmail`, `regLanguage` - Temp registration data
- `receiverId`, `receiverLanguage` - Temp call target
- `chatUserId` - Temp current chat user

## ✅ What You Have

- **9 HTML files** organized by feature
- **5 JavaScript managers** for different functionalities
- **5 CSS files** for styling each page
- **Clear separation** of authentication vs. application
- **Proper relative paths** for easy navigation
- **Complete documentation** in STRUCTURE.md

## 🎯 Key Features by Page

| Page | Purpose | Features |
|------|---------|----------|
| `index.html` | Entry point | Splash screen, welcome buttons |
| `pages/auth/register.html` | User registration step 1 | Name, email, language input |
| `pages/auth/password.html` | User registration step 2 | Password creation with validation |
| `pages/auth/login.html` | User login | User ID + password login |
| `pages/app/dashboard.html` | Main hub | Call input, profile dropdown, navigation |
| `pages/app/call.html` | Active call | Timer, mic/speaker controls, end call |
| `pages/app/chat.html` | Chat list | Recent chats, start new chat |
| `pages/app/chatroom.html` | Chat messaging | Message thread, send message, call button |
| `pages/app/history.html` | Call history | Recent calls with call/chat options |

---

**Everything is organized, clear, and ready to use!** 🎉
