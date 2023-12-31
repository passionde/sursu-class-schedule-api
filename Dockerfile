FROM python:3.9-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY requirements.txt /app/
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY . /app/

CMD ["uvicorn", "api.app:app", "--host", "0.0.0.0", "--port", "8080", "--log-level", "info", "--log-config", "log.ini"]
