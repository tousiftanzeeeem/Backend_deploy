# Backend API

## Setup

### Using Docker

Run with docker-compose from the root directory:

```bash
docker-compose up -d
```

### Manual Setup

1. Start PostgreSQL:

```bash
docker run -d --name postgres -e POSTGRES_PASSWORD=postgres -e POSTGRES_DB=user_management -p 5432:5432 postgres:15-alpine
```

2. Create a virtual environment:

```bash
python -m venv venv
```

3. Activate the virtual environment:

- Windows: `venv\Scripts\activate`
- Linux/Mac: `source venv/bin/activate`

4. Install dependencies:

```bash
pip install -r requirements.txt
```

5. Configure environment:
   Copy `.env.example` to `.env` and update if needed.

6. Run the server:

```bash
python main.py
```

The API will be available at http://localhost:8000

## Environment Variables

Create a `.env` file:

```
POSTGRES_HOST=localhost
POSTGRES_USER=postgres
POSTGRES_PASS=postgres
POSTGRES_DATABASE=user_management
CORS_ORIGINS=http://localhost:3000
```

## Database

The application uses PostgreSQL. The database schema is automatically created on startup.

**Users Table:**

- id: Integer (Primary Key)
- name: String
- email: String (Unique)
- created_at: DateTime

## API Endpoints

- `GET /api/users` - Get all users
- `POST /api/users` - Add a new user
  - Body: `{"name": "John Doe", "email": "john@example.com"}`

## API Documentation

Visit http://localhost:8000/docs for interactive API documentation.
