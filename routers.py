from fastapi import APIRouter, Depends, Form, HTTPException, Request
from fastapi.templating import Jinja2Templates
from database import SessionLocal, User,Item,OrderedItem
from models import UserCreate
from sqlalchemy.orm import Session
from typing import List





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

    items = db.query(Item).all()  # Fetch items from the database

    return templates.TemplateResponse("items.html", {"request": request, "items": items})

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

@router.post("/add_items")
async def create_item(name: str, db: Session = Depends(get_db)):
    new_item = Item(name=name)
    db.add(new_item)
    db.commit()
    db.refresh(new_item)
    return new_item

@router.post("/place_order")
async def save_items(selected_items: List[int] = Form(...), db: Session = Depends(get_db)):
    items = db.query(Item).filter(Item.id.in_(selected_items)).all()

    ordered_items = []
    for item in items:
        ordered_item = OrderedItem(item_name=item.name, quantity=1)  # Set the quantity as needed
        ordered_items.append(ordered_item)

    db.add_all(ordered_items)
    db.commit()

    return {"message": "Items saved successfully"}

@router.get("/list_orders")
async def get_ordered_items(db: Session = Depends(get_db)):
    ordered_items = db.query(OrderedItem).all()
    return ordered_items
