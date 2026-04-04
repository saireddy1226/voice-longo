from supabase import create_client
from config import SUPABASE_URL, SUPABASE_KEY
import uuid
from datetime import datetime
import bcrypt

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# Password Hashing
def hash_password(password):
    """Hash password using bcrypt"""
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode(), salt).decode()

def verify_password(password, password_hash):
    """Verify password against hash"""
    return bcrypt.checkpw(password.encode(), password_hash.encode())


# ================= USER MANAGEMENT =================

def register_user(user_id, name, email, password, language="English"):
    """
    Register a new user with user-provided user_id
    """
    try:
        # Check if email already exists
        existing_email = supabase.table("users").select("*").eq("email", email).execute()
        if existing_email.data:
            return {"error": "Email already registered"}

        # Check if user_id already exists
        existing_id = supabase.table("users").select("*").eq("user_id", user_id).execute()
        if existing_id.data:
            return {"error": "User ID already taken"}

        password_hash = hash_password(password)

        user_data = {
            "user_id": user_id,
            "name": name,
            "email": email,
            "password_hash": password_hash,
            "language": language,
            "online_status": False,
            "created_at": datetime.utcnow().isoformat()
        }

        result = supabase.table("users").insert(user_data).execute()

        return result.data[0] if result.data else None

    except Exception as e:
        print(f"Registration error: {e}")
        return None


def login_user(user_id, password):
    """Authenticate user by user_id and password"""
    try:

        res = supabase.table("users") \
            .select("*") \
            .eq("user_id", user_id) \
            .execute()

        if not res.data:
            return None

        user = res.data[0]

        if verify_password(password, user["password_hash"]):
            return user

        return None

    except Exception as e:
        print(f"Login error: {e}")
        return None

def get_user_by_id(user_id):
    """Get user information by user ID"""
    try:
        res = supabase.table("users").select("*").eq("user_id", user_id).execute()
        return res.data[0] if res.data else None
    except Exception as e:
        print(f"Error getting user: {e}")
        return None


def get_all_users():
    """Get all registered users"""
    try:
        res = supabase.table("users").select("user_id, name, email, online_status").execute()
        return res.data if res.data else []
    except Exception as e:
        print(f"Error getting users: {e}")
        return []


def set_user_online(user_id):
    """Mark user as online"""
    try:
        supabase.table("users").update(
            {"online_status": True}
        ).eq("user_id", user_id).execute()
    except Exception as e:
        print(f"Error setting user online: {e}")


def set_user_offline(user_id):
    """Mark user as offline"""
    try:
        supabase.table("users").update(
            {"online_status": False}
        ).eq("user_id", user_id).execute()
    except Exception as e:
        print(f"Error setting user offline: {e}")


def get_user_language(user_id):
    """Get user's preferred language for translation"""
    try:
        user = get_user_by_id(user_id)
        if user:
            return user.get("language", "English")
        return "English"
    except Exception as e:
        print(f"Error getting user language: {e}")
        return "English"


# ================= CALL HISTORY =================

def save_call_history(caller_id, callee_id, duration, status):
    """Save call history"""
    try:
        call_data = {
            "call_id": str(uuid.uuid4()),
            "caller_id": caller_id,
            "callee_id": callee_id,
            "duration": duration,
            "status": status,
            "timestamp": datetime.utcnow().isoformat()
        }

        supabase.table("call_history").insert(call_data).execute()

    except Exception as e:
        print(f"Error saving call history: {e}")
#-------------------user abalability check api-------------------
def is_user_id_available(user_id):
    """Check if a user_id already exists"""
    try:
        res = supabase.table("users").select("user_id").eq("user_id", user_id).execute()
        return len(res.data) == 0
    except Exception as e:
        print(f"Error checking user_id availability: {e}")
        return False