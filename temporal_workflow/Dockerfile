# Python 3.11 based image is used
FROM python:3.11-slim

# env variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /worker

COPY . /worker

RUN pip install --no-cache-dir -r requirements.txt

# to start the worker
CMD ["python", "-m", "worker"]