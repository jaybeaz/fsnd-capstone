# FSND Capstone: Casting Agency API

## Project Overview

The Casting Agency API is a backend system that manages actors and movies for a casting agency. The API implements role-based access control (RBAC) with three different user roles, each with specific permissions for managing the database.

**Live Application URL:** `https://render-deployment-example-b64l.onrender.com/`

## Tech Stack

- **Backend Framework:** Flask (Python)
- **Database:** PostgreSQL
- **Authentication:** Auth0 (JWT tokens with RBAC)
- **Deployment:** Render
- **Testing:** Python unittest

## Getting Started Locally

### Prerequisites

- Python 3.10
- PostgreSQL
- Auth0 account (for authentication)

### Installation

1. **Clone the repository:**
```bash
git clone https://github.com/jaybeaz/fsnd-capstone.git
cd fsnd-capstone
```

2. **Create and activate virtual environment:**
```bash
python3.10 -m venv capstone_venv
source capstone_venv/bin/activate  # On Windows: capstone_venv\Scripts\activate
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

4. **Set up database and environment variables:**
```bash
source setup.sh
```

5. **Run the application:**
```bash
python app.py
```

The app will run on `http://127.0.0.1:3000/`

## Running Tests

1. **Create test database:**
```bash
createdb casting_test
```

2. **Update tokens in `test_app.py`:**
Copy the `access_token` values specified below into lines 11-13 of `test_app.py`

3. **Run tests:**
```bash
python test_app.py
```

All 13 tests should pass.

## API Documentation

### Base URL

**Local:** `http://127.0.0.1:3000`  
**Deployed:** `https://render-deployment-example-b64l.onrender.com/`

### Authentication

All endpoints (except `/`, `/coolkids`, `/lebowski`, and `/thejesus`) require authentication via JWT Bearer token.

**Header format:**
```
Authorization: Bearer <JWT_TOKEN>
```

### Endpoints

#### GET /actors

Get all actors.

**Required Permission:** `get:actors`

**Response:**
```json
{
  "success": true,
  "actors": [
    {
      "id": 1,
      "name": "Tom Hanks",
      "age": 67,
      "gender": "Male"
    }
  ],
  "total_actors": 1
}
```

#### GET /movies

Get all movies.

**Required Permission:** `get:movies`

**Response:**
```json
{
  "success": true,
  "movies": [
    {
      "id": 1,
      "title": "Forrest Gump",
      "release_date": "1994-07-06"
    }
  ],
  "total_movies": 1
}
```

#### POST /actors

Create a new actor.

**Required Permission:** `post:actors`

**Request Body:**
```json
{
  "name": "Brad Pitt",
  "age": 60,
  "gender": "Male"
}
```

**Response:**
```json
{
  "success": true,
  "created": 2,
  "actors": [...],
  "total_actors": 2
}
```

#### POST /movies

Create a new movie.

**Required Permission:** `post:movies`

**Request Body:**
```json
{
  "title": "Inception",
  "release_date": "2010-07-16"
}
```

**Response:**
```json
{
  "success": true,
  "created": 2,
  "movies": [...],
  "total_movies": 2
}
```

#### PATCH /actors/<actor_id>

Update an existing actor.

**Required Permission:** `patch:actors`

**Request Body (all fields optional):**
```json
{
  "name": "Tom Hanks",
  "age": 68,
  "gender": "Male"
}
```

**Response:**
```json
{
  "success": true,
  "actor": 1
}
```

#### PATCH /movies/<movie_id>

Update an existing movie.

**Required Permission:** `patch:movies`

**Request Body (all fields optional):**
```json
{
  "title": "Forrest Gump (Updated)",
  "release_date": "1994-07-06"
}
```

**Response:**
```json
{
  "success": true,
  "movie": 1
}
```

#### DELETE /actors/<actor_id>

Delete an actor.

**Required Permission:** `delete:actors`

**Response:**
```json
{
  "success": true,
  "deleted": 1
}
```

#### DELETE /movies/<movie_id>

Delete a movie.

**Required Permission:** `delete:movies`

**Response:**
```json
{
  "success": true,
  "deleted": 1
}
```

### Error Responses

**401 Unauthorized:**
```json
{
  "success": false,
  "error": 401,
  "message": "Authorization header is expected."
}
```

