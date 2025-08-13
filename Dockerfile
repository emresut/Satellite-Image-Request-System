# Python 3.11 based image is used
FROM python:3.11-slim

# env variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV FLASK_APP=app.py

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN pip install -r requirements.txt

# port 5000
EXPOSE 5000

# to start the flask application
CMD ["flask", "run", "--host=0.0.0.0"]