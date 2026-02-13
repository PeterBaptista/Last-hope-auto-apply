from fastapi import FastAPI
import threading
from .consumer import start_consumer
from .scraper import scrape_job_vacancy
from .payload_client import create_job_vacancy
from pydantic import BaseModel

app = FastAPI()

class ScrapeRequest(BaseModel):
    url: str

@app.on_event("startup")
async def startup_event():
    # Start the RabbitMQ consumer in a separate thread
    consumer_thread = threading.Thread(target=start_consumer, daemon=True)
    consumer_thread.start()

@app.post("/scrape-jobs")
async def scrape_jobs_endpoint(request: ScrapeRequest):
    """
    Endpoint to trigger job scraping and save to Payload CMS.
    """
    # 1. Scrape the job details
    scraped_data = scrape_job_vacancy(request.url)

    if "error" in scraped_data:
         return {"status": "failed", "error": scraped_data["error"]}

    # 2. Save to Payload CMS
    payload_response = create_job_vacancy(scraped_data)

    if payload_response:
        return {"status": "success", "data": payload_response}
    else:
        return {"status": "partial_success", "message": "Scraped but failed to save to Payload", "scraped_data": scraped_data}

@app.get("/")
def read_root():
    return {"status": "Microservice is running", "service": "Scraper with RabbitMQ & SeleniumBase"}

@app.get("/health")
def health_check():
    return {"status": "ok"}
