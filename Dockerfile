FROM python:3.13.3-alpine
WORKDIR /app

# Update packages and apply security patches
RUN apk update && apk upgrade && apk add --no-cache --virtual .build-deps gcc musl-dev

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["python", "app.py"]