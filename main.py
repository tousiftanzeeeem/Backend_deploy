from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
from datetime import datetime
from sqlalchemy.orm import Session
import os
from dotenv import load_dotenv

from database import get_db, init_db, UserDB

load_dotenv()

app = FastAPI()

# Configure CORS
cors_origins = os.getenv("CORS_ORIGINS", "http://localhost:3000").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models
class UserCreate(BaseModel):
    name: str
    email: str

class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    created_at: datetime

    class Config:
        from_attributes = True

# Initialize database on startup
@app.on_event("startup")
def startup_event():
    init_db()

# Basic health check endpoint
@app.get("/health")
def health_check():
    return {"status": "healthy"}

@app.get("/")
def read_root():
    return {"message": "Welcome to User Management API"}

@app.get("/api/users", response_model=List[UserResponse])
def get_users(db: Session = Depends(get_db)):
    """Get all users"""
    users = db.query(UserDB).all()
    return users

@app.post("/api/users", response_model=UserResponse)
def add_user(user: UserCreate, db: Session = Depends(get_db)):
    """Add a new user"""
    
    # Check if email already exists
    existing_user = db.query(UserDB).filter(UserDB.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already exists")
    
    new_user = UserDB(name=user.name, email=user.email)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return new_user

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
