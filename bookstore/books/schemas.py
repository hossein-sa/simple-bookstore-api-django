from ninja import Schema
from datetime import date
from typing import Optional

# Publisher Schemas
class PublisherSchemaIn(Schema):
    name: str

class PublisherSchemaOut(Schema):
    id: int
    name: str


# Book Schemas
class BookSchemaIn(Schema):
    title: str
    author: str
    publisher_id: int  # Use publisher_id here for input
    price: float
    published_date: date

class BookSchemaOut(Schema):
    id: int
    title: str
    author: str
    publisher: PublisherSchemaOut  # Use PublisherSchemaOut for nested output
    price: float
    published_date: date


# This schema is specifically for PATCH operations with optional fields
class BookSchemaPartialUpdate(Schema):
    title: Optional[str] = None
    author: Optional[str] = None
    publisher_id: Optional[int] = None
    price: Optional[float] = None
    published_date: Optional[date] = None
    
    
# Wishlist Schemas
class WishlistSchemaOut(Schema):
    id: int
    user_id: int
    books: list[BookSchemaOut]


# User Schema
class UserSchema(Schema):
    id: int
    username: str
    email: str
