FROM python:3.11-slim

WORKDIR /app

RUN pip install django==4.2.7 django-jalali

COPY . .

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
