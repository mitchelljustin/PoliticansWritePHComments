FROM python

RUN mkdir -p /app
WORKDIR /app

ADD requirements.txt /app
RUN pip install -r requirements.txt

ADD . /app

EXPOSE 8000

CMD ["gunicorn", "-b", "0.0.0.0:8000", "app:app", "--log-file=-"]