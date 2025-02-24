# Jason Nghiem - UOP Final year project

## Link to documents

- [General notes](https://docs.google.com/document/d/1b6HnAn6ybo2X5j6eZODDUxaw9Kp-SIuVymI8jHa9hO4/edit?usp=sharing)

## Setup

- Create python virtual environment (python 3.12)
- install libraries in requirements.txt
- Create database, ensure you have PostgreSQL installed on your machine and run [this file](public/flask_app/routes/init_db.py)
- run [this file for locally, production use please use the command below](public/run.py)

## Docker set up soon, gunicorn command

gunicorn -w 4 -b 0.0.0.0:8000 "public.flask_app:create_app()"
