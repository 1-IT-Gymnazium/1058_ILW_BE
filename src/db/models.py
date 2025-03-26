from __future__ import annotations
import datetime

from sqlalchemy import Date, Column, ForeignKey, Integer, String, Boolean, DateTime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

class Base(DeclarativeBase):
    """
    Base class for all SQLAlchemy models.

    This class serves as a foundation for all database models, providing
    common functionality and ensuring consistent behavior across models.
    """
    pass

class User(Base):
    """
    Represents a user in the system.

    :param id: Unique identifier for the user.
    :type id: int
    :param name: First name of the user.
    :type name: str
    :param surname: Last name of the user.
    :type surname: str
    :param ISIC_id: Unique ISIC identification string used for most of the database operations.
    :type ISIC_id: str
    :param user_number: Internal user number unique to each user.
    :type user_number: int
    :param password: User's password.
    :type password: str
    :param meals: List of meals associated with the user through orders.
    :type meals: list[src.db.models.Meal]
    """

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
    surname: Mapped[str] = mapped_column(String(30))
    ISIC_id: Mapped[str] = mapped_column(String)
    user_number: Mapped[int] = mapped_column(Integer)
    password: Mapped[str] = mapped_column(String)

    meals: Mapped[list["Meal"]] = relationship(
        "Meal",
        secondary="orders",
        back_populates="users",
    )

class Meal(Base):
    """
    Represents a meal available in the system.

    :param id: Unique identifier for the meal.
    :type id: int
    :param meal_number: Meal number used for internal tracking. Value from 1-3 representing the meal type.
    :type meal_number: int
    :param name: Name of the meal.
    :type name: str
    :param date: Date when the meal is available.
    :type date: datetime.date
    :param users: List of users who have ordered this meal.
    :type users: list[src.db.models.User]
    """
    __tablename__ = "meals"

    id: Mapped[int] = mapped_column(primary_key=True)
    meal_number: Mapped[int] = mapped_column(Integer)
    name: Mapped[str] = mapped_column(String)
    date: Mapped[datetime.date] = mapped_column(Date)

    users: Mapped[list["User"]] = relationship(
        "User",
        secondary="orders",
        back_populates="meals",
    )

class Order(Base):
    """
    Represents an order linking a user to a meal.

    :param id: Unique identifier for the order.
    :type id: int
    :param user_id: ID of the user who placed the order.
    :type user_id: int
    :param meal_id: ID of the meal that was ordered.
    :type meal_id: int
    :param status: Status of the order (True when available and false when withdrawn).
    :type status: bool
    :param withdrawed_at: Timestamp when the order was withdrawn.
    :type withdrawed_at: datetime.datetime
    :param user: Relationship to the User model.
    :type user: src.db.models.User
    :param meal: Relationship to the Meal model.
    :type meal: src.db.models.Meal
    """
    __tablename__ = 'orders'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    meal_id: Mapped[int] = mapped_column(ForeignKey('meals.id'))
    status: Mapped[bool] = mapped_column(Boolean)
    withdrawed_at: Mapped[datetime.datetime] = mapped_column(DateTime)

    user: Mapped["User"] = relationship("User", backref="orders")
    meal: Mapped["Meal"] = relationship("Meal", backref="orders")
