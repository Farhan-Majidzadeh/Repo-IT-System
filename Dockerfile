FROM python:3.11-slim

WORKDIR /app

RUN pip install --no-cache-dir django==4.2.7 django-jalali django-unfold

COPY . .

EXPOSE 8000

CMD ["sh", "-c", "python manage.py migrate --noinput && python manage.py collectstatic --noinput 2>/dev/null; python manage.py runserver 0.0.0.0:8000"]
