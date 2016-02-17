from os import environ
from app import app

debug = (environ.get('DEBUG', 'true') == 'true')
app.run(debug=debug, port=8001, host='0.0.0.0')
