**API for storing phones and addresses**

This is a test FastAPI application that allows you to upload phones and addresses and store them via Redis

In order to run this app kindly use:
```zsh
docker compose up --build
```
Then use Swagger on http://localhost:5000/docs or just send requests via endpoints check_data and write_data

For check_data you should  send  data in header like http://localhost:5000/check_data?phone=800000000 

As for write_data JSON {"phone": "800000000","address": "Moscow"} should be sent in request body towards http://localhost:5000/write_data/ in order to add or update information in DB
