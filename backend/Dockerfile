FROM python:3.12

RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /backend/app

COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

RUN python -c "import nltk; nltk.download('punkt')"

COPY alembic.ini /backend/app/alembic.ini
COPY alembic /backend/app/alembic
COPY . /backend/app/

COPY entrypoint.sh /backend/app/
RUN chmod +x /backend/app/entrypoint.sh

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
