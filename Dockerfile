FROM python:3.11.5-slim

WORKDIR /app

COPY . /app



RUN pip install -r requirements.txt
# Run playwright install to ensure all browsers are downloaded
RUN playwright install --with-deps