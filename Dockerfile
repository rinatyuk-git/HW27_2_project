FROM python:3.12-slim

WORKDIR /app

#COPY /requirements.txt /

#RUN apt-get update
#RUN apt-get -y install gcc

#RUN pip install -r /requirements.txt --no-cache-dir

COPY pyproject.toml .
RUN pip install --upgrade pip
RUN apt-get update
RUN apt-get -y install gcc
RUN pip install poetry

RUN poetry config virtualenvs.create false
RUN poetry install --no-root --no-dev

COPY . .

CMD ["sh", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:8000 "]
