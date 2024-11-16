# Start from the official Python 3.11 image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /streamlit_app

# Copy the requirements file to the container
COPY requirements.txt .

# Install the dependencies from requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your application code to the container
COPY . .

# Expose the port Streamlit will run on
EXPOSE 8080

# Command to run the Streamlit app
CMD ["streamlit", "run", "streamlit_app.py", "--server.port=8080", "--server.address=0.0.0.0"]
