# Microservice Scraper

This is a FastAPI-based microservice that listens to RabbitMQ messages and performs web scraping using SeleniumBase.

## Prerequisites

- Python 3.9+
- Docker & Docker Compose (for RabbitMQ)

## Local Setup

1.  **Create a Virtual Environment**:

    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

2.  **Install Dependencies**:

    ```bash
    pip install -r requirements.txt
    seleniumbase install
    ```

3.  **Start RabbitMQ**:
    This will start RabbitMQ with the Management UI.

    ```bash
    docker-compose up -d
    ```

    - Access UI: [http://localhost:15672](http://localhost:15672)
    - Username: `guest`
    - Password: `guest`

4.  **Run the Microservice**:
    ```bash
    ./run.sh
    ```
    OR
    ```bash
    uvicorn main:app --reload
    ```

## deployment (Railway)

This project includes a `Dockerfile` optimized for Railway.

1.  Push this code to a GitHub repository.
2.  Connect your repository to Railway.
3.  Add a generic Service for RabbitMQ in Railway or use an external provider (e.g., CloudAMQP).
4.  Set the environment variables in Railway:
    - `RABBITMQ_HOST`
    - `RABBITMQ_PORT`
    - `RABBITMQ_USER`
    - `RABBITMQ_PASSWORD`
    - `RABBITMQ_QUEUE`

## API Endpoints

- `GET /`: Status check.
- `GET /health`: Health check.

## Testing

Publish a message to the `scraping_tasks` queue:

```json
{ "url": "https://example.com" }
```
