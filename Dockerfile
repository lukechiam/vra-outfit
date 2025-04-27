FROM python:alpine

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY ./app .

EXPOSE 80

CMD ["gunicorn", "-c", "gunicorn_config.py", "app:app"]
