FROM python:3.11.5-bookworm

LABEL maintainer="yasin-dev81.ir"
LABEL version="1.1.1"

WORKDIR /code

COPY requirements.txt /code/

# pip
RUN pip install -U pip
RUN pip install -r requirements.txt

COPY . /code/

RUN python manage.py makemigrations
RUN python manage.py migrate

EXPOSE 8000

CMD ["gunicorn", "config.wsgi", "-b", "0.0.0.0:8000"]
