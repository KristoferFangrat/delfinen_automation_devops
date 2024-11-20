# Start from the official Python 3.11 image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /streamlit_app.py

# Copy the requirements file to the container
COPY requirements.txt .

# Install virtualenv
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your application code to the container
COPY . .

# Copy the service account key file to the container
COPY service-account-key.json /app/service-account-key.json

# Set environment variable for Google Application Credentials
ENV GOOGLE_APPLICATION_CREDENTIALS="/app/service-account-key.json"

# Expose the port Streamlit will run on
EXPOSE 8080

# Command to run the Streamlit app
CMD ["streamlit", "run", "streamlit_app.py", "--server.port=8080"]