**404 Not Found:**
```json
{
  "success": false,
  "error": 404,
  "message": "resource not found"
}
```

**422 Unprocessable:**
```json
{
  "success": false,
  "error": 422,
  "message": "unprocessable"
}
```

## Roles and Permissions

### Casting Assistant

**Permissions:**
- `get:actors`
- `get:movies`

**Can:**
- View all actors and movies

**Cannot:**
- Create, update, or delete anything

### Casting Director

**Permissions:**
- `get:actors`
- `get:movies`
- `post:actors`
- `delete:actors`
- `patch:actors`
- `patch:movies`

**Can:**
- View all actors and movies
- Add or delete actors
- Modify actors and movies

**Cannot:**
- Add or delete movies

### Executive Producer

**Permissions:** All permissions
- `get:actors`
- `get:movies`
- `post:actors`
- `post:movies`
- `delete:actors`
- `delete:movies`
- `patch:actors`
- `patch:movies`

**Can:**
- Perform all actions including adding and deleting movies

## Auth0 Configuration

**Domain:** `dev-2chb8bw0zdh1z1um.us.auth0.com`  
**API Identifier:** `fsnd-casting-agency-capstone`

### Test Users

**Casting Assistant:**
- Email: `assistant@test.com`
- Password: ***********

**Casting Director:**
- Email: `director@test.com`
- Password: ***********

**Executive Producer:**
- Email: `producer@test.com`
- Password: ***********

### Current JWT Tokens (Valid for 7 days from generation)

