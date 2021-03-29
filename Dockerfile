FROM python:3.7

RUN mkdir usr/app

COPY . .

RUN pip install -r requirements.txt

CMD python manage.py runserver 8000

EXPOSE 80
