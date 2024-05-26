# Temel imaj olarak Python kullanıyoruz
FROM python:3.12.3-bullseye

# Çalışma dizinini ayarlıyoruz
WORKDIR /app

# Gereken sistem bağımlılıklarını yüklüyoruz
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Gereken Python paketlerini yüklüyoruz
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Uygulama kodlarını kopyalıyoruz
COPY . .

# Çalışma zamanı komutları
CMD ["daphne", "-b", "0.0.0.0", "-p", "8000", "sokakagzi.asgi:application"]