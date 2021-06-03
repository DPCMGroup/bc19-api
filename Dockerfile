FROM python:3.7

COPY . .

RUN pip install -r requirements.txt && python manage.py migrate

