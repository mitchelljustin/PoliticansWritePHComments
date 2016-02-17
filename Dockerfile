FROM python:3.5.1-alpine

RUN mkdir -p /app
WORKDIR /app

ADD requirements.txt /app
RUN pip install -r requirements.txt

ADD . /app

EXPOSE 8001

CMD ["gunicorn", "-b", "0.0.0.0:8001", "app:app", "--log-file=-"]