FROM python:3.10

WORKDIR src/


ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN python3 -m pip install --upgrade pip

COPY . .

RUN python3 -m pip install -r requirements.txt

