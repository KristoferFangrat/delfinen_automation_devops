FROM python:3.11.8

WORKDIR /app

# Kopiera och installera beroenden
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Kopiera resten av applikationen
COPY . .

# Exponera porten som Streamlit körs på
EXPOSE 8080

# Starta Streamlit-applikationen
CMD ["streamlit", "run", "streamlit_app.py", "--server.port=8080", "--server.address=0.0.0.0"]