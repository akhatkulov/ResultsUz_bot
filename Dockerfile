FROM python:3.11-slim

ENV APP_HOME=/app

RUN mkdir -p $APP_HOME
WORKDIR $APP_HOME

COPY . .

RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    python3-dev \
    gettext

RUN pip install -U pip && \
    pip install -r requirements.txt

CMD ["python3", "app.py"]
