from pydantic import BaseModel
import datetime

class UserBase(BaseModel):
    name: str
    surname: str
    ISIC_id: str
    user_number: int
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
    meal_number: int
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
