from datetime import date
from typing import Any, Dict, List
from fastapi import APIRouter, Depends, HTTPException, Query, Security
from sqlalchemy.orm import Session
from db.database import SessionLocal
from utils import VerifyToken
from crud import (
    create_meal, create_order, create_user, get_all_meals, get_all_orders, get_all_users, get_meal_by_id, get_order_by_id,
    get_user_by_number, get_user_meal_info, update_meal_by_id, update_order, update_user,
    delete_meal_by_id, delete_order, delete_user_by_ISIC
)
from schemas import (
    Order, User, Meal, MealCreate, OrderCreate, UserCreate,
    UserUpdate, MealUpdate, OrderUpdate
)

auth = VerifyToken()

# Router for user-related endpoints
router_user = APIRouter(prefix="/users", tags=["users"])

def get_db():
    """
    Dependency to get a new database session.
    
    :yield: SQLAlchemy database session.
    :rtype: Session
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router_user.post("/", response_model=User)
def create_user_endpoint(user: UserCreate, db: Session = Depends(get_db)):
    """
    Create a new user.
    
    :param user: User creation data.
    :type user: UserCreate
    :param db: Database session.
    :type db: Session
    :return: Created user object.
    :rtype: User
    """
    return create_user(db=db, user=user)

@router_user.get("/private", response_model=List[User])
def get_all_users_endpoint(db: Session = Depends(get_db)):
    """
    Retrieve all users.
    
    :param db: Database session.
    :type db: Session
    :return: List of all users.
    :rtype: List[User]
    """
    users = get_all_users(db=db)
    return users


@router_user.get("/{user_number}", response_model=User)
def get_user_endpoint(user_number: str, db: Session = Depends(get_db)):
    """
    Retrieve a user by ISIC ID.
    
    :param ISIC_id: The ISIC ID of the user.
    :type ISIC_id: str
    :param db: Database session.
    :type db: Session
    :return: User object if found.
    :rtype: User
    :raises HTTPException: If user is not found.
    """
    user = get_user_by_number(db=db, user_number=user_number)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user



@router_user.put("/{user_number}", response_model=User)
def update_user_endpoint(user_number: str, user_update: UserUpdate, db: Session = Depends(get_db)):
    """
    Update an existing user by ISIC ID.
    
    :param ISIC_id: The ISIC ID of the user to update.
    :type ISIC_id: str
    :param user_update: Updated user details.
    :type user_update: UserUpdate
    :param db: Database session.
    :type db: Session
    :return: Updated user object.
    :rtype: User
    """
    return update_user(db=db, user_number=user_number, user_update=user_update)

@router_user.delete("/{user_number}")
def delete_user_endpoint(user_number: str, db: Session = Depends(get_db)):
    """
    Delete a user by ISIC ID.
    
    :param ISIC_id: The ISIC ID of the user.
    :type ISIC_id: str
    :param db: Database session.
    :type db: Session
    :return: Success message.
    :rtype: dict
    """
    delete_user_by_ISIC(db=db, user_number=user_number)
    return {"message": "User deleted successfully!"}

@router_user.get("/meals-info/{ISIC_id}")
def get_meal_info_by_ISIC(ISIC_id: str, db: Session = Depends(get_db)) -> Dict[str, Any]:
    """
    Retrieve user and meal information based on ISIC_id.
    
    :param ISIC_id: The ISIC ID of the user.
    :type ISIC_id: str
    :param db: Database session.
    :type db: Session
    :return: Dictionary containing user and meal info.
    :rtype: Dict[str, Any]

    Example:
        GET /users/123456789
    """
    return get_user_meal_info(db=db, isic_id=ISIC_id)

router_meals = APIRouter(prefix="/meals", tags=["meals"])

@router_meals.post("/", response_model=Meal)
def create_meal_endpoint(meal: MealCreate, db: Session = Depends(get_db)):
    """
    Create a new meal.
    
    :param meal: Meal data.
    :type meal: MealCreate
    :param db: Database session.
    :type db: Session
    :return: Created meal object.
    :rtype: Meal
    """
    return create_meal(db=db, meal=meal)

@router_meals.get("/", response_model=List[Meal])
def get_all_meals_endpoint(db: Session = Depends(get_db)):
    """
    Retrieve all meals.
    
    :param db: Database session.
    :type db: Session
    :return: List of all meals.
    :rtype: List[Meal]
    """
    meals = get_all_meals(db=db)
    return meals


@router_meals.get("/{meal_id}", response_model=Meal)
def get_meal_endpoint(meal_id: int, db: Session = Depends(get_db)):
    """
    Retrieve meal by ID.
    
    :param meal_id: Meal ID.
    :type meal_id: int
    :param db: Database session.
    :type db: Session
    :raises HTTPException: If meal is not found.
    :return: Meal object.
    :rtype: Meal
    """
    meal = get_meal_by_id(db=db, meal_id=meal_id)
    if meal is None:
        raise HTTPException(status_code=404, detail="Meal not found")
    return meal

@router_meals.put("/{meal_id}", response_model=Meal)
def update_meal_endpoint(meal_id: int, meal_update: MealUpdate, db: Session = Depends(get_db)):
    """
    Update meal details.
    
    :param meal_id: Meal ID.
    :type meal_id: int
    :param meal_update: Updated meal details.
    :type meal_update: MealUpdate
    :param db: Database session.
    :type db: Session
    :return: Updated meal object.
    :rtype: Meal
    """
    return update_meal_by_id(db=db, meal_id=meal_id, meal_update=meal_update)

@router_meals.delete("/{meal_id}")
def delete_meal_endpoint(meal_id: int, db: Session = Depends(get_db), auth_result: str = Security(auth.verify)):
    """
    Delete a meal by ID.
    
    :param meal_id: Meal ID.
    :type meal_id: int
    :param db: Database session.
    :type db: Session
    :return: Deletion confirmation message.
    :rtype: dict
    """
    delete_meal_by_id(db=db, meal_id=meal_id)
    return {"message": "Meal deleted successfully!"}

router_orders = APIRouter(prefix="/orders", tags=["orders"])

@router_orders.post("/", response_model=Order)
def create_order_endpoint(order: OrderCreate, db: Session = Depends(get_db)):
    """
    Create a new order.
    
    :param order: Order data.
    :type order: OrderCreate
    :param db: Database session.
    :type db: Session
    :return: Created order object.
    :rtype: Order
    """
    return create_order(db=db, order=order)

@router_orders.get("/", response_model=List[Order])
def get_all_orders_endpoint(db: Session = Depends(get_db)):
    """
    Retrieve all orders
    
    :param db: Database session.
    :type db: Session
    :return: List of all meals.
    :rtype: List[Meal]
    """
    meals = get_all_orders(db=db)
    return meals

@router_orders.get("/{order_id}", response_model=Order)
def get_order_endpoint(order_id: int, db: Session = Depends(get_db)):
    """
    Retrieve order by ID.
    
    :param order_id: Order ID.
    :type order_id: int
    :param db: Database session.
    :type db: Session
    :raises HTTPException: If order is not found.
    :return: Order object.
    :rtype: Order
    """
    order = get_order_by_id(db=db, order_id=order_id)
    if order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return order

@router_orders.put("/{user_number}", response_model=Order)
def update_order_endpoint(user_number: int, order_update: OrderUpdate, db: Session = Depends(get_db)):
    """
    Update an existing order in the database.

    :param user_number: Unique user number.
    :type user_number: int
    :param order_update: The updated order details.
    :type order_update: OrderUpdate
    :param db: Database session dependency.
    :type db: Session
    :return: The updated order object.
    :rtype: Order

    :raises HTTPException 404: If the order with the given ID is not found.

    Example:
        >>> update_order_endpoint(1023, OrderUpdate(user_id=2, meal_id=3, status=False, withdrawed_at=None), db)
    """
    return update_order(db=db, user_number=user_number, order_update=order_update)


@router_orders.delete("/{order_id}")
def delete_order_endpoint(order_id: int, db: Session = Depends(get_db)):
    """
    Delete an order by ID.
    
    :param order_id: Order ID.
    :type order_id: int
    :param db: Database session.
    :type db: Session
    :return: Deletion confirmation message.
    :rtype: dict
    """
    delete_order(db=db, order_id=order_id)
    return {"message": "Order deleted successfully!"}

