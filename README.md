# Django Bookstore API

This is a Django-based Bookstore API using Django Ninja. It includes CRUD operations for Publishers, Books, and a Wishlist system. Additionally, there is a user management API to list all users.

## Features

- Publisher CRUD operations
- Book CRUD operations (including partial updates with PATCH)
- Wishlist management (add/remove books)
- User listing API

## Project Structure

- `api.py`: Contains the main API implementation and routing.
- `schemas.py`: Defines the Pydantic schemas for request/response data.
- `models.py`: Contains the Django models (Publisher, Book, Wishlist).
- `urls.py`: Main project URLs configuration.
- `.gitignore`: Specifies files and directories to be ignored by Git.

## Getting Started

### Prerequisites

- Python 3.x
- Django 4.x
- Django Ninja

### Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/yourusername/django-bookstore-api.git
    cd django-bookstore-api
    ```

2. Create and activate a virtual environment:

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3. Install the dependencies:

    ```bash
    pip install -r requirements.txt
    ```

4. Run migrations:

    ```bash
    python manage.py migrate
    ```

5. Create a superuser:

    ```bash
    python manage.py createsuperuser
    ```

6. Run the server:

    ```bash
    python manage.py runserver
    ```

### API Documentation

After running the server, visit `http://127.0.0.1:8000/api/docs/` to see the auto-generated API documentation.

## Contributing

Feel free to open issues or create pull requests. Contributions are welcome!

## License

This project is licensed under the MIT License.
