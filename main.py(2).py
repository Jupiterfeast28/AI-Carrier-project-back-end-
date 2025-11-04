from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from supabase import create_client
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# Create Supabase client
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# Initialize FastAPI
app = FastAPI()

# --------------------
# Schemas
# --------------------
class SignUpSchema(BaseModel):
    email: str
    password: str
    role: str  # 'candidate' or 'employer'

class SignInSchema(BaseModel):
    email: str
    password: str

# --------------------
# Routes
# --------------------
@app.post("/signup")
def signup(user: SignUpSchema):
    if user.role not in ["candidate", "employer"]:
        raise HTTPException(status_code=400, detail="Invalid role")
    
    # Create user in Supabase Auth
    result = supabase.auth.sign_up(
        {"email": user.email, "password": user.password}
    )
    
    # Add user to 'users' table with role
    if result.user:
        supabase.table("users").insert({"email": user.email, "role": user.role}).execute()
        return {"message": "User created successfully"}
    
    raise HTTPException(status_code=400, detail=result.error.message)

@app.post("/signin")
def signin(user: SignInSchema):
    result = supabase.auth.sign_in(
        {"email": user.email, "password": user.password}
    )
    if result.user:
        return {"access_token": result.session.access_token}
    
    raise HTTPException(status_code=400, detail=result.error.message)
