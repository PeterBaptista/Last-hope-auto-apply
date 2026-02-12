from seleniumbase import SB

def scrape(url: str):
    """
    Scrapes the given URL using SeleniumBase in UC mode.
    """
    print(f"Starting scrape for: {url}")
    try:
        with SB(uc=True, test=True, headless=True) as sb:
            sb.open(url)
            # Example scraping logic - modify as needed for specific targets
            title = sb.get_title()
            print(f"Successfully scraped title: {title}")
            return {"url": url, "title": title, "status": "success"}
    except Exception as e:
        print(f"Error scraping {url}: {e}")
        return {"url": url, "error": str(e), "status": "failed"}

def process_message(body):
    """
    Process the message body from RabbitMQ.
    Expected body to be a URL string or JSON containing a URL.
    """
    import json
    try:
        data = json.loads(body)
        url = data.get("url")
    except json.JSONDecodeError:
        url = body.decode("utf-8") if isinstance(body, bytes) else body

    if url:
        return scrape(url)
    else:
        print("No URL found in message")
        return None
