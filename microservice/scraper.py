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

def scrape_job_vacancy(url: str):
    """
    Scrapes a job vacancy page for details.
    """
    print(f"Starting job scrape for: {url}")
    try:
        with SB(uc=True, test=True, headless=False, headed=True) as sb:
            sb.open(url)

            # Generic scraping logic (to be improved for specific sites)
            title = sb.get_title()

            # Try to find common elements for job details
            company = ""
            location = ""
            description = ""

            # Heuristic: First H1 is often the title (already got title from metadata, but H1 is better)
            if sb.is_element_visible("h1"):
                title = sb.get_text("h1")

            # Heuristic: Company often in H2 or class containing 'company'
            # This is very generic and might strictily need adjustment per site

            # Get all text to use as description for now if no specific container found
            # Or try to find a main article/content
            if sb.is_element_visible("main"):
                description = sb.get_text("main")
            elif sb.is_element_visible("article"):
                description = sb.get_text("article")
            else:
                description = sb.get_text("body")

            print(f"Successfully scraped job: {title}")
            return {
                "title": title,
                "company": company, # Placeholder
                "location": location, # Placeholder
                "description": description[:2000], # Limit length for now
                "applicationLink": url,
                "source": "Web Scraper"
            }
    except Exception as e:
        print(f"Error scraping job {url}: {e}")
        return {"error": str(e)}
