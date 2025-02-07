""" 
Flask research and experimentation
only will be a basic ui for now
"""
import sys
import os
from flask import Blueprint, render_template, jsonify, request

# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))
# from questionInit.question_tree import populate_tree
from .pvar.main import open_csv

# test = populate_tree(os.path.abspath(os.path.join(os.path.abspath(__file__), "../../../questionInit/static_questions.csv")))

# print(open_csv("public/flask_app/routes/pvar/all_questions.csv"))
test = open_csv("public/flask_app/routes/pvar/all_questions.csv")
main_blueprint = Blueprint("main", __name__)
    
@main_blueprint.route("/")
def index():
    """
    Home Page
    """
    return render_template("index.html")

@main_blueprint.route("/question")
def question():
    """ 
    Questions page:
    displays question and text box
    """
    return render_template("question.html")

@main_blueprint.route("/api/questions")
def get_questions():
    """
    Return tree nodes to question.html as JSON
    """
    data = test
    return jsonify(data)

@main_blueprint.route("/json", methods=["POST"])
def get_json():
    """
    Get JSON data from front-end
    """
    data = request.get_json()
    
    print(data) # check, reuse function for checking
    return data
