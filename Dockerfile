# Use official lightweight Python image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy and install dependencies
COPY app/requirements.txt .
RUN pip install -r requirements.txt

# Copy application code
COPY app/ .

# Expose service port
EXPOSE 5000

# Run the application
CMD ["python", "main.py"]
