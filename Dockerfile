FROM python:3.7

RUN mkdir usr/app

WORKDIR usr/app

COPY . .

RUN pip install -r requirements.txt && python manage.py migrate

CMD python manage.py runserver 0.0.0.0:8000

EXPOSE 8000
