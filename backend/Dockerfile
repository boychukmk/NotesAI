FROM python:3.12

RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /backend

COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

RUN python -c "import nltk; nltk.download('punkt')"

COPY . /backend

RUN chmod +x /backend/entrypoint.sh

EXPOSE 8000

ENTRYPOINT ["/backend/entrypoint.sh"]
