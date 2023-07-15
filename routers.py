from fastapi import APIRouter, Depends, Form, HTTPException, Request
from fastapi.templating import Jinja2Templates
from database import SessionLocal, User
from models import UserCreate
from sqlalchemy.orm import Session



router = APIRouter()
templates = Jinja2Templates(directory="templates")

def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/user/login")
async def login(request: Request, username: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == username, User.password == password).first()
    if not user:
        raise HTTPException(status_code=401, detail="Invalid username or password")
    return templates.TemplateResponse("items.html", {"request": request})

@router.post("/user/register")
async def register(user: UserCreate, db = Depends(get_db)):
    # Extract user data
    username = user.username
    password = user.password
    email = user.email
    
    # Check if the username already exists in the database
    if db.query(User).filter(User.username == username).first():
        raise HTTPException(status_code=400, detail="Username already exists")

    # Create a new user instance
    new_user = User(username=username, password=password, email=email)

    # Add the new user to the database session
    db.add(new_user)
    db.commit()
    
    return {"message": "User registered successfully"}