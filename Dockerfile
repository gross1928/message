# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy the dependencies file to the working directory
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the content of the local src directory to the working directory
# Copy the application code
COPY src/ ./src
COPY main.py .

# Command to run the application
# Command to run the main application runner
CMD ["python", "main.py"]
