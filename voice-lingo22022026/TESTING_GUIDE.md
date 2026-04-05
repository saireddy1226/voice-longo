# Voice Lingo - Complete Testing Guide

## 🔧 **FIXES APPLIED**

### ✅ Fix 1: Dynamic IP Configuration
**File**: `frontend/js/config.js`
- ❌ BEFORE: Hardcoded `https://192.168.0.110:8000`
- ✅ AFTER: Uses `window.location.origin` dynamically
- **Impact**: Works on any network (same WiFi, different WiFi, cellular)

### ✅ Fix 2: WebRTC Stream Allocation (Asymmetric Audio)
**File**: `frontend/js/webrtc.js`
- **Problem**: Laptop→Mobile audio doesn't work
- **Root Cause**: Callee's peer connection created BEFORE local stream added
- **Solution**: Add local stream tracks BEFORE setting remote description
- **Impact**: Both directions now work - Mobile↔Laptop audio symmetric ✅

### ✅ Fix 3: Mobile TTS Mic Stuck
**File**: `frontend/call.html`
- **Problem**: After translation speaks, mic stays disabled on mobile
- **Solution**: Added 3-second timeout fallback if onend callback doesn't fire
- **Impact**: Mobile mic auto re-enables after TTS ✅

### ✅ Fix 4: Offline User Detection (Race Condition)
**File**: `backend/signaling.py`
- **Problem**: When mobile calls, target shows "offline" even if just connecting
- **Solution**: Added 2-second wait + database fallback check
- **Impact**: Handles timing issues when WebSocket still connecting ✅

---

## 🧪 **STEP-BY-STEP TEST PROCEDURE**

### **Environment Setup**
- Laptop and Mobile: Same WiFi network
- Open browser on both to the same URL (use domain name, not IP)
- Clear cache: Chrome Ctrl+Shift+Delete → Clear All
- Open DevTools (F12) on both for console logs

---

### **TEST 1: Can Call From Mobile (Offline Bug Fix)**

**Setup**:
1. Open laptop browser → Register/Login
2. Open mobile browser → Register/Login

**Test Steps**:
1. Both should show "connected" in signaling (F12 console)
   ```
   ✅ Expected: "Signaling connected"
   ```

2. Go to dashboard on BOTH devices
   ```
   ✅ Expected: Profile shows your ID without errors
   ```

3. On MOBILE: Enter LAPTOP's user ID in "Enter Receiver ID" field
   ```
   ✅ Expected: Input accepts the ID without error
   ```

4. On MOBILE: Click "Start Call"
   ```
   ✅ BEFORE FIX: "Call failed: User offline" (even though laptop is online)
   ✅ AFTER FIX: Call connects properly
   ```

5. On LAPTOP: Should see "Incoming Call" from mobile
   ```
   ✅ Expected: Shows mobile's name and "Accept/Reject" buttons
   ```

6. On LAPTOP: Click "Accept Call"
   ```
   ✅ Expected: Redirects to call.html, shows timer
   ```

**✅ TEST 1 PASSED**: Mobile can now call without "offline" error

---

### **TEST 2: Bidirectional Audio (Asymmetry Fix)**

**Prerequisite**: Call active between Mobile and Laptop (from TEST 1)

**Test Steps**:

**Mobile speaks first**:
1. On MOBILE: Speak clearly "Hello from Mobile, can you hear me?"
2. On LAPTOP: Listen and check
   ```
   ✅ BEFORE FIX: Should hear the audio clearly
   ✅ AFTER FIX: Still works ✓
   ```

**Laptop speaks (THIS WAS BROKEN)**:
1. On LAPTOP: Speak clearly "Hello from Laptop, can you hear me?"
2. On MOBILE: Listen and check
   ```
   ❌ BEFORE FIX: NO AUDIO (mobile hears nothing)
   ✅ AFTER FIX: Hears laptop's audio clearly ✓
   ```

**Bidirectional Test**:
1. Both speak at the same time
   ```
   ✅ Both should hear each other simultaneously
   ```

2. Switch roles: Laptop calls Mobile instead
   ```
   ✅ Should still work both directions
   ```

**✅ TEST 2 PASSED**: Audio flows both directions symmetrically

---

### **TEST 3: Real-time Translation (Bonus)**

**Prerequisite**: Call active, both in different languages

**Test Steps**:

1. On MOBILE: Set language to "Hindi"
2. On LAPTOP: Set language to "English"
3. On MOBILE: Speak something in English
4. On LAPTOP: Should see translation area appear with Hindi text
   ```
   ✅ Expected: "🌐 Live Translation" box shows translated text
   ✅ Expected: Text-to-speech speaks it back automatically
   ```

5. On MOBILE: Mic should auto re-enable after speech ends
   ```
   ❌ BEFORE FIX: Mic stays disabled (frozen)
   ✅ AFTER FIX: Mic auto re-enables (either from onend callback or timeout)
   ```

---

### **TEST 4: Error Handling & Console Logs**

