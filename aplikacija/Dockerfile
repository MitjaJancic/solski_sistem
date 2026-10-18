FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    default-libmysqlclient-dev \
    build-essential \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
RUN chmod +x entrypoint.sh

EXPOSE 8000

ENTRYPOINT ["./entrypoint.sh"]
# Privzeto (produkcija): aplikacijski strežnik gunicorn.
# Razvojni docker-compose.override.yml ta ukaz zamenja z `runserver`.
CMD ["gunicorn", "solski_sistem.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3"]
