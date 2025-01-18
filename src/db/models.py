from __future__ import annotations
import datetime

from sqlalchemy import Date, Column, ForeignKey, Integer, String, Table, Boolean, DateTime
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship


class Base(DeclarativeBase):
    pass


class User(Base):
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
    __tablename__ = 'orders'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    meal_id: Mapped[int] = mapped_column(ForeignKey('meals.id'))
    status: Mapped[bool] = mapped_column(Boolean)
    withdrawed_at: Mapped[datetime.datetime] = mapped_column(DateTime)

    user: Mapped["User"] = relationship("User", backref="orders")
    meal: Mapped["Meal"] = relationship("Meal", backref="orders")



