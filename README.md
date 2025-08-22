# Book & Author Manager

A Django REST API for managing books and authors. This application provides a robust backend for managing a library
catalog with detailed information about books and their authors.

## Features

- CRUD operations for books and authors with comprehensive data models
- Many-to-many relationship between books and authors enabling flexible associations
- RESTful API endpoints built with Django REST Framework
- PostgreSQL database for reliable data storage
- Production-ready Docker configuration
- API documentation with Swagger UI
- Automated testing setup with pytest
- Static file handling with whitenoise
- Production deployment with gunicorn
- Sample data fixtures included

## Project Structure
```
gestor_libros/ 
├── books_authors/ # App with models, serializers, views, migrations 
├── core/ # Django project settings 
├── staticfiles/ # Static assets 
├── manage.py # Django management script 
├── requirements.txt # Python dependencies 
├── Dockerfile # Docker image definition 
├── docker-compose.yml # Multi-container orchestration 
├── entrypoint.sh # Container entrypoint script 
└── deploy.sh # Deployment helper script 
```
## Setup

### Prerequisites

- Docker & Docker Compose
- Python 3.10+ (for local development)

### Installation

1. Clone the repository:
```
git clone <repo-url>
cd gestor_libros
``` 
2. Configure environment variables:
   - Create a `.env` file in the root directory with the  content as in env.example
3. Set up for docker fro development:
   - Modify the `docker-compose.yml` web service to use command for entrypoint
   - Modify `.env` file to set `DEBUG=True` for development mode
4. Build and start the containers:
```./deploy.sh```
5. If you are deploying to production, ensure you have set `DEBUG=False` in the `.env` file and run the folling:
```bash
docker compose exec web python manage.py collectstatic --noinput
```

5. Access the API at `http://localhost:8000/api/`
6. Access the admin interface at `http://localhost:8000/admin/` with the superuser credentials created during setup.
7. Access the Swagger documentation at `http://localhost:8000/swagger/` to explore the API endpoints.
8. Run tests:
```bash
docker compose exec web pytest -q
```

## Authentication & Security

All API endpoints require JWT authentication.

- Obtain a token by POSTing to `/api/token/` with username and password:
  ```bash
  curl -X POST http://localhost:8000/api/token/ -d '{"username": "youruser", "password": "yourpass"}' -H "Content-Type: application/json"
  ```
- Use the token in the `Authorization: Bearer <token>` header for all requests:
  ```bash
  curl -H "Authorization: Bearer <your_token>" http://localhost:8000/api/authors/
  ```

### Fail2ban Integration

- All failed login attempts to `/api/token/` are logged in `/app/access.log`.
- You can configure fail2ban to monitor this log and block brute-force attempts.
- Example fail2ban filter:
  ```
  [Definition]
  failregex = ^.*POST /api/token/.* 401 .*
  ignoreregex =
  ```
- Example jail config:
  ```
  [django-jwt]
  enabled  = true
  port     = http,https
  filter   = django-jwt
  logpath  = /app/access.log
  maxretry = 5
  findtime = 600
  bantime  = 3600
  ```


### Endpoints

- **Books**
  - `GET /api/books/` - List all books
  - `POST /api/books/` - Create a new book
  - `GET /api/books/{id}/` - Retrieve a book by ID
  - `PUT /api/books/{id}/` - Update a book by ID
  - `DELETE /api/books/{id}/` - Delete a book by ID
  - `GET /api/books/more_than_one_author/` - List books with more than one author
  - `GET /api/books/price_range/?min_price=&max_price=` - List books filtered by price range
  - `GET /api/books/advance_search/?genre=&min_pages=&language=` - Advanced search for books by genre, pages, and language

- **Authors**
  - `GET /api/authors/` - List all authors
  - `POST /api/authors/` - Create a new author
  - `GET /api/authors/{id}/` - Retrieve an author by ID
  - `PUT /api/authors/{id}/` - Update an author by ID
  - `DELETE /api/authors/{id}/` - Delete an author by ID
  - `GET /api/authors/more_books_order/` - List authors ordered by number of books
  - `GET /api/authors/books_statistics/` - Get book statistics per author
