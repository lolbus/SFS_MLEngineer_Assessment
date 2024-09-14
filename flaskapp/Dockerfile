# Use an official Python 3.12 runtime as a parent image
FROM python:3.12-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . .

# Install the required packages
RUN pip install --no-cache-dir Flask==3.0.3 joblib==1.4.2 pandas==2.2.2 scikit-learn==1.5.2  waitress==3.0.0

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Run the application using Waitress
CMD ["waitress-serve", "--host=0.0.0.0", "--port=5000", "flask_app:app"]