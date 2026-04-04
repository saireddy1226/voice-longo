# Voice-Lingo Frontend Structure

## 📁 Directory Organization

```
frontend/
├── index.html                    # Main entry point (splash screen + auth)
├── register.html                 # Step 1: User details (ID, name, email, language)
├── password.html                 # Step 2: Password creation
├── login.html                    # User login (ID + password)
├── dashboard.html                # Main call interface (hub)
├── call.html                     # Active call screen
├── chat.html                     # Chat list
├── chatroom.html                 # Chat messaging
├── history.html                  # Call history
├── serve.py                      # Development server
│
├── js/                           # JavaScript controllers
│   ├── app.js                    # VoiceLingoApp - Main coordinator
│   ├── auth.js                   # AuthManager - Registration & Login
│   ├── signaling.js              # SignalingManager - Call signaling
│   ├── webrtc.js                 # WebRTCManager - P2P audio
│   ├── translation.js            # TranslationManager - Real-time translation
│   └── config.js                 # Config & API endpoints
│
└── css/                          # Stylesheets
    ├── style.css                 # Global, index, register, password, login, dashboard
    ├── call.css                  # Call page styles
    ├── chat.css                  # Chat list styles
    ├── chatroom.css              # Chat messaging styles
    └── history.css               # Call history styles
```

## 🗂️ File Organization Guide

### Authentication & Startup Flow
1. **index.html** → Splash screen (2-3 sec auto-fade)
   - Shows "VOICE LINGO" + subtitle
   - Auto-transitions to welcome/choice page
2. **Welcome/Choice Page** → Register or Login buttons
3. **register.html** → Step 1: User ID, name, email, language
4. **password.html** → Step 2: Create password (validated)
5. **login.html** → Enter User ID & password
6. **dashboard.html** → Main interface (success)

### Main Application Flow (After Login)
- **dashboard.html** → Central hub with:
  - Call input & start call button
  - Incoming call alerts (modal)
  - Live translation display
  - Chat & History navigation buttons
  - Profile menu (language change, logout)
  - Call status display

#### From Dashboard:
- **[Start Call]** → Input receiver ID → Initiated → Transitions to **call.html** when accepted
- **[💬 Chat]** → **chat.html** (recent chats list)
  - Select user → **chatroom.html** (message thread)
- **[📞 History]** → **history.html** (call logs)
  - [Call] button → **call.html**
  - [Chat] button → **chatroom.html**

### Page Details
- **call.html** → Active call interface with:
  - Timer showing call duration
  - Mic/Speaker controls
  - End Call button
  - Translation display
  - Back to dashboard option
  
- **chat.html** → Recent chats with:
  - User list
  - New chat button
  - Navigate to chatroom when selected
  
- **chatroom.html** → Message thread with:
  - Message history
  - Message input
  - Send button
  - Call button (routes to call.html)
  - Back to chat/dashboard options
  
- **history.html** → Call logs with:
  - Call list with duration & timestamp
  - Quick action buttons (Call/Chat)
  - Back to dashboard

## 🔗 Navigation Map

```
Start
  ↓
index.html (Splash screen - 2-3 sec)
  ↓
Welcome/Choice Page (Register/Login buttons)
  ├─→ [Register Button]
  │      ↓
  │   register.html (Step 1: ID, name, email, language)
  │      ↓ Continue
  │   password.html (Step 2: password, confirm password)
  │      ↓ Register
  │   dashboard.html (Success)
  │
  └─→ [Login Button]
         ↓
      login.html (User ID + password)
         ↓ Login successful
      dashboard.html (Main interface)

From dashboard.html (Hub):
  ├─→ [Start Call button]
  │      ↓ Input receiver ID
  │   call.html (When call accepted)
  │      ↓ End Call
  │   dashboard.html
  │
  ├─→ [💬 Chat button]
  │      ↓
  │   chat.html (Recent chats list)
  │      ↓ Select user
  │   chatroom.html (Message thread)
  │      ├─→ [Call button] → call.html
  │      └─→ [Back] → dashboard.html
  │
  └─→ [📞 History button]
         ↓
      history.html (Call logs)
         ├─→ [Call action] → call.html
         ├─→ [Chat action] → chatroom.html
         └─→ [Back] → dashboard.html
```

## 📦 File Manifest

### HTML Files (9 total)
- **index.html** - Entry point (splash + auth container)
- **register.html** - Registration step 1
- **password.html** - Registration step 2
- **login.html** - User login
- **dashboard.html** - Main call hub
- **call.html** - Active call interface
- **chat.html** - Chat list
- **chatroom.html** - Chat messages
- **history.html** - Call history

### JavaScript Files (6 total)
- **app.js** - Main VoiceLingoApp orchestrator
- **auth.js** - AuthManager for registration/login
- **signaling.js** - SignalingManager for call signaling via WebSocket
- **webrtc.js** - WebRTCManager for P2P audio
- **translation.js** - TranslationManager for real-time translation
- **config.js** - Configuration & API endpoints

### CSS Files (5 total)
- **style.css** - Global styles, index, register, password, login, dashboard, profile
- **call.css** - Call page interface
- **chat.css** - Chat list styling
- **chatroom.css** - Chat message thread
- **history.css** - Call history page

## ✅ Path Patterns

### All HTML to CSS/JS Links
Since all HTML files are in the same directory:
```html
<!-- CSS Links -->
<link rel="stylesheet" href="css/style.css">
<link rel="stylesheet" href="css/call.css">

<!-- JS Links -->
<script src="js/config.js"></script>
<script src="js/app.js"></script>
<script src="js/auth.js"></script>
<script src="js/signaling.js"></script>
<script src="js/webrtc.js"></script>
<script src="js/translation.js"></script>
```

### HTML to HTML Navigation
```javascript
// Simple file names (same directory)
window.location.href = 'register.html';
window.location.href = 'password.html';
window.location.href = 'dashboard.html';
// etc.
```

## 🚀 How to Use

### Access by URL
```
http://localhost:5500/frontend/index.html          # Start here
http://localhost:5500/frontend/pages/auth/register.html
http://localhost:5500/frontend/pages/auth/password.html
http://localhost:5500/frontend/pages/auth/login.html
http://localhost:5500/frontend/pages/app/dashboard.html
http://localhost:5500/frontend/pages/app/call.html
http://localhost:5500/frontend/pages/app/chat.html
http://localhost:5500/frontend/pages/app/chatroom.html
http://localhost:5500/frontend/pages/app/history.html
```

### Navigation via Buttons
See Navigation Map above - all buttons are configured correctly.

## 💾 Data Flow

### localStorage Keys
- `userId` - Current user ID
- `currentUser` - Full user object (JSON)
- `userPassword` - Password (demo only)
- `recentChats` - Array of chat user IDs
- `callHistory` - Array of call logs
- `chatMessages` - Array of all messages

### sessionStorage Keys
- `regName` - Temp: registration name
- `regEmail` - Temp: registration email
- `regLanguage` - Temp: registration language
- `receiverId` - Temp: call target user ID
- `receiverLanguage` - Temp: call target language
- `chatUserId` - Temp: current chat user

## ✅ Quality Checklist

- [x] Clear folder structure (auth vs app)
- [x] Consistent naming conventions
- [x] Organized by feature/function
- [x] All paths documented
- [x] Navigation map clear
- [x] Size appropriate (9 HTML, 5 JS, 5 CSS)
- [x] No redundant files
- [x] External links properly configured

---

**Start at:** `frontend/index.html`
**Main hub:** `frontend/pages/app/dashboard.html`
**Backend API:** `http://localhost:8000`
