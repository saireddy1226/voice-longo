from fastapi import WebSocket, WebSocketDisconnect
from database import set_user_online, set_user_offline, get_user_by_id, save_call_history
from datetime import datetime

active_users = {}
call_requests = {}

async def safe_send(ws, data):
    try:
        await ws.send_json(data)
    except Exception as e:
        print(f"❌ safe_send failed: {e}")

async def signaling_socket(websocket: WebSocket, user_id: str):
    await websocket.accept()

    existing = active_users.get(user_id, {})
    active_users[user_id] = {
        "websocket": websocket,
        "connected_to": existing.get("connected_to", None),
        "call_start": existing.get("call_start", None)
    }

    print(f"✅ {user_id} connected. Active: {list(active_users.keys())}")
    set_user_online(user_id)

    try:
        await safe_send(websocket, {"type": "connected", "user_id": user_id})

        if active_users[user_id]["connected_to"]:
            await safe_send(websocket, {
                "type": "call_active",
                "connected_to": active_users[user_id]["connected_to"]
            })

        while True:
            data = await websocket.receive_json()
            msg_type = data.get("type")

            if msg_type == "call_request":
                target_id = data.get("target_id")
                if not target_id:
                    continue

                print(f"📞 {user_id} → {target_id}. Active: {list(active_users.keys())}")

                # ✅ no asyncio.sleep — immediate check
                if target_id not in active_users:
                    await safe_send(websocket, {
                        "type": "call_failed",
                        "reason": "User offline"
                    })
                    continue

                caller = get_user_by_id(user_id)
                call_requests[target_id] = user_id

                await safe_send(active_users[target_id]["websocket"], {
                    "type": "incoming_call",
                    "caller_id": user_id,
                    "caller_name": caller["name"],
                    "caller_language": caller.get("language", "English")
                })

                await safe_send(websocket, {
                    "type": "call_ringing",
                    "target_id": target_id
                })

            elif msg_type == "call_accept":
                caller_id = call_requests.get(user_id)
                if not caller_id or caller_id not in active_users:
                    continue

                active_users[user_id]["connected_to"] = caller_id
                active_users[caller_id]["connected_to"] = user_id

                now = datetime.utcnow()
                active_users[user_id]["call_start"] = now
                active_users[caller_id]["call_start"] = now

                print(f"📞 Call accepted: {user_id} ↔ {caller_id}")

                await safe_send(active_users[caller_id]["websocket"], {
                    "type": "call_accepted",
                    "callee_id": user_id
                })

                await safe_send(websocket, {
                    "type": "call_confirmed",
                    "caller_id": caller_id
                })

                if user_id in call_requests:
                    del call_requests[user_id]

            elif msg_type == "restore_call":
                connected_to = data.get("connected_to")
                if connected_to and connected_to in active_users:
                    active_users[user_id]["connected_to"] = connected_to
                    if not active_users[user_id]["call_start"]:
                        active_users[user_id]["call_start"] = datetime.utcnow()
                    print(f"🔁 Restored: {user_id} ↔ {connected_to}")
                else:
                    print(f"⚠️ Could not restore: {user_id} → {connected_to}")

            elif msg_type == "call_reject":
                caller_id = call_requests.get(user_id)
                if caller_id and caller_id in active_users:
                    await safe_send(active_users[caller_id]["websocket"], {
                        "type": "call_rejected",
                        "callee_id": user_id
                    })
                if user_id in call_requests:
                    del call_requests[user_id]

            elif msg_type in ["offer", "answer", "ice_candidate"]:
                target_id = active_users[user_id]["connected_to"]
                if target_id and target_id in active_users:
                    data["from_id"] = user_id
                    await safe_send(active_users[target_id]["websocket"], data)

            elif msg_type == "end_call":
                target_id = active_users[user_id]["connected_to"]
                print(f"🔴 END CALL: {user_id} → {target_id}")

                if target_id and target_id in active_users:
                    call_start = active_users[user_id]["call_start"]
                    if call_start:
                        duration = int((datetime.utcnow() - call_start).total_seconds())
                        save_call_history(user_id, target_id, duration, "completed")

                    await safe_send(active_users[target_id]["websocket"], {"type": "call_ended"})
                    print(f"✅ call_ended sent to {target_id}")

                    active_users[target_id]["connected_to"] = None
                    active_users[target_id]["call_start"] = None

                active_users[user_id]["connected_to"] = None
                active_users[user_id]["call_start"] = None
                await safe_send(websocket, {"type": "call_closed"})

    except WebSocketDisconnect:
        print(f"🔌 {user_id} disconnected")

    finally:
        if user_id in active_users:
            target_id = active_users[user_id]["connected_to"]
            if target_id and target_id in active_users:
                await safe_send(active_users[target_id]["websocket"], {
                    "type": "call_ended",
                    "reason": "user_disconnected"
                })
                active_users[target_id]["connected_to"] = None
                active_users[target_id]["call_start"] = None
            del active_users[user_id]

        if user_id in call_requests:
            del call_requests[user_id]

        set_user_offline(user_id)
        print(f"👋 {user_id} removed. Active: {list(active_users.keys())}")