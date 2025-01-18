from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db.database import SessionLocal
from crud import create_meal, create_order, create_user, get_meal_by_id, get_order_by_id, get_user_by_ISIC, update_meal_name_by_id, update_order_status, update_user, delete_meal_by_id, delete_order, delete_user_by_ISIC
from schemas import Order, User, Meal, MealCreate, OrderCreate, UserCreate, UserUpdate, MealUpdate, OrderUpdate

router_user = APIRouter(prefix="/users", tags=["users"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router_user.post("/", response_model=User)
def create_user_endpoint(user: UserCreate, db: Session = Depends(get_db)):
    return create_user(db=db, user=user)

@router_user.get("/{ISIC_id}", response_model=User)
def get_user_endpoint(ISIC_id: str, db: Session = Depends(get_db)):
    user = get_user_by_ISIC(db=db, ISIC_id=ISIC_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router_user.put("/{ISIC_id}", response_model=User)
def update_user_endpoint(ISIC_id: str, user_update: UserUpdate, db: Session = Depends(get_db)):
    return update_user(db=db, ISIC_id=ISIC_id, user_update=user_update)

@router_user.delete("/{ISIC_id}")
def delete_user_endpoint(ISIC_id: str, db: Session = Depends(get_db)):
    delete_user_by_ISIC(db=db, ISIC_id=ISIC_id)
    return {"message": "User deleted successfully!"}

router_meals = APIRouter(prefix="/meals", tags=["meals"])

@router_meals.post("/", response_model=Meal)
def create_meal_endpoint(meal: MealCreate, db: Session = Depends(get_db)):
    return create_meal(db=db, meal=meal)

@router_meals.get("/{meal_id}", response_model=Meal)
def get_meal_endpoint(meal_id: int, db: Session = Depends(get_db)):
    meal = get_meal_by_id(db=db, meal_id=meal_id)
    if meal is None:
        raise HTTPException(status_code=404, detail="Meal not found")
    return meal

@router_meals.put("/{meal_id}", response_model=Meal)
def update_meal_endpoint(meal_id: int, meal_update: MealUpdate, db: Session = Depends(get_db)):
    return update_meal_name_by_id(db=db, meal_id=meal_id, meal_update=meal_update)

@router_meals.delete("/{meal_id}")
def delete_meal_endpoint(meal_id: int, db: Session = Depends(get_db)):
    delete_meal_by_id(db=db, meal_id=meal_id)
    return {"message": "Meal deleted successfully!"}

router_orders = APIRouter(prefix="/orders", tags=["orders"])

@router_orders.post("/", response_model=Order)
def create_order_endpoint(order: OrderCreate, db: Session = Depends(get_db)):
    return create_order(db=db, order=order)

@router_orders.get("/{order_id}", response_model=Order)
def get_order_endpoint(order_id: int, db: Session = Depends(get_db)):
    order = get_order_by_id(db=db, order_id=order_id)
    if order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return order

@router_orders.put("/{order_id}", response_model=Order)
def update_order_endpoint(order_id: int, order_update: OrderUpdate, db: Session = Depends(get_db)):
    return update_order_status(db=db, order_id=order_id, order_update=order_update)

@router_orders.delete("/{order_id}")
def delete_order_endpoint(order_id: int, db: Session = Depends(get_db)):
    delete_order(db=db, order_id=order_id)
    return {"message": "Order deleted successfully!"}
