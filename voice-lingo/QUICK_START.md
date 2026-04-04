# 🚀 Quick Start - Testing Your Voice-Lingo App

## Step 1: Setup Backend (5 minutes)

### 1.1 Navigate to backend folder
```bash
cd backend
```

### 1.2 Create `.env` file
Create a file named `.env` in the backend folder with:
```
SUPABASE_URL=your_supabase_project_url
SUPABASE_KEY=your_supabase_anon_key
GROQ_API_KEY=your_groq_api_key
```

**Need these credentials?**
- Supabase: https://supabase.com (Create free project)
- Groq: https://console.groq.com (Get free API key with generous rate limits)

### 1.3 Install Python dependencies
```bash
python -m venv venv
venv\Scripts\activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 1.4 Start the backend server
```bash
uvicorn main:app --reload
```

You should see:
```
Uvicorn running on http://127.0.0.1:8000
```

✅ **Backend is ready!**

---

## Step 2: Test Frontend in Browser

### 2.1 Open frontend in browser
Navigate to the `frontend/` directory and open `index.html` in your browser

Or drag `index.html` into your browser window

### 2.2 Watch the Splash Screen
- App loads with "VOICE LINGO" splash
- Message: "AI Powered Real Time Voice Translation System"
- Auto-closes after 2-3 seconds
- Welcome page with Register/Login buttons appears

### 2.3 Test Registration (First User)
1. Click **"Register"**
2. Enter details:
   - Name: `Alice`
   - Email: `alice@test.com`
   - Language: `English`
3. Click **"Continue"**
4. Create password:
   - Password: `SecurePass123!`
   - Confirm: `SecurePass123!`
5. Click **"Register"**
6. See success message with **User ID** (copy this!)
7. Auto-redirects to Dashboard

✅ **First user registered!**

### 2.4 Get User ID
When you see: **"Registration successful! Your User ID: abc123-def456..."**

**Copy this User ID** - you'll need it for testing calls

### 2.5 Open New Browser Window/Tab (For Second User)
Repeat registration with:
- Name: `Bob`
- Email: `bob@test.com`
- Language: `Spanish`
- Password: `SecurePass456!`

**Copy Bob's User ID too!**

---

## Step 3: Test Calling

### 3.1 Switch back to Alice's window
You should see Dashboard with:
- Header: "VOICE LINGO" + Profile Icon
- Input field: "Enter Receiver ID"
- Green "Start Call" button

### 3.2 Paste Bob's User ID
In the input field, paste: **bob's user id (from step 2.5)**

### 3.3 Click "Start Call"
Alice's status: "Calling..."

### 3.4 Watch Bob's Window
Bob should see:
```
📞 Incoming Call
Alice is calling you...

[Accept] [Reject]
```

### 3.5 Bob Clicks "Accept"
- Call connects
- Browser asks for **microphone permission** → Click **"Allow"**
- Status shows: "Call connected"
- Translation card appears

### 3.6 Test Speaking
- Alice says something in English
- Bob hears it and sees translation in Spanish
- Bob responds in Spanish
- Alice sees Spanish translation of Bob's words

✅ **Live translation working!**

### 3.7 Test Language Change (Optional)
1. Click **profile icon** (👤) in Alice's header
2. Click **"Language"** dropdown
3. Select different language
4. Conversation continues with new language preference

### 3.8 End Call
Click **red "End Call"** button

Status shows: `"Call ended. Duration: X minutes Y seconds"`

✅ **Full call cycle complete!**

---

## Troubleshooting

### Issue: Backend won't start
**Solution:**
```bash
pip install -r requirements.txt --upgrade
uvicorn main:app --reload
```

### Issue: "Port already in use"
**Solution:**
```bash
uvicorn main:app --reload --port 8001
```
(Then update frontend WebSocket URL if needed)

### Issue: "Microphone access denied"
**Solution:**
- Check browser permissions
- Allow microphone access when prompted
- Restart browser if needed

### Issue: "Can't register - email already exists"
**Solution:**
Use different email addresses:
- alice@test.com
- bob@test.com
- etc.

### Issue: No translation appearing
**Solution:**
1. Check OpenRouter API key is valid
2. Verify Supabase credentials in .env
3. Check browser console for errors (F12)
4. Allow microphone access

### Issue: "Call not connecting"
**Possible causes:**
1. Check both users are registered
2. Both must have dashboard open
3. Backend must be running
4. CORS must be enabled
5. Different browser windows/tabs recommended

---

## Quick Test Scenario (5 minutes)

1. **Start Backend** (30 seconds)
   ```bash
   cd backend
   uvicorn main:app --reload
   ```

2. **Open Frontend** (10 seconds)
   - Browser 1: index.html
   - Browser 2: index.html

3. **Register Two Users** (2 minutes)
   - Browser 1: Register Alice
   - Copy Alice's User ID
   - Browser 2: Register Bob
   - Copy Bob's User ID

4. **Test Call** (2 minutes)
   - Browser 1: Paste Bob's ID → Click Call
   - Browser 2: See alert → Click Accept
   - Both see "Call connected"
   - Allow microphone access
   - Speak and see translations

5. **End Call** (10 seconds)
   - Either click "End Call"
   - See call duration

**Total: ~5 minutes for complete test!**

---

## Features to Test

✅ Registration flow (2-step)
✅ Login with User ID
✅ Unique User ID generation
✅ Password validation
✅ Call initiation
✅ Incoming call alert
✅ Accept/Reject calls
✅ Real-time translation
✅ Call duration
✅ End call
✅ Logout
✅ Language change

---

## Next Steps After Testing

1. ✅ All tests pass → Ready for production setup
2. Need more features? → Add Chat & History pages
3. Want mobile version? → Need HTTPS + mobile framework
4. Scale up? → Deploy backend to server
5. Production deployment:
   - Move to HTTPS
   - Use real database backups
   - Add rate limiting
   - Configure CORS for production domain
   - Use secure password hashing

---

## Contact & Support

If anything doesn't work:
1. Check the error message in browser console (F12)
2. Verify .env file has correct credentials
3. Ensure backend is running on port 8000
4. Check that microphone is allowed

---

## 🎉 You're All Set!

Everything is ready to test. Start the backend, open the frontend, and enjoy your Voice-Lingo application!

**Happy Testing!** 🚀
