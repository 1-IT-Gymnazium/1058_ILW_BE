from sqlalchemy.orm import Session
from src.db.models import User
from src.db.models import Meal
from src.db.models import Order
from src.db.database import SessionLocal
import datetime
#from src.schemas import ItemCreate

# Create User
def create_user(name: str, surname: str, ISIC_id: str, user_number: int, password: str):
    session=SessionLocal()
    new_user = User(name=name, surname=surname, ISIC_id=ISIC_id, user_number=user_number, password=password)
    session.add(new_user)
    session.commit()
    session.close()

# Read (Retrieve) Users
def get_user_by_ISIC(ISIC_id: str):
    session = SessionLocal()
    user = session.query(User).filter(User.ISIC_id == ISIC_id).first()
    session.close()
    return user

# Update User by ISIC ID
def update_user( user_number: int, new_ISIC_id: str, new_name: str, new_surname: str, new_password: str):
    session = SessionLocal()
    user = session.query(User).filter(User.user_number == user_number).first()
    if user:
        user.ISIC_id = new_ISIC_id
        user.name = new_name
        user.surname=new_surname
        user.password = new_password
        session.commit()
        print(f"User {user.name} {user.surname} has been changed")
    else:
        print("User not found")
    session.close()

# Delete User by ISIC ID
def delete_user_by_ISIC(ISIC_id: str):
    session = SessionLocal()
    user = session.query(User).filter(User.ISIC_id == ISIC_id).first()
    if user:
        session.delete(user)
        session.commit()
        print(f"User {user.name} {user.surname} deleted")
    else:
        print("User not found")
    session.close()

# Create meal
def create_meal(meal_number: int, name: str, date: datetime.date):
    session = SessionLocal()
    new_meal = Meal(meal_number=meal_number, name=name, date=date)
    session.add(new_meal)
    session.commit()
    session.close()

# Read (Retrieve) meales
def get_meal_by_id(meal_id: int):
    session = SessionLocal()
    meal = session.query(Meal).filter(Meal.id == Meal.id).first()
    session.close()
    return meal

# Update meal by ID
def update_meal_name_by_id(meal_id: int, new_name: str, new_number: int):
    session = SessionLocal()
    meal = session.query(Meal).filter(Meal.id == Meal.id).first()
    if meal:
        meal.name = new_name
        meal.meal_number = new_number
        session.commit()
        print(f"meal with ID {meal_id} has been updated")
    else:
        print("meal not found")
    session.close()

# Delete meal by ID
def delete_meal_by_id(meal_id: int):
    session = SessionLocal()
    meal = session.query(meal).filter(Meal.id == Meal.id).first()
    if meal:
        session.delete(meal)
        session.commit()
        print(f"meal with ID {meal_id} deleted")
    else:
        print("meal not found")
    session.close()

#Create Order
def create_order(user_id: int, meal_id: int, status: bool, withdraw: datetime.datetime):
    session = SessionLocal()
    order = Order(user_id=user_id, meal_id=meal_id, status=status, withdraw=withdraw)
    session.add(order)
    session.commit()
    session.close()
    print("Order created successfully!")

#Retrieve Order
def get_order_by_id(order_id: int):
    session = SessionLocal()
    order = session.query(Order).filter(Order.id == order_id).first()
    session.close()
    return order

#Update Order
def update_order_status(order_id: int, new_status: bool):
    session = SessionLocal()
    order = session.query(Order).filter(Order.id == order_id).first()
    if order:
        order.status = new_status
        session.commit()
    session.close()

#Delete Order
def delete_order(order_id: int):
    session = SessionLocal()
    order = session.query(Order).filter(Order.id == order_id).first()
    if order:
        session.delete(order)
        session.commit()
    session.close()