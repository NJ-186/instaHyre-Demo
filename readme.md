This is a demo for Instahyre - Full Stack Developer Position.

For Populating the database, run:-

python manage.py populate --users m --global n

where 1 < m < 40 and n 1 < n < 30

Eg:- if you want to add 5 users and 10 global users (total becomes 15 -> after adding 5 registered users), command will be - python manage.py populate --users 5 -- global 10

For running the server:- 

First install all the dependencies from requirements.txt --> pip install -r requirements.txt

Then makemigrations --> python manage.py makemigrations

Then migrate --> python manage.py migrate

Then runserver --> python manage.py runserver

All the APIs are pretty self explanatory