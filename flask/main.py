'''
Flask research and experimentation
only will be a basic ui for now
'''
from flask import Flask
from markupsafe import escape

app = Flask(__name__)

@app.route('/')
def index():
    return 'Index Page'

@app.route('/hello')
def hello_world():
    '''
    test
    '''
    return f"hello, world" # this is for safety to avoid harmful injections
