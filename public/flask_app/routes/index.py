'''
Flask research and experimentation
only will be a basic ui for now
'''
from flask import Blueprint, render_template

main_blueprint = Blueprint("main", __name__)

@main_blueprint.route('/')
def index():
    '''
    Home Page
    '''
    return render_template("index.html")


