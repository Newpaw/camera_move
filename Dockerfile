# Použití oficiálního Python obrazu jako základ
FROM python:3.12

# Nastavení pracovní složky v kontejneru
WORKDIR /app

# Kopírování requirements.txt a instalace závislostí
COPY requirements.txt .
RUN pip install -r requirements.txt

# Instalace závislostí pro OpenCV, ffmpeg a nginx
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    ffmpeg \
    nginx

# Kopírování obsahu projektu do pracovní složky
COPY . .

# Konfigurace NGINX pro serverování videí
RUN echo 'server { \
    listen 80; \
    location /videos { \
        alias /app/videos; \
        autoindex on; \
    } \
}' > /etc/nginx/sites-available/default

# Spuštění NGINX a Python aplikace
CMD ["sh", "-c", "service nginx start && python main.py"]