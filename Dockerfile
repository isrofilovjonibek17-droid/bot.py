FROM python:3.9-slim

# Tizimga ffmpeg o'rnatish
RUN apt-get update && apt-get install -y ffmpeg && apt-get clean

WORKDIR /app

# Kutubxonalarni o'rnatish
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Botni ishga tushirish
CMD ["python", "main.py"]
