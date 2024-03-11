FROM python:3.10.12

WORKDIR /usr/src/app

COPY ./requirements.txt .

COPY . /usr/src/app/

RUN pip install --upgrade pip \
    && pip install -r requirements.txt
