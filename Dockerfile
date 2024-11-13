FROM python:3.11-slim-buster

WORKDIR /streamlit_app

# Kopiera och installera beroenden
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

# Kopiera resten av applikationen
COPY . .

# Exponera porten som Streamlit körs på
EXPOSE 8080

# Starta Streamlit-applikationen
CMD ["streamlit", "run", "streamlit_app.py", "--server.port=8080", "--server.address=0.0.0.0"]