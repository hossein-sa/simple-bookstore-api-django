from ninja import NinjaAPI, Router
from typing import List
from books.models import Publisher, Book, Wishlist
from django.contrib.auth.models import User
from books.schemas import PublisherSchemaOut, PublisherSchemaIn, BookSchemaIn, BookSchemaOut, WishlistSchemaOut, BookSchemaPartialUpdate, UserSchema
from ninja.errors import HttpError
from ninja_jwt.authentication import JWTAuth
from ninja_jwt.routers.obtain import obtain_pair_router


# Initialize the main API
api = NinjaAPI()


api.add_router("/token", tags=["Auth"], router=obtain_pair_router)


# Create separate routers for better organization
publisher_router = Router(tags=["Publishers"], auth=JWTAuth())
book_router = Router(tags=["Books"], auth=JWTAuth())
wishlist_router = Router(tags=["Wishlist"], auth=JWTAuth())
user_router = Router(tags=["Users"], auth=JWTAuth())

# Publisher CRUD Operations
@publisher_router.get("/", response=List[PublisherSchemaOut], auth=None)
def list_publishers(request):
    return Publisher.objects.all()

@publisher_router.post("/", response=PublisherSchemaOut)
def create_publisher(request, data: PublisherSchemaIn):
    publisher = Publisher.objects.create(**data.dict())
    return publisher

@publisher_router.put("/{publisher_id}/", response=PublisherSchemaOut)
def update_publisher(request, publisher_id: int, data: PublisherSchemaIn):
    try:
        publisher = Publisher.objects.get(id=publisher_id)
        for attr, value in data.dict().items():
            setattr(publisher, attr, value)
        publisher.save()
        return publisher
    except Publisher.DoesNotExist:
        raise HttpError(404, "Publisher not found")

@publisher_router.delete("/{publisher_id}/")
def delete_publisher(request, publisher_id: int):
    try:
        publisher = Publisher.objects.get(id=publisher_id)
        publisher.delete()
        return {"success": True}
    except Publisher.DoesNotExist:
        raise HttpError(404, "Publisher not found")


# Book CRUD Operations
@book_router.get("/", response=List[BookSchemaOut], auth=None)
def list_books(request):
    return Book.objects.select_related('publisher').all()

@book_router.post("/", response=BookSchemaOut)
def create_book(request, data: BookSchemaIn):
    try:
        publisher = Publisher.objects.get(id=data.publisher_id)
        book = Book.objects.create(
            title=data.title,
            author=data.author,
            publisher=publisher,
            price=data.price,
            published_date=data.published_date,
        )
        return book
    except Publisher.DoesNotExist:
        raise HttpError(404, "Publisher not found")

@book_router.patch("/{book_id}/", response=BookSchemaOut)
def update_book(request, book_id: int, data: BookSchemaPartialUpdate):
    try:
        book = Book.objects.get(id=book_id)
        # Update only the fields provided in the request
        for attr, value in data.dict(exclude_unset=True).items():
            setattr(book, attr, value)
        book.save()
        return book
    except Book.DoesNotExist:
        raise HttpError(404, "Book not found")




@book_router.delete("/{book_id}/")
def delete_book(request, book_id: int):
    try:
        book = Book.objects.get(id=book_id)
        book.delete()
        return {"success": True}
    except Book.DoesNotExist:
        raise HttpError(404, "Book not found")


# Wishlist Operations
@wishlist_router.get("/{user_id}/", response=WishlistSchemaOut)
def get_wishlist(request, user_id: int):
    try:
        wishlist = Wishlist.objects.get(user_id=user_id)
        return wishlist
    except Wishlist.DoesNotExist:
        raise HttpError(404, "Wishlist not found")

@wishlist_router.post("/{user_id}/add/{book_id}/")
def add_to_wishlist(request, user_id: int, book_id: int):
    try:
        user = User.objects.get(id=user_id)
        book = Book.objects.get(id=book_id)
        wishlist, created = Wishlist.objects.get_or_create(user=user)
        wishlist.books.add(book)
        return {"success": True}
    except User.DoesNotExist:
        raise HttpError(404, "User not found")
    except Book.DoesNotExist:
        raise HttpError(404, "Book not found")

@wishlist_router.post("/{user_id}/remove/{book_id}/")
def remove_from_wishlist(request, user_id: int, book_id: int):
    try:
        user = User.objects.get(id=user_id)
        book = Book.objects.get(id=book_id)
        wishlist = Wishlist.objects.get(user=user)
        wishlist.books.remove(book)
        return {"success": True}
    except User.DoesNotExist:
        raise HttpError(404, "User not found")
    except Book.DoesNotExist:
        raise HttpError(404, "Book not found")
    except Wishlist.DoesNotExist:
        raise HttpError(404, "Wishlist not found")



@user_router.get("/", response=List[UserSchema])
def list_users(request):
    users = User.objects.all()
    return users



# Register routers with the main API
api.add_router("/publishers/", publisher_router)
api.add_router("/books/", book_router)
api.add_router("/wishlist/", wishlist_router)
api.add_router("/users/", user_router)
