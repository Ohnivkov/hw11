# hw11 — Contacts API

A homework project from my GoIT Python course (2024). It is a small REST API for storing
contacts, written with FastAPI.

## What it can do

- sign up, log in and get a JWT token
- confirm the account by email
- add, edit, delete and search contacts (by name, surname or email)
- show contacts who have a birthday in the next days
- upload an avatar (Cloudinary)
- limit how often some routes can be called (Redis)

## What I used

FastAPI, SQLAlchemy, Alembic, PostgreSQL, Redis, Docker Compose, pytest, Sphinx for docs.

## How to run

1. Copy `.env.example` to `.env` and fill in your values.
2. Start PostgreSQL and Redis:

   ```bash
   docker compose up -d
   ```

3. Apply migrations and start the app:

   ```bash
   alembic upgrade head
   python main.py
   ```

4. Open <http://localhost:8000/docs> to try the API.

Tests: `pytest test/`
