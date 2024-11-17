# Start from the official Python 3.11 image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file to the container
COPY requirements.txt .

# Install virtualenv
RUN pip install --no-cache-dir virtualenv

# Create a virtual environment
RUN virtualenv venv

# Activate the virtual environment and install dependencies
RUN . venv/bin/activate && pip install --no-cache-dir -r requirements.txt

# Copy the rest of your application code to the container
COPY . .

# Expose the port Streamlit will run on
EXPOSE 8080

# Command to run the Streamlit app
CMD ["streamlit", "run", "streamlit_app.py", "--server.port=8080"]
