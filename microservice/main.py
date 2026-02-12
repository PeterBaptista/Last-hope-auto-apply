from fastapi import FastAPI
import threading
from .consumer import start_consumer

app = FastAPI()

@app.on_event("startup")
async def startup_event():
    # Start the RabbitMQ consumer in a separate thread
    consumer_thread = threading.Thread(target=start_consumer, daemon=True)
    consumer_thread.start()

@app.get("/")
def read_root():
    return {"status": "Microservice is running", "service": "Scraper with RabbitMQ & SeleniumBase"}

@app.get("/health")
def health_check():
    return {"status": "ok"}
