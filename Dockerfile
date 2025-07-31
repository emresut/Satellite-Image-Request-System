# Python 3.11 tabanlı bir resmi imaj kullanılır
FROM python:3.11-slim

# Ortam değişkenleri bunlardır
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV FLASK_APP=app.py

# Çalışma dizini oluşturulur ve ayarlanır
WORKDIR /app

# Gereksiz önbellek dosyaları ve __pycache__'leri dahil etmemek için
COPY . /app

# Gerekli kütüphaneler kurulur
RUN pip install -r requirements.txt

# 5000 portu açılır
EXPOSE 5000

# Flask uygulaması başlatılır
CMD ["flask", "run", "--host=0.0.0.0"]