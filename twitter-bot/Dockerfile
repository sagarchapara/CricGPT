# Base image with Python
FROM python:3.13-slim

# Set working directory in the container
WORKDIR /app/server

# Copy only requirements.txt first (from the server folder)
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the server files
COPY . .

#Start the bot
CMD ["python", "process.py"]
