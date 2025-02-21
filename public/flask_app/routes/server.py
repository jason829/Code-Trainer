""" 
Server side code for the python learning project
"""
import sys
import os
from flask import Blueprint, render_template, jsonify, request
from .pvar.global_f import interpret_csv, check_answer
from .model.check_gen import grade_question, create_question

# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))
# from questionInit.question_tree import populate_tree
# answer = populate_tree(os.path.abspath(os.path.join(os.path.abspath(__file__), "../../../questionInit/static_questions.csv")))

# print(open_csv("public/flask_app/routes/pvar/all_questions.csv"))
# csv_data = open_csv("public/flask_app/routes/pvar/all_questions.csv")
main_blueprint = Blueprint("main", __name__)

client_data, server_data = interpret_csv()[0], interpret_csv()[1]
user_data = {"userID": 0, "level": 1, "score": 0}

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
    Send data to client as JSON
    """  
    return jsonify(client_data)

@main_blueprint.route("/json", methods=["POST"])
def get_json():
    """
    Get JSON data from client
    I need to change this from check_answer to using grade_question when its done ++++++++++++++++++++++++++
    """
    data = request.get_json()
    
    question = server_data[data["id"]]["question"]
    check = grade_question(data["answer"], question)
    print(check)

    formatted_answer = check.split("</think>")[1]
    print(formatted_answer)
    
    answer = check_answer(data, server_data)
    return {"result": answer}