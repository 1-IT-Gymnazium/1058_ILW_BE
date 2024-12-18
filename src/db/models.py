from __future__ import annotations
import datetime

from sqlalchemy import Date, Column, ForeignKey, Integer, String, Table
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column


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


class Lunch(Base):
    __tablename__ = "lunches"

    id: Mapped[int] = mapped_column(primary_key=True)
    lunch_number: Mapped[int] = mapped_column(Integer)
    name: Mapped[str] = mapped_column(String)
    date: Mapped[datetime.date] = mapped_column(Date)


UserLunch = Table(
    "users_lunches",
    Base.metadata,
    Column("user_id", ForeignKey("users.id")),
    Column("lunch_id", ForeignKey("lunches.id")),
)
