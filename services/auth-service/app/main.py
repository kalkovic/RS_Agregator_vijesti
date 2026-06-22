from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from .schemas import UserCreate, UserLogin
from .hashing import Hash
from .security import create_access_token, get_current_user, require_admin
from .database import create_users_table, get_users_table

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_users_table()
    yield

app = FastAPI(title="Auth Service", version="1.0.0", lifespan=lifespan)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/api/auth/register")
def register(user: UserCreate):
    table = get_users_table()
    
    response = table.get_item(Key={'email': user.email})
    if 'Item' in response:
        raise HTTPException(status_code=400, detail="Email already registered")
        
    hashed_password = Hash.bcrypt(user.password)
    
    table.put_item(
        Item={
            "email": user.email, 
            "hashed_password": hashed_password, 
            "role": "admin" 
        }
    )
    
    return {"message": "User registered successfully", "email": user.email}


@app.post("/api/auth/login")
def login(user: UserLogin):
    table = get_users_table()
    
    response = table.get_item(Key={'email': user.email})
    if 'Item' not in response:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    db_user = response['Item']
    
    if not Hash.verify(user.password, db_user["hashed_password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    access_token = create_access_token(
        data={"sub": user.email, "role": db_user["role"]}
    )
    
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/api/auth/me")
def get_me(current_user: dict = Depends(get_current_user)):
    return {
        "message": "Uspješno si pristupio zaštićenoj ruti!",
        "user_details": current_user
    }

@app.get("/api/auth/admin")
def admin_only_route(current_user: dict = Depends(require_admin)):
    return {
        "message": "Dobrodošao u VIP ložu! Ovo vide samo admini.",
        "admin_details": current_user
    }