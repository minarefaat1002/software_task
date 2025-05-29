FROM python:3.12.7

WORKDIR /app

COPY ./api/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY ./api /app

CMD ["fastapi", "dev", "--host", "0.0.0.0", "--port", "80"]
