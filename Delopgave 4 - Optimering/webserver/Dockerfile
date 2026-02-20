FROM python:3.11

RUN apt-get update && apt-get install -y \
    vim \
    nano \
    curl \
    wget \
    git \
    build-essential \
    gcc \
    g++ \
    make

WORKDIR /app

COPY . .

RUN pip install flask psycopg2-binary pandas numpy scipy requests beautifulsoup4

CMD python app.py
