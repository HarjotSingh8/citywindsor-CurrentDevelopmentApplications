# Use the official Python image as the base image
FROM python:3.9-slim

# Add the environment variable to ensure Python output is unbuffered
ENV PYTHONUNBUFFERED=1

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt ./

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . .

# Set the default command to run the scraper script
CMD ["python", "scraper.py"]