from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import RedirectResponse
from passlib.context import CryptContext
import sqlite3

app = FastAPI()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

@app.post("/login")
async def login(request: Request):
    data = await request.json()
    username = data.get("username")
    password = data.get("password")
    try: 
        conn = sqlite3.connect("./databases/dashboard.db")
        cursor = conn.cursor()
        cursor.execute("SELECT password_hash FROM users WHERE username = ?", (username,))
        user = cursor.fetchone()
        conn.close()
    except Exception as e:
        print(e)

    if user and verify_password(password, user[0]):
        return {"message": "Login successful"}, 200
    else:
        raise HTTPException(status_code=401, detail="Invalid credentials")

@app.get("/dashboard")
async def dashboard():
    return {"message": "Welcome to the Dashboard"}

@app.get("/")
async def root():
    return RedirectResponse(url="/index.html")


