# Python 3.11 based image is used
FROM python:3.11-slim

# env variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /worker

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# to start the worker
CMD ["python", "-m", "temporal_workflow.worker"]