from sqlalchemy.orm import Session
from db.models import User
from db.models import Meal
from db.models import Order
from db.database import SessionLocal
import datetime
from schemas import UserCreate, MealCreate, OrderCreate, UserUpdate, MealUpdate, OrderUpdate

# Create User
def create_user(db: Session, user: UserCreate):
    db_user = User(name=user.name, surname=user.surname, ISIC_id=user.ISIC_id, user_number=user.user_number, password=user.password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# Read (Retrieve) Users
def get_user_by_ISIC(db: Session, ISIC_id: str):
    return db.query(User).filter(User.ISIC_id == ISIC_id).first()

# Update User by ISIC ID
def update_user(db: Session, ISIC_id: int, user_update: UserUpdate):
    user = get_user_by_ISIC(db, ISIC_id)
    if user:
        user.name = user_update.name
        user.surname= user_update.surname
        user.ISIC_id = user_update.ISIC_id
        user.user_number = user_update.user_number
        user.password = user_update.password
        db.commit()
        db.refresh(user)
        print(f"User {user.name} {user.surname} has been changed")
        return user
    else:
        print("User not found")

# Delete User by ISIC ID
def delete_user_by_ISIC(db: Session, ISIC_id: int):
    user = get_user_by_ISIC(db, ISIC_id)
    if user:
        db.delete(user)
        db.commit()
        print(f"User {user.name} {user.surname} deleted")
    else:
        print("User not found")

# Create meal
def create_meal(db: Session, meal: MealCreate):
    db_meal = Meal(meal_number=meal.meal_number, name=meal.name, date=meal.date)
    db.add(db_meal)
    db.commit()
    db.refresh(db_meal)
    return db_meal

# Read (Retrieve) meales
def get_meal_by_id(db: Session, meal_id: int):
    return db.query(Meal).filter(Meal.id == meal_id).first()

# Update meal by ID
def update_meal_name_by_id(db: Session, meal_id: int, meal_update: MealUpdate):
    meal = get_meal_by_id(db, meal_id)
    if meal:
        meal.name = meal_update.name
        meal.meal_number = meal_update.meal_number
        db.commit()
        db.refresh(meal)
        print(f"meal with ID {meal_id} has been updated")
        return meal
    else:
        print("meal not found")

# Delete meal by ID
def delete_meal_by_id(db: Session, meal_id: int):
    meal = get_meal_by_id(db, meal_id)
    if meal:
        db.delete(meal)
        db.commit()
        print(f"meal with ID {meal_id} deleted")
    else:
        print("meal not found")

#Create Order
def create_order(db: Session, order: OrderCreate):
    db_order = Order(user_id = order.user_id, meal_id = order.meal_id, status=order.status, withdrawed_at=order.withdrawed_at)
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order

#Retrieve Order
def get_order_by_id(db: Session, order_id: int):
    return db.query(Order).filter(Order.id == order_id).first()

#Update Order
def update_order_status(db: Session, order_id: int, order_update: OrderUpdate):
    order = get_order_by_id(db, order_id)
    if order:
        order.user_id = order_update.user_id
        order.meal_id = order_update.meal_id
        order.status = order_update.status
        order.withdrawed_at = order_update.withdrawed_at
        db.commit()
        db.refresh(order)
        print(f"Order with ID {order_id} has been updated")
        return order
    else:
        print("Order not found")


#Delete Order
def delete_order(db: Session, order_id: int):
    order = get_order_by_id(db, order_id)
    if order:
        db.delete(order)
        db.commit()
        print(f"Order with ID {order_id} has been deleted")
    else:
        print("Order not found")