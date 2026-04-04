from fastapi import FastAPI, WebSocket, HTTPException, Body
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from signaling import signaling_socket
from translation import translation_socket

from database import (
    register_user,
    login_user,
    get_user_by_id,
    get_all_users,
    is_user_id_available,
    supabase
)

app = FastAPI()


# ---------------- CORS ----------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ---------------- MODELS ----------------

class LanguageUpdate(BaseModel):
    user_id: str
    language: str


# ---------------- ROOT ----------------

@app.get("/")
def root():
    return {"status": "VOICE-LINGO Backend Running"}


# ---------------- REGISTER ----------------

@app.post("/register")
async def register(data: dict = Body(...)):

    try:
        user_id = data.get("user_id")
        name = data.get("name")
        email = data.get("email")
        password = data.get("password")
        language = data.get("language", "English")

        if not user_id or not name or not email or not password:
            raise HTTPException(
                status_code=400,
                detail="user_id, name, email and password are required"
            )

        if len(password) < 8:
            raise HTTPException(
                status_code=400,
                detail="Password must be at least 8 characters"
            )

        user = register_user(user_id, name, email, password, language)

        if user is None:
            raise HTTPException(status_code=500, detail="Registration failed")

        if "error" in user:
            raise HTTPException(status_code=400, detail=user["error"])

        return {
            "success": True,
            "user_id": user["user_id"],
            "name": user["name"],
            "email": user["email"],
            "language": user["language"]
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ---------------- LOGIN ----------------

@app.post("/login")
async def login(data: dict = Body(...)):

    try:
        user_id = data.get("user_id")
        password = data.get("password")

        if not user_id or not password:
            raise HTTPException(
                status_code=400,
                detail="User ID and password required"
            )

        user = login_user(user_id, password)

        if user:
            return {
                "success": True,
                "user": {
                    "user_id": user["user_id"],
                    "name": user["name"],
                    "email": user["email"],
                    "language": user["language"]
                }
            }

        raise HTTPException(status_code=401, detail="Invalid credentials")

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ---------------- UPDATE LANGUAGE ----------------

@app.post("/update-language")
async def update_language(data: LanguageUpdate):

    try:
        supabase.table("users").update({
            "language": data.language
        }).eq("user_id", data.user_id).execute()

        return {"success": True}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ---------------- GET USER ----------------

@app.get("/users/{user_id}")
def get_user(user_id: str):

    try:
        user = get_user_by_id(user_id)

        if user:
            return {"success": True, "user": user}

        raise HTTPException(status_code=404, detail="User not found")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ---------------- LIST USERS ----------------

@app.get("/users-list")
def list_users():

    try:
        users = get_all_users()

        return {
            "success": True,
            "users": users
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ---------------- USER ID CHECK ----------------

@app.get("/check-userid/{user_id}")
def check_userid(user_id: str):

    try:
        available = is_user_id_available(user_id)

        return {
            "user_id": user_id,
            "available": available
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ---------------- WEBSOCKET SIGNALING ----------------

@app.websocket("/ws/signaling/{user_id}")
async def ws_signaling(websocket: WebSocket, user_id: str):
    await signaling_socket(websocket, user_id)


# ---------------- WEBSOCKET TRANSLATION ----------------

@app.websocket("/ws/translate/{user_id}")
async def ws_translation(websocket: WebSocket, user_id: str):
    await translation_socket(websocket, user_id)