## OCR


```
docker-compose build
docker-compose up

docker-compose up -d

docker-compose logs -f app
docker-compose logs app

heroku stack:set container --app tesseract-service
heroku logs -t --app tesseract-service --source app
```
