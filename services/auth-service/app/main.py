from fastapi import FastAPI
from .schemas import UserCreate
from .hashing import Hash  

app = FastAPI(title="Auth Service", version="1.0.0")

@app.post("/api/auth/register")
def register(user: UserCreate):
    hashed_password = Hash.bcrypt(user.password)
    
    return {
        "message": "User registered successfully",
        "email": user.email,
        "hashed_password": hashed_password 
    }