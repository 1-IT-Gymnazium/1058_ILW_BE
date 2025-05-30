from typing import Any, Dict, List, Optional
from fastapi import HTTPException
from sqlalchemy import desc
from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound
from db.models import User, Meal, Order
from db.database import SessionLocal
import datetime
from schemas import UserCreate, MealCreate, OrderCreate, UserUpdate, MealUpdate, OrderUpdate

def create_user(db: Session, user: UserCreate) -> User:
    """
    Create a new user in the database.

    :param db: Database session.
    :type db: Session
    :param user: User data transfer object containing user details.
    :type user: UserCreate
    :return: The created user object.
    :rtype: User
    
    Example:
        >>> new_user = UserCreate(name="John", surname="Doe", ISIC_id="123456", user_number=1, password="secret")
        >>> create_user(db, new_user)
    """
    db_user = User(
        name=user.name, 
        surname=user.surname, 
        ISIC_id=user.ISIC_id, 
        user_number=user.user_number, 
        password=user.password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_all_users(db: Session) -> List[User]:
    """
    Retrieve all users from the database.

    :param db: Database session.
    :type db: Session
    :return: List of all users.
    :rtype: List[User]
    
    Example:
        >>> get_all_users(db)
    """
    return db.query(User).all()


def get_user_by_number(db: Session, user_number: str) -> User:
    """
    Retrieve a user from the database by ISIC ID.

    :param db: Database session.
    :type db: Session
    :param ISIC_id: The ISIC ID of the user to retrieve.
    :type ISIC_id: str
    :return: The user object if found, else None.
    :rtype: User | None
    
    Example:
        >>> get_user_by_ISIC(db, "123456")
    """
    return db.query(User).filter(User.user_number == user_number).first()

def update_user(db: Session, user_number: int, user_update: UserUpdate) -> User:
    """
    Update user details based on ISIC ID.

    :param db: Database session.
    :type db: Session
    :param ISIC_id: The ISIC ID of the user to update.
    :type ISIC_id: int
    :param user_update: Updated user details.
    :type user_update: UserUpdate
    :return: The updated user object if found, else None.
    :rtype: User | None
    
    Example:
        >>> updated_user = UserUpdate(name="John", surname="Doe", ISIC_id="123456", user_number=1, password="newpass")
        >>> update_user(db, 123456, updated_user)
    """
    user = get_user_by_number(db, user_number)
    if user:
        user.name = user_update.name
        user.surname = user_update.surname
        user.ISIC_id = user_update.ISIC_id
        user.user_number = user_update.user_number
        user.password = user_update.password
        db.commit()
        db.refresh(user)
        return user
    return None

def delete_user_by_ISIC(db: Session, user_number: int) -> None:
    """
    Delete a user from the database by ISIC ID.

    :param db: Database session.
    :type db: Session
    :param ISIC_id: The ISIC ID of the user to delete.
    :type ISIC_id: int
    :return: None
    
    Example:
        >>> delete_user_by_ISIC(db, 123456)
    """
    user = get_user_by_number(db, user_number)
    if user:
        db.delete(user)
        db.commit()

def create_meal(db: Session, meal: MealCreate) -> Meal:
    """
    Create a new meal in the database.

    :param db: Database session.
    :type db: Session
    :param meal: Meal data transfer object containing meal details.
    :type meal: MealCreate
    :return: The created meal object.
    :rtype: Meal
    
    Example:
        >>> new_meal = MealCreate(meal_number=1, name="Pizza", date="2025-01-01")
        >>> create_meal(db, new_meal)
    """
    db_meal = Meal(meal_number=meal.meal_number, name=meal.name, date=meal.date)
    db.add(db_meal)
    db.commit()
    db.refresh(db_meal)
    return db_meal

def get_meal_by_id(db: Session, meal_id: int) -> Meal:
    """
    Retrieve a meal from the database by ID.

    :param db: Database session.
    :type db: Session
    :param meal_id: The ID of the meal to retrieve.
    :type meal_id: int
    :return: The meal object if found, else None.
    :rtype: Meal | None
    
    Example:
        >>> get_meal_by_id(db, 1)
    """
    return db.query(Meal).filter(Meal.id == meal_id).first()

def get_all_meals(db: Session) -> List[Meal]:
    """
    Retrieve all meals from the database.

    :param db: Database session.
    :type db: Session
    :return: List of all meals.
    :rtype: List[Meal]
    
    Example:
        >>> get_all_meals(db)
    """
    return db.query(Meal).all()



def update_meal_by_id(db: Session, meal_id: int, meal_update: MealUpdate) -> Meal:
    """
    Update meal details based on meal ID.

    :param db: Database session.
    :type db: Session
    :param meal_id: The ID of the meal to update.
    :type meal_id: int
    :param meal_update: Schema containing updated meal details.
    :type meal_update: MealUpdate
    :return: The updated meal object if successful, else None.
    :rtype: Meal | None
    """
    meal = get_meal_by_id(db, meal_id)
    if meal:
        meal.name = meal_update.name
        meal.meal_number = meal_update.meal_number
        db.commit()
        db.refresh(meal)
        return meal
    return None

def delete_meal_by_id(db: Session, meal_id: int) -> None:
    """
    Delete a meal from the database by ID.

    :param db: Database session.
    :type db: Session
    :param meal_id: The ID of the meal to delete.
    :type meal_id: int
    """
    meal = get_meal_by_id(db, meal_id)
    if meal:
        db.delete(meal)
        db.commit()


def create_order(db: Session, order: OrderCreate) -> Order:
    """
    Create a new order in the database by finding user_id based on name and surname,
    and meal_id based on meal_number and today's date.

    :param db: Database session.
    :type db: Session
    :param order: Order creation schema containing user details and meal details.
    :type order: OrderCreate
    :return: The created order object.
    :rtype: Order
    :raises ValueError: If user or meal is not found.
    """
    try:
        # Hledání uživatele podle jména a příjmení
        user = db.query(User).filter(
            User.name == order.name,
            User.surname == order.surname
        ).one()
    except NoResultFound:
        raise ValueError(f"User '{order.name} {order.surname}' not found.")

    try:
        # Hledání jídla podle meal_number a dnešního data
        today = datetime.date.today()
        meal = db.query(Meal).filter(
            Meal.meal_number == order.meal_number,
            Meal.date == today
        ).one()
    except NoResultFound:
        raise HTTPException(detail=f"Meal with number {order.meal_number} for today ({today}) not found.", status_code=404)

    # Vytvoření objednávky s nalezeným user_id a meal_id
    db_order = Order(
        user_id=user.id,
        meal_id=meal.id,
        status=order.status,
        withdrawed_at=order.withdrawed_at
    )

    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order

def get_order_by_id(db: Session, order_id: int) -> Order:
    """
    Retrieve an order from the database by ID.

    :param db: Database session.
    :type db: Session
    :param order_id: The ID of the order to retrieve.
    :type order_id: int
    :return: The order object if found, else None.
    :rtype: Order | None
    """
    return db.query(Order).filter(Order.id == order_id).first()

def get_all_orders(db: Session) -> List[Order]:
    """
    Retrieve all orders from the database.

    :param db: Database session.
    :type db: Session
    :return: List of all orders.
    :rtype: List[Order]
    
    Example:
        >>> get_all_orders(db)
    """
    return db.query(Order).all()

def update_order(db: Session, user_number: int, order_update: OrderUpdate) -> Optional[Order]:
    """
    Update an order based on the user's student number (user_number).

    This function first looks up a user by their user_number. If the user exists,
    it finds the most recent order associated with the user and updates it with the new data
    provided in the `order_update` schema.

    :param db: The SQLAlchemy database session.
    :type db: Session
    :param user_number: The unique number identifying the user (used instead of user_id).
    :type user_number: int
    :param order_update: An instance of OrderUpdate containing updated order data.
    :type order_update: OrderUpdate
    :return: The updated Order object if successful, otherwise None.
    :rtype: Optional[Order]
    """

    # Find user by student number
    user = db.query(User).filter(User.user_number == user_number).first()
    if not user:
        return None

    # Find the most recent order by user_id (adjust logic if needed)
    order = db.query(Order).filter(Order.user_id == user.id).order_by(Order.id.desc()).first()
    if not order:
        return None

    # Apply updates to the order
    order.user_id = order_update.user_id
    order.meal_id = order_update.meal_id
    order.status = order_update.status
    order.withdrawed_at = order_update.withdrawed_at

    # Commit changes to the database
    db.commit()
    db.refresh(order)
    return order

def delete_order(db: Session, order_id: int) -> None:
    """
    Delete an order from the database by ID.

    :param db: Database session.
    :type db: Session
    :param order_id: The ID of the order to delete.
    :type order_id: int
    """
    order = get_order_by_id(db, order_id)
    if order:
        db.delete(order)
        db.commit()

def get_user_meal_info(db: Session, isic_id: str) -> Dict[str, Any]:
    """
    Retrieve user and meal information based on ISIC_id, but only for today's meals.

    1. Najde `user.id` na základě `ISIC_id`.
    2. Hledá pouze objednávky (`orders`), kde `meal.date = today()`.

    :param db: Database session.
    :param isic_id: ISIC ID of the user.
    :return: Dictionary containing user and meal info.

    Example:
        >>> get_user_meal_info(db, "123456789")
    """

    today = datetime.date.today()

    # Získání ID uživatele podle ISIC_id
    user = db.query(User).filter(User.ISIC_id == isic_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Tento uživatel nebyl nalezen")

    # Hledání objednávky pouze pro dnešní datum
    result = (
        db.query(
            Meal.id.label("meal_id"),
            User.id.label("user_id"),
            Order.status.label("order_status"),
            User.name.label("user_name"), 
            Meal.meal_number.label("meal_number"), 
            Meal.name.label("meal_name"), 
            User.user_number.label("user_number"),
            Meal.date.label("meal_date")
        )
        .join(Order, Order.user_id == User.id)
        .join(Meal, Order.meal_id == Meal.id)
        .filter(Order.user_id == user.id, Meal.date == today)
        .first()  # Vrátí pouze první nalezenou objednávku pro dnešek
    )

    if not result:
        raise HTTPException(status_code=404, detail="Tento uživatel dnes nemá jídlo")

    return {
        "meal_id": result.meal_id,
        "user_id": result.user_id,
        "order_status": result.order_status,
        "user_name": result.user_name,
        "user_number": result.user_number,
        "meal_number": result.meal_number,
        "meal_name": result.meal_name,
        "meal_date": result.meal_date
    }