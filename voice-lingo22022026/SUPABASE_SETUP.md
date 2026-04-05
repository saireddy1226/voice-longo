# Supabase Database Setup for Voice-Lingo

## Step 1: Create a Supabase Project

1. Go to [https://supabase.com](https://supabase.com)
2. Sign up or log in to your account
3. Click **"New Project"**
4. Fill in the details:
   - **Project Name:** voice-lingo
   - **Database Password:** Create a strong password (save this securely!)
   - **Region:** Choose closest to your location
5. Click **"Create new project"** and wait for initialization (2-3 minutes)

## Step 2: Get Your API Keys

Once the project is ready:
1. Go to **Settings** → **API**
2. Copy the following:
   - **Project URL** (the `SUPABASE_URL`)
   - **anon public** key (the `SUPABASE_KEY`)
3. Save these values in your `.env` file:

```env
SUPABASE_URL=https://your-project-id.supabase.co
SUPABASE_KEY=your-anon-public-key
OPENAI_API_KEY=your-openrouter-api-key
```

## Step 3: Create Database Tables

Go to **SQL Editor** in Supabase and run the following SQL commands:

### Table 1: Users Table (for registration/login)

```sql
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

-- Create indexes for faster queries
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_user_id ON users(user_id);
```

### Table 2: Call History Table

```sql
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

-- Create index for faster lookups
CREATE INDEX idx_call_history_caller ON call_history(caller_id);
CREATE INDEX idx_call_history_callee ON call_history(callee_id);
```

### Table 3: Chat Messages Table (optional - for chat feature)

```sql
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

-- Create index for faster lookups
CREATE INDEX idx_chat_sender ON chat_messages(sender_id);
CREATE INDEX idx_chat_receiver ON chat_messages(receiver_id);
```

## Step 4: Database Schema Summary

| Table | Columns | Purpose |
|-------|---------|---------|
| `users` | user_id, name, email, password_hash, language, online_status, created_at, updated_at | Store user credentials and profile |
| `call_history` | call_id, caller_id, callee_id, duration, status, timestamp | Track all user calls |
| `chat_messages` | message_id, sender_id, receiver_id, message, timestamp | Store chat messages |

## Step 5: Enable Row Level Security (Optional but Recommended)

For better security, enable RLS:

1. Go to **Authentication** → **Policies**
2. For each table, click **Enable RLS**
3. This ensures users can only access their own data

## Step 6: Test the Connection

After setting up tables, the backend will automatically:
- ✅ Hash passwords using bcrypt
- ✅ Store user credentials securely
- ✅ Authenticate users on login
- ✅ Track call history
- ✅ Store chat messages

## Troubleshooting

**Issue:** "Connection refused" error
- Check that SUPABASE_URL and SUPABASE_KEY are correct in `.env`
- Make sure your Supabase project is active

**Issue:** "Table doesn't exist" error
- Run the SQL commands above in Supabase SQL Editor
- Make sure all tables are created successfully

**Issue:** Foreign key constraint error
- Ensure `users` table exists before creating `call_history` and `chat_messages`
- Check that column names match exactly

## Data Flow

```
Frontend (registration form)
    ↓ sends name, email, password
Backend (REST API /register)
    ↓ hashes password with bcrypt
    ↓ creates unique UUID
Supabase Database
    ↓ stores user_id, name, email, password_hash
Frontend (login form)
    ↓ sends email, password
Backend (REST API /login)
    ↓ retrieves user from database
    ↓ verifies password with bcrypt
    ↓ returns user_id if successful
```

## Next Steps

1. Create the `.env` file with your Supabase keys
2. Install required Python packages: `pip install -r requirements.txt`
3. Run the backend: `python main.py`
4. Test registration and login with the frontend
