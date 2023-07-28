# syntax=docker/dockerfile:1

FROM python:3.11

WORKDIR /api

COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["gunicorn", "main:app"]
