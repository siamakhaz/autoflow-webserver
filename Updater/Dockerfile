# Use an official Python runtime as a parent image
FROM python:3.8-alpine

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy the dependencies file to the working directory
COPY requirements.txt .

# Install any dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Install Git
RUN apk add --no-cache git openssh

# Copy the content of the local src directory to the working directory
COPY src/ .

# Run the application
CMD [ "python", "./updater.py" ]
