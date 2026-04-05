# Voice-Lingo Database Setup Checklist

## ✅ What We've Updated

1. **Backend Changes:**
   - ✅ Updated `database.py` - Added password hashing with bcrypt
   - ✅ Updated `main.py` - Added `/login` endpoint for authentication
   - ✅ Updated `requirements.txt` - Added bcrypt dependency

2. **Frontend Changes:**
   - ✅ Updated `auth.js` - Updated register() to accept password, updated login() to use email/password
   - ✅ Updated `password.html` - Now sends password to backend during registration
   - ✅ Updated `login.html` - Changed from User ID to Email login
   - ✅ Updated `register.html` - Unchanged (still collects name, email, language)

3. **Documentation:**
   - ✅ Created `SUPABASE_SETUP.md` - Complete Supabase setup guide

---

## 🚀 Steps to Get Everything Working

### Step 1: Set Up Supabase (5 minutes)
1. Go to [https://supabase.com](https://supabase.com)
2. Create a new project called `voice-lingo`
3. Once ready, go to **Settings → API** and copy:
   - **Project URL** → `SUPABASE_URL`  
   - **anon public** key → `SUPABASE_KEY`

### Step 2: Create Database Tables (2 minutes)
1. In Supabase, go to **SQL Editor**
2. Copy-paste the SQL commands from `SUPABASE_SETUP.md` (all three tables)
3. Run each SQL command

**Quick SQL Summary:**
```sql
-- Table 1: Users (with password_hash)
CREATE TABLE users (
  id BIGINT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
  user_id TEXT UNIQUE NOT NULL,
  name TEXT NOT NULL,
  email TEXT UNIQUE NOT NULL,
  password_hash TEXT NOT NULL,
  language TEXT DEFAULT 'English',
  online_status BOOLEAN DEFAULT false,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now())
);
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_user_id ON users(user_id);

-- Table 2: Call History  
CREATE TABLE call_history (
  id BIGINT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
  call_id TEXT UNIQUE NOT NULL,
  caller_id TEXT NOT NULL,
  callee_id TEXT NOT NULL,
  duration INTEGER,
  status TEXT,
  timestamp TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()),
  FOREIGN KEY (caller_id) REFERENCES users(user_id),
  FOREIGN KEY (callee_id) REFERENCES users(user_id)
);
CREATE INDEX idx_call_history_caller ON call_history(caller_id);
CREATE INDEX idx_call_history_callee ON call_history(callee_id);

-- Table 3: Chat Messages (optional)
CREATE TABLE chat_messages (
  id BIGINT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
  message_id TEXT UNIQUE NOT NULL,
  sender_id TEXT NOT NULL,
  receiver_id TEXT NOT NULL,
  message TEXT NOT NULL,
  timestamp TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()),
  FOREIGN KEY (sender_id) REFERENCES users(user_id),
  FOREIGN KEY (receiver_id) REFERENCES users(user_id)
);
CREATE INDEX idx_chat_sender ON chat_messages(sender_id);
CREATE INDEX idx_chat_receiver ON chat_messages(receiver_id);
```

### Step 3: Create `.env` File (1 minute)
Create a `.env` file in the `backend/` directory:
```env
SUPABASE_URL=https://xxxx.supabase.co
SUPABASE_KEY=your-anon-public-key
OPENAI_API_KEY=your-openrouter-api-key
```

### Step 4: Install Dependencies (2 minutes)
```bash
cd backend
pip install -r requirements.txt
```

### Step 5: Test the Backend
```bash
cd backend
python main.py
```

You should see:
```
INFO:     Uvicorn running on http://127.0.0.1:8000
```

### Step 6: Test Registration & Login

**In your browser:**

1. **Open frontend:** `frontend/index.html`
2. **Click "Get Started"** → Register
3. **Fill registration form:**
   - Name: "John Doe"
   - Email: "john@example.com"
   - Language: "English"
   - Click **Continue**
4. **Create Password:**
   - Password: `SecurePass123!` (must have: 8+ chars, 1 digit, 1 special char)
   - Confirm: `SecurePass123!`
   - Click **Register**
5. **You should see:**
   - ✅ Success message with User ID
   - ✅ Auto-redirect to dashboard in 3 seconds

### Step 7: Test Login

1. **Go back to index.html** or logout
2. **Click "Login"**
3. **Enter credentials:**
   - Email: `john@example.com`
   - Password: `SecurePass123!`
   - Click **Login**
4. **You should see:**
   - ✅ Success message
   - ✅ Auto-redirect to dashboard

---

## 📊 What's Now Stored in Supabase

When you register, the following is saved to the database:

```
Table: users
├── user_id: "550e8400-e29b-41d4-a716-446655440000" (UUID)
├── name: "John Doe"
├── email: "john@example.com"
├── password_hash: "$2b$12$jK7g9..." (bcrypt hashed)
├── language: "English"
├── online_status: false
└── created_at: "2025-03-06T14:32:10.123456"
```

---

## 🔒 Security Notes

- **Password Hashing:** Passwords are hashed using bcrypt (industry standard)
- **No Plain Text:** Passwords are NEVER stored in plain text
- **Database Indexes:** Email and user_id are indexed for fast lookups
- **Foreign Keys:** Call history and chat messages are linked to users

---

## 🧪 Testing with curl (Optional)

### Register a user:
```bash
curl -X POST http://localhost:8000/register \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Jane Doe",
    "email": "jane@example.com",
    "password": "TestPass123!",
    "language": "Hindi"
  }'
```

### Login with email and password:
```bash
curl -X POST http://localhost:8000/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "jane@example.com",
    "password": "TestPass123!"
  }'
```

---

## 🐛 Troubleshooting

| Problem | Solution |
|---------|----------|
| "Connection refused" | Check `.env` file - make sure SUPABASE_URL and SUPABASE_KEY are correct |
| "Table doesn't exist" | Run the SQL commands in Supabase SQL Editor to create tables |
| "Email already registered" | That email is already in database - use a different one |
| "Invalid email or password" | Check your email/password - they're case-sensitive |
| "ModuleNotFoundError: bcrypt" | Run `pip install bcrypt` or `pip install -r requirements.txt` |

---

## ✨ Next Steps

After testing registration/login:
- Test calling functionality (WebRTC)
- Test translation feature
- Test chat functionality
- Test call history storage

All of these will now properly store user data in Supabase!
