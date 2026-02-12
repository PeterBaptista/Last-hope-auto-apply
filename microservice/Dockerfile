FROM python:3.10-slim

# Install system dependencies required for Selenium/Chrome
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    unzip \
    xvfb \
    libxi6 \
    libgconf-2-4 \
    libnss3 \
    default-jdk \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Install SeleniumBase browsers/drivers
RUN seleniumbase install chromedriver
RUN seleniumbase install geckodriver

# Copy application code
COPY . .

# Expose port (if needed for API)
EXPOSE 8000

# Start command
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
