FROM python:3.9

# Gerekli bağımlılıkları yükle
RUN apt-get update && apt-get install -y \
    libnss3 \
    libatk-bridge2.0-0 \
    libatk1.0-0 \
    libcups2 \
    libdbus-1-3 \
    libxkbcommon0 \
    libatspi2.0-0 \
    libxcomposite1 \
    libxdamage1 \
    libxfixes3 \
    libxrandr2 \
    libgbm1 \
    libasound2

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Playwright'ı yükle ve DOCKER=1 ortam değişkenini ayarla
ENV DOCKER=1
RUN playwright install

COPY . .

# Docker ağı yapılandırmasını güncelle
CMD ["python", "crawler.py", "--network", "host"]
