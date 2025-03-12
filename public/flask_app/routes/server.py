"""
Server side code for the python learning project
"""

import random
from flask import Blueprint, render_template, jsonify, request
from .pvar.global_f import *
from .model.check_gen import *

main_blueprint = Blueprint("main", __name__)
question_data = interpret_csv()


def gen_question(level):
    """
    Create a new question
    """
    question = create_question(level)

    if "error" in question:
        # If an error occured then let the user know. Stops crashing
        question = {"question": "ERROR OCCURRED WITH GENERATING QUESTION", "level": 0}
        print("ERROR HAS OCCURRED WHEN CREATING NEW QUESTION")

    return question


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


@main_blueprint.route("/api/questions", methods=["GET"])
def get_questions():
    """
    Send data to client as JSON
    """
    req_level = request.args.get("level", default="1")
    temp_q_arr = [x for x in question_data if x["level"] == int(req_level)]

    if len(temp_q_arr) <= 0:
        random_q = gen_question(req_level)
    else:
        random_q = random.choice((temp_q_arr))

    return jsonify(random_q)


@main_blueprint.route("/json/mark", methods=["POST"])
def check_answer():
    """
    Get JSON data from client
    """
    data = request.get_json()
    check = grade_question(data["answer"], data["question"], data["level"])

    if "error" in check:
        # If an error occured then let the user know. Stops crashing
        check = {"feedback": "ERROR OCCURRED WITH MARKING", "total_mark": 0}

    return {"result": check}


@main_blueprint.route("/json/username", methods=["POST"])
def get_username():
    """
    Get data from database with username
    """
    data = request.get_json()

    username, password = data["user"], data["pass"]
    all_users = open_json("public/flask_app/routes/users.json", "r")
    response_data = {"success": False, "level": 1}

    for user in all_users:
        if user["username"] == username and user["password"] == password:
            response_data = {"success": True, "level": user["level"]}
            break

    return jsonify(response_data)

@main_blueprint.route("/json/update", methods=["POST"])
def update_user_details():
    """
    Update user information in users.json
    """
    user_found = False
    result = False
    data = request.get_json()
    tar_user = data["user"]
    new_level = data["level"]
    
    all_users = open_json("public/flask_app/routes/users.json", "r")
    
    for user in all_users:
        if user["username"] == tar_user:
            user["level"] = new_level
            user_found = True
            break
    
    if user_found:
        with open("public/flask_app/routes/users.json", "w") as file:
            json.dump(all_users, file, indent=4)
            result = True
    else:
        print("No user found")
    
    return {"Success": result}
