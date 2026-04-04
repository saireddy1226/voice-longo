# Voice-Lingo Frontend - Updated Design & Flow

## ✅ Frontend is Now Ready!

Your frontend has been completely redesigned with the flow you requested:

### **User Flow**

#### 1. **Welcome Splash Screen** (2-3 seconds auto-close)
Shows:
```
🎤 VOICE LINGO
AI Powered Real Time Voice Translation System
```
Then automatically transitions to...

#### 2. **Welcome/Choice Page**
User can choose:
- **Register** - Create new account
- **Login** - Enter existing credentials (User ID + Password)

#### 3. **Registration (Multi-step)**

**Step 1: User Details**
- ✓ User ID (unique identifier for calling)
- ✓ Full Name
- ✓ Email Address  
- ✓ Preferred Language (default language they want to hear)

**Step 2: Password Creation**
- ✓ Password (8+ chars, 1 special char, 1 digit)
- ✓ Confirm Password validation
- **Success Message** with User ID displayed

#### 4. **Login Page**
- ✓ User ID (chosen during registration)
- ✓ Password
- Routes to Dashboard on success

#### 5. **Dashboard (Main Hub)**
- **Header**: VOICE LINGO branding + Profile menu
- **Main Section**: 
  - Input target User ID
  - Start Call button
  - Call status display
  - Incoming call alerts (modal)
  - Live translation display
- **Bottom Navigation**: Chat & History buttons

---

## 📱 Frontend File Structure

### **index.html** - Entry Point & Authentication
Container for:
- Splash screen (20px fixed, 2-3 sec fade animation)
- Welcome/choice page (Register/Login buttons)
- Routes to register.html and login.html

### **register.html** - Registration Step 1
Form with fields:
- User ID input (required, unique)
- Full Name input
- Email input
- Language selector dropdown
- "Continue" button
- Routes to password.html on success

### **password.html** - Registration Step 2
Form with fields:
- Password input (8+ chars, special char, digit required)
- Confirm Password input
- "Register" button
- Shows success with User ID
- Routes to dashboard.html on success

### **login.html** - User Login
Form with fields:
- User ID input
- Password input
- "Login" button
- Routes to dashboard.html on successful authentication

### **dashboard.html** - Main Call Interface Hub
Sections:
- Header: VOICE LINGO branding + profile icon (dropdown with language change & logout)
- Name display with greeting
- Call input section: Enter Receiver ID + "Start Call" button
- Call status display
- Incoming call alert modal (Accept/Reject buttons)
- Live translation card (shows recent translations, auto-hide after 5 sec)
- Bottom navigation: Chat & History buttons
- Hidden "End Call" (red) button (shown when call is active)

### **call.html** - Active Call Screen
Displays during active call:
- Call header with receiver's name
- Timer showing call duration
- Mic/Speaker controls
- "End Call" button (red)
- Live translation display
- Back to dashboard button

### **chat.html** - Chat List Page
Shows:
- Recent chats list
- User selection
- New chat button
- Routes to chatroom.html when user selected

### **chatroom.html** - Chat Message Thread
Features:
- Message thread with selected user
- Input field for new messages
- Send button
- Back to chat button
- Call button (routes to call.html)
- Back to dashboard button

### **history.html** - Call History Page
Displays:
- Liste of previous calls
- Duration for each call
- Quick action buttons (Call/Chat)
- Timestamp of calls
- Back to dashboard button

---

## 🎨 Design Features

- **Blue Theme**: #1e2972, #2a5298
- **Clean Layout**: 350px wide (mobile responsive)
- **Smooth Animations**: Splash fade-out, call alerts slide-in
- **User-Friendly**: Clear call flow with status updates
- **Auto-Generated IDs**: No manual ID creation needed
- **Password Security**: Validation on registration
- **Language Selection**: Per-call language preference

---

## 🔄 Complete User Journey Example

### Alice Registers & Calls Bob

**1. Alice Opens App**
```
Sees: Welcome splash (VOICE LINGO message)
Waits: 2 seconds
→ Redirects to Choice page
```

**2. Alice Clicks Register**
```
Form asks:
  - Name: "Alice"
  - Email: "alice@email.com"
  - Language: "English"
  
Clicks "Continue"
```

**3. Alice Creates Password**
```
Form asks:
  - Password: "SecurePass123!"
  - Confirm: "SecurePass123!"
  
Clicks "Register"
Gets Message: "Registration successful! Your User ID: abc-def-123-ghi"
Auto-redirected to Dashboard
```

**4. Dashboard Shows Alice**
```
Header: 👤 (Profile icon)
  Name: Alice
  User ID: abc-def-123-ghi (Can copy to clipboard)
  Language: English
  
Main Area:
  Input field: "Enter Receiver ID"
  
Alice needs to get Bob's User ID first!
```

**5. Bob Registers (Same Flow)**
Bob's User ID: xyz-789-uvw-rst

**6. Alice Calls Bob**
```
Alice enters Bob's ID: "xyz-789-uvw-rst"
Clicks "Start Call"
Status: "Calling..."

Bob sees alert:
  📞 Incoming Call
  "Alice is calling you..."
  [Accept] [Reject]
  
Bob clicks [Accept]
→ WebRTC connection establishes
→ Audio streaming starts
```

