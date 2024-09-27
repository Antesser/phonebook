**API for storing phones and addresses**

This is a test FastAPI application that allows you to upload phones and addresses and store them via Redis

In order to run this app kindly use:
```zsh
docker compose up --build
```
Then use Swagger on http://localhost:5000/docs or just send requests via endpoints check_data and write_data

For check_data you should  send  data in header like http://localhost:5000/check_data?phone=800000000 

As for write_data JSON {"phone": "800000000","address": "Moscow"} should be sent in request body towards http://localhost:5000/write_data/ in order to add or update information in DB


**Second task**

I've actually recreated tables short_names with 700k and full_names with 500k records to test my ~~not really~~marvellous queries:

1) Query died trying, but it *surely* works if you have ~20-30 records

UPDATE full_names
SET status = (
select status from short_names
where short_names.name=regexp_replace(full_names.name, '\.(.*)', ''))
where exists(
select 1 from short_names
where short_names.name=regexp_replace(full_names.name, '\.(.*)', '')
);

regex is kinda: u have a problem, wanna use a regex? well, u have 2 problems now. or it's due to my lack of skill, both sound plausible.

2) Query returned successfully in 1 secs 990 msec.

UPDATE full_names
set status=short_names.status
from short_names 
where short_names.name=left(full_names.name, POSITION('.' in full_names.name)-1); 


3) Query returned successfully in 1 secs 623 msec.

UPDATE full_names
set status=short_names.status
from short_names 
where short_names.name=left(full_names.name, strpos(full_names.name, '.')-1);

2nd and 3rd are similar though
