# main.py

import os
from fastapi import FastAPI, Depends, HTTPException, UploadFile, File, Form
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv
import bcrypt
from typing import List, Optional
import datetime

# Optional libraries for resumes, AI, emails
# import pypdf2
# import docx
# import openai
# from sendgrid import SendGridAPIClient
# from sendgrid.helpers.mail import Mail
# from supabase import create_client

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

app = FastAPI(title="Job Platform API MVP")

# -----------------------------
# DATABASE CONNECTION
# -----------------------------
def get_db():
    conn = psycopg2.connect(DATABASE_URL, cursor_factory=RealDictCursor)
    try:
        yield conn
    finally:
        conn.close()

# -----------------------------
# AUTH (placeholder)
# -----------------------------
security = HTTPBearer()
def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    # For MVP, we'll just return a dummy user
    return {"user_id": 1, "role": "candidate", "email": "demo@example.com"}

# -----------------------------
# MODELS
# -----------------------------
class UserSignUp(BaseModel):
    email: str
    password: str
    role: str  # 'candidate', 'employer', 'admin'

class ProfileUpdate(BaseModel):
    headline: Optional[str]
    summary: Optional[str]
    location: Optional[str]
    salary_expectation: Optional[float]

class JobPost(BaseModel):
    title: str
    description: str
    location: Optional[str]
    salary_min: Optional[float]
    salary_max: Optional[float]
    remote_type: Optional[str] = 'on-site'
    seniority: Optional[str] = 'mid'

class Application(BaseModel):
    job_id: int
    message: Optional[str]

# -----------------------------
# ROUTES (Minimal MVP)
# -----------------------------

@app.get("/")
def home():
    return {"message": "Job Platform API is running!"}

@app.post("/signup")
def signup(user: UserSignUp):
    # Dummy hashing for MVP
    hashed = bcrypt.hashpw(user.password.encode(), bcrypt.gensalt())
    return {"message": f"User {user.email} created with role {user.role}", "hashed_password": hashed.decode()}

@app.post("/profile")
def update_profile(profile: ProfileUpdate, current_user=Depends(get_current_user)):
    return {"message": "Profile updated", "profile": profile.dict(), "user": current_user}

@app.post("/jobs")
def post_job(job: JobPost, current_user=Depends(get_current_user)):
    return {"message": "Job posted", "job": job.dict(), "posted_by": current_user}

@app.get("/jobs")
def list_jobs():
    return [{"job_id": 1, "title": "Backend Developer"}, {"job_id": 2, "title": "Frontend Developer"}]

@app.post("/apply")
def apply_job(application: Application, current_user=Depends(get_current_user)):
    return {"message": "Applied to job", "job_id": application.job_id, "candidate": current_user}

# -----------------------------
# RUN SERVER
# -----------------------------
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
