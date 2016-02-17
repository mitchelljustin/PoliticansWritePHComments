FROM python:3.5.1-alpine

RUN mkdir -p /app
WORKDIR /app

ADD requirements.txt /app
RUN pip install -r requirements.txt

ADD . /app

EXPOSE 8001

CMD ["python", "run_server.py"]