**Note:** These tokens expire after 7 days (11/3/2027).
```
ASSISTANT_TOKEN=""eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImhadjdxRUIzcGRMeTd2MU9qNXhCYyJ9.eyJpc3MiOiJodHRwczovL2Rldi0yY2hiOGJ3MHpkaDF6MXVtLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw2OGZkMzZkZWE0MDc3Mzg0N2M2MDE4YWIiLCJhdWQiOlsiZnNuZC1jYXN0aW5nLWFnZW5jeS1jYXBzdG9uZSIsImh0dHBzOi8vZGV2LTJjaGI4YncwemRoMXoxdW0udXMuYXV0aDAuY29tL3VzZXJpbmZvIl0sImlhdCI6MTc2MTYyMTYxMiwiZXhwIjoxNzYyMjI2NDEyLCJzY29wZSI6Im9wZW5pZCBwcm9maWxlIGVtYWlsIiwiZ3R5IjoicGFzc3dvcmQiLCJhenAiOiJUZmRZejlVVmc2TDFZRVVPRUlkVmZrRzdKNUR3Mlg2OSIsInBlcm1pc3Npb25zIjpbImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIl19.aHFyOcFnmWVIM1b2kD2AzOR7AOKPHL2EB6pk0l1wu1NgTKQaWlxwEFaENM2xN6OxjEYpK8tn_Mn6SnSjjfLsqd2w83j-G4nv6mcZ5cfcaXQvx-HQ-PE2w9OBBahUSPIOvURb6FjjHUcc5vYZU0bSkQWwXzeLP9ZDAdqcprFPD6wJec4Ud_rmT6w4OX71m2tXPfUiTpi2HDvKj2l5jLLQbkM_BFpZ6SUKhlsHEEb1NTRdgOSWYvBUdq0oqtDmKdLvD_7SlNgJnPeJF07FsAJocv0llh13EOUrBxZsBGe3mX1QZHXs8sGckAmR8TxkQBAIkeOgyTBIvoisHBRr4oPmXQ"
DIRECTOR_TOKEN="eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImhadjdxRUIzcGRMeTd2MU9qNXhCYyJ9.eyJpc3MiOiJodHRwczovL2Rldi0yY2hiOGJ3MHpkaDF6MXVtLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw2OGZkM2EwYTg4NTA5NTNjYmU1MGE3NGYiLCJhdWQiOlsiZnNuZC1jYXN0aW5nLWFnZW5jeS1jYXBzdG9uZSIsImh0dHBzOi8vZGV2LTJjaGI4YncwemRoMXoxdW0udXMuYXV0aDAuY29tL3VzZXJpbmZvIl0sImlhdCI6MTc2MTYyMTYxMywiZXhwIjoxNzYyMjI2NDEzLCJzY29wZSI6Im9wZW5pZCBwcm9maWxlIGVtYWlsIiwiZ3R5IjoicGFzc3dvcmQiLCJhenAiOiJUZmRZejlVVmc2TDFZRVVPRUlkVmZrRzdKNUR3Mlg2OSIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTphY3RvcnMiLCJnZXQ6YWN0b3JzIiwiZ2V0Om1vdmllcyIsInBhdGNoOmFjdG9ycyIsInBhdGNoOm1vdmllcyIsInBvc3Q6YWN0b3JzIl19.vgSyIC6tdv6Tfm5rl0qdXM9TUzDDOS5ihw15CoLM3CXBSakwln9Pdzoh8cVA5-cUoKRTvzuO9a1Ah1Q_wIoFOeNLPSOad8tM0Lg82clvpTYileyglV3jg-nPBR9wahT4NwNYmlsO9P2TlbHSpXRwtwHkPtAcRqs8wrPYbCZYaoYeifG0olEvpKVQh-MlAnLZZodKh0pXlolIcNnnATuZZLn03RMAoLvF5cUP29xdgyvb-XOKmfniV0mbzu6uFBt91jig_PVaFKca93eJzHfX0IQcJeh8wLqn-CPxUkDbst1pjKHVdR3xCz_w_cjk2GlYOdcLQ-rbaraU26GfNNlUTg"
EXECUTIVE_TOKEN="eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImhadjdxRUIzcGRMeTd2MU9qNXhCYyJ9.eyJpc3MiOiJodHRwczovL2Rldi0yY2hiOGJ3MHpkaDF6MXVtLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw2OGZkM2E2YmM3OTQwY2U2MjUyZWMwZmYiLCJhdWQiOlsiZnNuZC1jYXN0aW5nLWFnZW5jeS1jYXBzdG9uZSIsImh0dHBzOi8vZGV2LTJjaGI4YncwemRoMXoxdW0udXMuYXV0aDAuY29tL3VzZXJpbmZvIl0sImlhdCI6MTc2MTYyMTYxMywiZXhwIjoxNzYyMjI2NDEzLCJzY29wZSI6Im9wZW5pZCBwcm9maWxlIGVtYWlsIiwiZ3R5IjoicGFzc3dvcmQiLCJhenAiOiJUZmRZejlVVmc2TDFZRVVPRUlkVmZrRzdKNUR3Mlg2OSIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTphY3RvcnMiLCJkZWxldGU6bW92aWVzIiwiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiLCJwYXRjaDphY3RvcnMiLCJwYXRjaDptb3ZpZXMiLCJwb3N0OmFjdG9ycyIsInBvc3Q6bW92aWVzIl19.EZ_uhQeyeBIKFmKEg9S8v49DS1hR4PTCUQLnPdnMXT-nHrWTc4IFxu6oZkVU5sIlbMfpNtLEjiUnavPndGBPODS-0u5HBqTS2ph4s_4f-CQSYGOGu2sAx0XZ1dEckcS8cR7QL92sEeQjic-QiKitRDGLqYHU6Ee-fCUWgzvGXbonYqKIFfAzkroTBlWT6V5t1FXpgsZWkG4QeYs7eF7LcxK3vMJolqTZ4QaXKFzkuTG8Ct95qQvf8rQz8dFRt_2gUQjtk4OB3MipRfIzFgg73y-IoGLWoHZPwr52Hx2leO1yx70o0tS80dPITWoXX8c5QyXcGMnCtCEBmdCuPPUDwg"
```

## Deployment

The application is deployed on Render at: `https://render-deployment-example-b64l.onrender.com/`

**Environment Variables (set in Render dashboard):**
- `DATABASE_URL`: PostgreSQL connection string (from Render Postgres service)
- `EXCITED`: `true`
- `PYTHON_VERSION`: `3.10.15`

The app automatically redeploys when changes are pushed to the main branch on GitHub.

## Project Structure
```
capstone_sample/
├── app.py                 # Main application with routes
├── models.py              # Database models (Actors, Movies)
├── auth.py                # Auth0 authentication logic
├── test_app.py            # Unit tests
├── requirements.txt       # Python dependencies
├── runtime.txt            # Python version for Render
├── Procfile              # Gunicorn config for deployment
├── setup.sh              # Environment variables setup
└── README.md             # This file
```

## Author

**Jason B.**  
Udacity Full Stack Web Developer Nanodegree Candidate :P