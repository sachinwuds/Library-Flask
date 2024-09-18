
# Flask Library Management System

This is a simple Flask-based Library Management System that allows users to list, create, update, and delete books. Admin access is required for creating, updating, and deleting books. The app also uses JWT authentication to secure the endpoints.

## Features

- **GET /books**: List all books.
- **POST /books**: Create a new book (Admin access required).
- **PUT /books/<id>**: Update an existing book (Admin access required).
- **DELETE /books/<id>**: Delete a book (Admin access required).
- JWT-based authentication for securing endpoints.
- SQLite database for storing books.

## Requirements

- [Docker](https://www.docker.com/)
- [Python 3.9+](https://www.python.org/downloads/) (if running locally without Docker)

## Project Setup

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/library-management-system.git
cd library-management-system
```

### 2. Run with Docker

This project is containerized using Docker. Follow the steps below to run the project in Docker.

#### a) Build the Docker Image

```bash
docker build -t flask-app .
```

#### b) Run the Docker Container

```bash
docker run -p 5000:5000 flask-app
```

This command maps port 5000 of the container to port 5000 on your local machine. You can access the app by visiting `http://localhost:5000`.

### 3. API Endpoints

Here are the available API endpoints:

| Method | Endpoint          | Description                        | Authorization |
|--------|-------------------|------------------------------------ |---------------|
| GET    | `/books`           | List all books                     | None          |
| POST   | `/books`           | Create a new book                  | Admin         |
| PUT    | `/books/<id>`      | Update a specific book             | Admin         |
| DELETE | `/books/<id>`      | Delete a specific book             | Admin         |

To interact with the API, you can use tools like [Postman](https://www.postman.com/) or [curl](https://curl.se/).

### 4. Authentication

This project uses JWT for user authentication. You will need to obtain a JWT token to access the admin-protected routes.

#### Register admin
Send a `POST` request to `/auth/register` with a username, password and is_admin to register the admin:
```json
{
  "username": "admin",
  "password": "admin_password",
  "is_admin":true
}
```

#### Get Token
Send a `POST` request to `/auth/login` with a valid username and password to receive a JWT token:
```json
{
  "username": "admin",
  "password": "admin_password"
}
```

You will receive a token in the response, which must be included in the Authorization header for secured routes:
```
Authorization: Bearer <token>
```

### 5. Running Tests

If you want to run unit tests, follow the steps below.

#### a) Running Tests with `unittest`

```bash
python -m unittest discover -s tests
```

#### b) Running Tests with `pytest`

```bash
pytest
```

### 6. Running Locally (without Docker)

If you don't want to use Docker, you can also run the app locally:

#### a) Set up a virtual environment

```bash
python -m venv venv
source venv/bin/activate    # On Windows: venv\Scripts\activate
```

#### b) Install dependencies

```bash
pip install -r requirements.txt
```

#### c) Run the Flask app

```bash
flask run
```

The app will be available at `http://localhost:5000`.

## Environment Variables

Make sure to set up the following environment variables in a `.env` file for JWT authentication and Flask configuration:

```env
SECRET_KEY=your_secret_key
JWT_SECRET_KEY=your_jwt_secret_key
FLASK_ENV=development
```

## Troubleshooting

### Port Already in Use

If you encounter an error that port `5000` is already in use, you can either stop the process using the port or map the application to a different port:
```bash
docker run -p 5001:5000 flask-app
```
