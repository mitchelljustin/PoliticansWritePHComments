import pymongo
from os import environ

client = pymongo.MongoClient(environ.get('MONGODB_URL', 'webdb'))
db = client['porniticians']
markov_dict = db['markov_dict']
comments = db['comments']

PREFIX_LEN = 3
SYMS_START = ['__start{}__'.format(i) for i in range(PREFIX_LEN)]
SYMS_END = ['__end{}__'.format(i) for i in range(PREFIX_LEN)]