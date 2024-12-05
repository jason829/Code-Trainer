'''
Flask research and experimentation
only will be a basic ui for now
'''
from flask import Flask, render_template
from markupsafe import escape

app = Flask(__name__)

@app.route('/')
def index():
    '''
    Home Page
    '''
    return render_template("index.html")


