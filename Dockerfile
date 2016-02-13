FROM python

RUN mkdir -p /app
WORKDIR /app

ADD requirements.txt /app
RUN pip install -r requirements.txt

ADD . /app

ENV PORT=8000
EXPOSE 8000

ENV DEBUG=false 

CMD ["python", "run_server.py"]