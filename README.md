# Book & Author Manager

A Django REST API for managing books and authors.

## Features

- CRUD operations for books and authors
- Many-to-many relationship between books and authors
- API endpoints with Django REST Framework
- PostgreSQL database support
- Dockerized for easy deployment

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
3. Set up for docker on development:
   - Modify the `docker-compose.yml` web service to use command for entrypoint
   - Modify `.env` file to set `DEBUG=True` for development mode
4. Build and start the containers:
```./deploy.sh```
5. Access the API at `http://localhost:8000/api/`
6. Access the admin interface at `http://localhost:8000/admin/` with the superuser credentials created during setup.
7. Access the Swagger documentation at `http://localhost:8000/swagger/` to explore the API endpoints.
8. Run tests:
```bash
docker compose exec web pytest -q
```

### Endpoints

- **Books**
  - `GET /api/books/` - List all books
  - `POST /api/books/` - Create a new book
  - `GET /api/books/{id}/` - Retrieve a book by ID
  - `PUT /api/books/{id}/` - Update a book by ID
  - `DELETE /api/books/{id}/` - Delete a book by ID
- **Authors**
  - `GET /api/authors/` - List all authors
  - `POST /api/authors/` - Create a new author
  - `GET /api/authors/{id}/` - Retrieve an author by ID
  - `PUT /api/authors/{id}/` - Update an author by ID
  - `DELETE /api/authors/{id}/` - Delete an author by ID



