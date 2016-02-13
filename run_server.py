from app import app
from os import environ

debug = (environ.get('DEBUG', '') == 'true')

port = int(environ['PORT']) or 8000
app.run(debug=debug, port=port, host='0.0.0.0')
