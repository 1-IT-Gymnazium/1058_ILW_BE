from typing import Optional
from pydantic import BaseModel, ValidationError, AfterValidator
import datetime
from typing_extensions import Annotated

def CheckMealValue(v: int) -> int:
    """
    Validate meal number to ensure it is between 1 and 3.

    :param v: Meal number to validate.
    :type v: int
    :return: The validated meal number.
    :rtype: int
    :raises ValueError: If the value is not between 1 and 3 which is the range of the possible meal numbers.
    """
    if v > 3 or v < 1:
        raise ValueError("value must be between or containing 1-3")
    return v

class UserBase(BaseModel):
    """
    Base schema for user data.
    """
    name: str
    surname: str
    ISIC_id: str
    user_number: int
    password: str

class UserCreate(UserBase):
    """
    Schema for creating a new user.
    """
    pass

class UserUpdate(UserBase):
    """
    Schema for updating an existing user.
    """
    pass

class User(UserBase):
    """
    Schema for user retrieval including an ID.
    """
    id: int

    class Config:
        from_attributes = True

class MealBase(BaseModel):
    """
    Base schema for meal data.
    """
    meal_number: Annotated[int, AfterValidator(CheckMealValue)]
    name: str
    date: datetime.date

class MealCreate(MealBase):
    """
    Schema for creating a new meal.
    """
    pass

class MealUpdate(MealBase):
    """
    Schema for updating an existing meal.
    """
    pass

class Meal(MealBase):
    """
    Schema for meal retrieval including an ID.
    """
    id: int

    class Config:
        from_attributes = True

class OrderBase(BaseModel):
    """
    Base schema for order data.
    """
    user_id: int
    meal_id: int
    status: bool | None = True
    withdrawed_at: datetime.datetime | None = None

class OrderCreate(BaseModel):
    name: str  # Jméno uživatele
    surname: str  # Příjmení uživatele
    meal_number: int  # Číslo jídla
    status: bool  # Stav objednávky (např. True = aktivní)
    withdrawed_at: Optional[datetime.datetime] = None  # Čas výdeje (nepovinné)
  

class OrderUpdate(OrderBase):
    """
    Schema for updating an existing order.
    """
    pass

class Order(OrderBase):
    """
    Schema for order retrieval including an ID.
    """
    id: int

    class Config:
        from_attributes = True