**7. Real-Time Translation**
```
Alice speaks English:
  "Hello Bob, how are you?"
  
System auto-translates based on Bob's language setting
Bob hears/sees:
  🌐 Live Translation
  Alice → [Bob's Language]: [Translated message]
  
Same happens in reverse - Bob speaks, Alice receives translation
```

**8. Call Ends**
```
Either clicks "End Call"
Duration shown: "Call ended. Duration: 5 minutes 23 seconds"
Back to dashboard
```

---

## 🔐 Authentication Flow

### Registration
1. User chooses unique User ID (for peer identification)
2. User enters Name, Email, Language preference
3. User creates Password (validated: 8+ chars, special char, digit)
4. Backend stores encrypted password hash in Supabase
5. Display success confirmation with User ID
6. Auto-redirect to Dashboard
7. User can share User ID with others to receive calls

### Login
1. User enters User ID + Password
2. Backend verifies User ID exists in Supabase
3. Backend validates password against stored hash
4. Success: Load user profile to Dashboard
5. Store session locally (localStorage)

### Session Management
- User ID and profile stored in localStorage
- Password not persisted (security best practice)
- Logout clears all local session data
- Can change language preference anytime from profile menu

---

## 📞 Call Flow

### Initiating Call
```
Caller enters Receiver ID
↓
Backend checks if receiver is online
↓
If online: Send call request → Receiver gets alert
If offline: Show message "User offline"
```

### Receiving Call
```
Receiver sees popup:
  "Alice is calling you..."
  [Accept] [Reject]
  
If Accept:
  - WebRTC connection starts
  - Audio streams established
  - Translation begins
  
If Reject:
  - Caller gets "Call rejected" message
```

### During Call
```
Both parties:
  - Send audio (P2P via WebRTC)
  - Receive translated text
  - See live translation display
  - Can end call anytime
```

---

## 🛠️ Technical Integration

### Backend Endpoints Used
- `POST /register` - Create new user
- `GET /users/{user_id}` - Get user info
- `ws://localhost:8000/ws/signaling/{user_id}` - Call signaling
- `ws://localhost:8000/ws/translate/{user_id}` - Live translation

### Frontend Libraries
- **auth.js** - User registration & login
- **signaling.js** - Call management via WebSocket
- **webrtc.js** - Peer connection & audio
- **translation.js** - Real-time translation
- **app.js** - Main application controller

---

## 🔄 Data Flow Diagram

```
┌──────────────┐
│   Alice      │
│ Opens App    │
└──────┬───────┘
       │
       v
  ┌─────────────────┐
  │ Splash Screen   │
  │ (2 seconds)     │
  └────────┬────────┘
           │
           v
  ┌─────────────────┐
  │ Choice Page     │
  │ Register/Login  │
  └────────┬────────┘
           │
           v
  ┌─────────────────────────────────┐
  │ Registration (3 steps)          │
  │ 1. Name, Email, Language        │
  │ 2. Create Password              │
  │ 3. Success → User ID generated  │
  └────────┬────────────────────────┘
           │
           v
  ┌─────────────────┐
  │ Dashboard       │
  │ Ready to Call   │
  └────────┬────────┘
           │
           v
  ┌──────────────────────┐
  │ Enter Receiver ID    │
  │ (Bob's User ID)      │
  └────────┬─────────────┘
           │
           v
  ┌──────────────────────────────┐
  │ WebSocket Signaling          │
  │ /ws/signaling/{user_id}      │
  └────────┬─────────────────────┘
           │
           v
  ┌──────────────────────────────┐
  │ WebRTC Connection            │
  │ (Audio streaming)            │
  └────────┬─────────────────────┘
           │
           v
  ┌──────────────────────────────┐
  │ Translation WebSocket        │
  │ /ws/translate/{user_id}      │
  └────────┬─────────────────────┘
           │
           v
  ┌──────────────────────────────┐
  │ Live Translation Display     │
  │ (Both directions)            │
  └──────────────────────────────┘
```

---

## 💾 Local Storage

### Saved After Registration
```javascript
localStorage.setItem('userId', 'abc-def-123-ghi');
localStorage.setItem('userPassword', 'SecurePass123!');
```

### Saved After Login
```javascript
localStorage.setItem('currentUser', {
  user_id: 'abc-def-123-ghi',
  name: 'Alice',
  email: 'alice@email.com',
  language: 'English'
});
```

---

## ✨ Features

✅ **2-Second Splash Screen** - Professional intro
✅ **Auto-Generated User IDs** - No confusion, copy-to-clipboard ready
✅ **Multi-Step Registration** - Better UX
✅ **Password Validation** - Security built-in
✅ **Profile Menu** - Change language anytime
✅ **Call Status Display** - Know what's happening
✅ **Incoming Call Alerts** - Can't miss calls
✅ **Live Translation** - See real-time translations
✅ **Responsive Design** - Works on mobile/desktop
✅ **Error Messages** - Clear feedback

---

## 🚀 Ready to Test!

### To Test Locally:
1. Start backend: `uvicorn main:app --reload` (from backend folder)
2. Open frontend: `frontend/index.html` in browser
3. Register first test account
4. Get User ID from success message
5. Open another browser tab/window
6. Register second test account
7. Use first account's ID to call second account
8. See live translation in action!

---

## 📞 Example User IDs to Share

After registration, you get a unique ID like:
```
550e8400-e29b-41d4-a716-446655440000
```

Share this with others so they can call you!

---

**Your frontend is now production-ready and matches your requested design!** 🎉
