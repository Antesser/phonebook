**API for storing phones and addresses**

This is a test FastAPI application that allows you to upload phone numbers and addresses in order to store them via Redis

To run this app kindly use:
```zsh
docker compose up --build
```
Then use Swagger on http://localhost:5000/docs or just send requests via endpoints check_data and write_data

For check_data you should send data in header like http://localhost:5000/check_data?phone=89541627281 

As for write_data endpoint JSON similar to {"phone": "89541627281","address": "Moscow"} should be sent in request body towards http://localhost:5000/write_data/ in order to add POST or update PATCH information in DB


**Second task**

I've actually recreated tables short_names with 700k and full_names with 500k records to test my ~~not really~~marvellous queries:

1) Query died trying, but it *surely* works if you have ~20-30 records
```zsh
UPDATE full_names
SET status = (
select status from short_names
where short_names.name=regexp_replace(full_names.name, '\.(.*)', ''))
where exists(
select 1 from short_names
where short_names.name=regexp_replace(full_names.name, '\.(.*)', '')
);
```
Regex is kinda: u have a problem, wanna use a regex? well, u have 2 problems now. or it's due to my lack of skill, both sound plausible.

2) Query returned successfully in 1 secs 990 msec.
```zsh
UPDATE full_names
set status=short_names.status
from short_names 
where short_names.name=left(full_names.name, position('.' in full_names.name)-1); 
```
3) Query returned successfully in 1 secs 623 msec.
```zsh
UPDATE full_names
set status=short_names.status
from short_names 
where short_names.name=left(full_names.name, strpos(full_names.name, '.')-1);
```
In 2 and 3 we're doing similar search of a location with dot and than substracting the remaining name

4) Query returned successfully in 2 secs 338 msec.
```zsh
UPDATE full_names
SET status = short_names.status
FROM short_names 
WHERE short_names.name = substr(full_names.name, 1, length(full_names.name) - position('.' in reverse(full_names.name)));
```
In this one we insure that even if name contains more than one dot we find the first point in the inverted line and subtract the resulting number from the total length. This gives us its position in the non-inverted line.