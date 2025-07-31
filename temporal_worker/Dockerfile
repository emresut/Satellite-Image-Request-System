# Python 3.11 tabanlı bir resmi imaj kullanılır
FROM python:3.11-slim

# Ortam değişkenleri
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Çalışma dizinine geçilir
WORKDIR /worker

# Gerekli dosyalar kopyalanır
COPY . /worker

# Gereken Python paketleri kurulur
RUN pip install --no-cache-dir -r requirements.txt

# Worker başlatılır
CMD ["python", "-m", "temporal_worker.worker"]