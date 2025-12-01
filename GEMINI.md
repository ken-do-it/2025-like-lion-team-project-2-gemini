# Gemini Project Context: Music Sharing SNS Backend

## Project Overview

This project is the backend for a music sharing social media platform. It's built with Python and FastAPI, following a detailed architectural design. The frontend is expected to be a React application, but this context focuses solely on the backend.

The architecture is designed to be scalable and modular, with key features including music uploading/streaming, user profiles, likes, comments, playlists, and more.

## Key Technologies

- **Framework:** FastAPI
- **Database:** PostgreSQL (with SQLAlchemy ORM and Alembic for migrations)
- **Authentication:** JWT (RS256) verification. Tokens are issued by a separate, external "Auth Server". This backend is only responsible for validating the tokens.
- **Caching:** Redis is used for caching frequently accessed data like track metadata, user profiles, and JWT public keys (JWKS).
- **File Storage:** AWS S3 is used for storing all music files. Uploads are handled securely using presigned URLs.
- **Deployment:** The target production environment is Docker containers on AWS EC2, managed with Nginx as a reverse proxy.

## Building and Running

As the project is in its initial setup phase, the commands are standard for a FastAPI application.

1.  **Create a virtual environment (Recommended):**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

2.  **Install dependencies:**
    A `requirements.txt` file needs to be created. Based on the architecture, it should contain:
    ```
    fastapi
    uvicorn[standard]
    sqlalchemy
    psycopg2-binary
    alembic
    redis
    boto3
    python-jose[cryptography]
    python-dotenv
    ```
    To install:
    ```bash
    pip install -r team_2_music_back/requirements.txt
    ```

3.  **Set up environment variables:**
    Create a `.env` file in the `team_2_music_back` directory for local development:
    ```env
    DATABASE_URL="postgresql://user:password@host:port/database"
    REDIS_HOST="localhost"
    REDIS_PORT="6379"
    AWS_ACCESS_KEY_ID="your_key"
    AWS_SECRET_ACCESS_KEY="your_secret"
    S3_BUCKET_NAME="your_bucket_name"
    AUTH_SERVER_JWKS_URL="https://your-auth-server.com/.well-known/jwks.json"
    ```

4.  **Run database migrations:**
    ```bash
    # Inside team_2_music_back directory
    alembic upgrade head
    ```

5.  **Run the development server:**
    ```bash
    # Inside team_2_music_back directory
    uvicorn app.main:app --reload
    ```

## Development Conventions

- **Phased Development:** The project follows a phased approach, starting with core architecture and progressively adding features like user interactions, playlists, and notifications.
- **Modular Design:** The backend is organized into "Skills" or domain modules (e.g., `user-profile`, `music-upload`, `interaction-like-comment`). Each module has a specific responsibility.
- **API Versioning:** All API endpoints are prefixed with `/api/v1/`.
- **Music Upload Flow:** A three-step process is used for uploads:
    1.  **Initiate:** The client requests a presigned URL from the backend.
    2.  **Upload:** The client uploads the file directly to S3 using the presigned URL.
    3.  **Finalize:** The client notifies the backend that the upload is complete, and the backend creates the track metadata in the database.
- **Testing:** The strategy includes unit tests for core logic, integration tests for API flows, and optional E2E tests. Tests are intended to be run automatically via GitHub Actions on pull requests.