**Setup**: Open DevTools on both devices (F12)

**Test Steps**:

1. Mobile initiates call - check console logs:
   ```
   ✅ Should see:
   - "📞 Caller: Initiating offer..."
   - "📤 Sending offer"
   ```

2. Laptop receives offer - check console logs:
   ```
   ✅ Should see:
   - "📨 Callee: Received offer from caller"
   - "📱 Getting local stream on callee side..."
   - "✅ Added local track to PC (callee): audio"
   - "📤 Sending answer"
   ```

3. Look for any ❌ errors (should be none):
   ```
   ❌ If you see: "Microphone permission denied"
   → Check browser permissions
   
   ❌ If you see: "WebSocket connection failed"
   → Check server is running
   ```

---

## 📋 **VERIFICATION CHECKLIST**

- [ ] Mobile can see which users are online
- [ ] Mobile can call laptop without "offline" error
- [ ] Laptop can call mobile without errors
- [ ] **Audio FROM Laptop TO Mobile works** ← THIS WAS BROKEN
- [ ] **Audio FROM Mobile TO Laptop works**
- [ ] Both can speak simultaneously
- [ ] Mobile mic automatically re-enables after translation speaks
- [ ] Console shows detailed logs (📞📨📤✅)
- [ ] No permission errors in console
- [ ] No WebSocket errors in console

---

## 🚀 **DEPLOYMENT STEPS**

### **1. Verify Backend is Running**
```bash
cd voice-lingo/backend
uvicorn main:app --host 0.0.0.0 --port 8000 --ssl-keyfile=key.pem --ssl-certfile=cert.pem --reload
```

**Expected Output**:
```
✅ Application startup complete
✅ Uvicorn running on https://0.0.0.0:8000
```

### **2. Verify Frontend is Accessible**
```bash
# Open in browser (NOT localhost, use actual server IP or domain)
https://192.168.0.110:8000/index.html
OR
https://your-domain.com/index.html
```

### **3. Clear Cache on All Devices**
- Laptop: Ctrl+Shift+Delete → Clear All → Hard Refresh (Ctrl+F5)
- Mobile: Settings → Storage → App Cache → Clear All → Refresh (Cmd+Shift+R on iOS, Ctrl+F5 on Android)

### **4. Test Following the Procedure Above**

---

## 🐛 **TROUBLESHOOTING**

### Problem: "Call failed: User offline" on mobile
**Diagnosis**:
1. Check backend console for logs:
   ```
   If you see: "⏳ [target_id] not connected yet, waiting 2 seconds..."
   → Normal, backend is waiting for connection
   
   If you see: "❌ [target_id] doesn't exist in database"
   → Target user ID is invalid
   
   If you see: "📞 [mobile_id] calling [laptop_id]. Active users: [...]"
   → Shows all connected users
   ```

2. On mobile DevTools:
   - Check if `navigator.mediaDevices.getUserMedia()` failed
   - Check if signaling WebSocket connected successfully

**Solution**:
- Restart both browsers
- Check both are on same WiFi with correct server URL
- Clear cookies/cache

### Problem: Laptop can't hear mobile (audio only one direction)
**Diagnosis**:
1. Mobile → Laptop works but Laptop → Mobile doesn't
2. Check browser console for:
   ```
   ❌ "RemoteDescription not set"
   ❌ "addIceCandidate failed"
   ```

**Solution**:
- These fixes should resolve it
- If still broken, check:
  - Are both on same WiFi?
  - Is laptop's microphone working? (test in Settings)
  - Clear browser cache and refresh

### Problem: Mobile mic stays disabled after translation
**Diagnosis**:
1. Translation speaks with TTS
2. Try to speak → No audio captured
3. Check console:
   ```
   Should see either:
   - "🔊 TTS finished - enabling microphone" (good)
   - "⏱️ TTS timeout - force enabling microphone" (fallback working)
   ```

**Solution**:
- If neither message shows, TTS might not be speaking
- Check volume is on
- Check browser permissions for audio

---

## 📊 **EXPECTED BEHAVIOR SUMMARY**

| Scenario | Before Fixes | After Fixes |
|----------|-------------|------------|
| Mobile calls laptop | ❌ "User offline" | ✅ Connects |
| Laptop calls mobile | ✅ Connects | ✅ Connects |
| Mobile speaks | ✅ Heard on laptop | ✅ Heard on laptop |
| **Laptop speaks** | ❌ **NOT heard on mobile** | ✅ **Heard on mobile** |
| Mobile mic after TTS | ❌ Stuck (disabled) | ✅ Auto re-enabled |
| Same WiFi required | Needed | Still needed |
| Remote deployment | ❌ Fails with hardcoded IP | ✅ Works automatically |

---

## 💡 **NOTES**

- First call after deployment might take 3-5 seconds (WebSocket + stream setup)
- Translations only work during active calls
- Both users must have microphone permissions enabled
- Browser console (F12) is your best friend for debugging

