FROM python:3.13-slim

WORKDIR /app

RUN apt-get update && apt-get install -d -y gcc default-libmysqlclient-dev pkg-config && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["python", "mwu/main.py"]