from pydantic import BaseModel, ValidationError, AfterValidator
import datetime
from typing_extensions import Annotated

#Funkce CheckMealValue kontroluje jestli má jídlo povolené čísla
def CheckMealValue(v: int):
        if (v > 3 or v < 1):
            raise ValueError("value must be between or containing 1-3")
        return v

def CheckUserNumberLength(v: int):
    length = len(str(v))
    if(length == 4):
        return v
    else:
        raise ValueError("User number must be 4 digits long")

class UserBase(BaseModel):
    name: str
    surname: str
    ISIC_id: str
    user_number: Annotated[int, AfterValidator(CheckUserNumberLength)]
    password: str


class UserCreate(UserBase):
    pass

class UserUpdate(UserBase):
    pass

class User(UserBase):
    id: int

    class Config:
        from_attributes = True


class MealBase(BaseModel):
    meal_number: Annotated[int, AfterValidator(CheckMealValue)]
    name: str
    date: datetime.date

class MealCreate(MealBase):
    pass

class MealUpdate(MealBase):
    pass

class Meal(MealBase):
    id: int

    class Config:
        from_attributes = True

class OrderBase(BaseModel):
    user_id: int
    meal_id: int
    status: bool | None = True
    withdrawed_at: datetime.datetime | None = None

class OrderCreate(OrderBase):
    pass

class OrderUpdate(OrderBase):
    pass

class Order(OrderBase):
    id: int

    class Config:
        from_attributes = True 
