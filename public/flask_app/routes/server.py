""" 
Server side code for the python learning project
"""

import sys
import os
import psycopg2
import random
from dotenv import load_dotenv
from flask import Blueprint, render_template, jsonify, request
from .pvar.global_f import *
from .model.check_gen import *

main_blueprint = Blueprint("main", __name__)

question_data = interpret_csv()
user_data = {"userID": 0, "level": 1, "score": 0}

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

def connect_to_db():
    load_dotenv()
    DB_USER = os.getenv("fyp_db_user")
    DB_PASS = os.getenv("fyp_db_pass")

    conn = psycopg2.connect(
        database="fyp_db", user=DB_USER, password=DB_PASS, host="0.0.0.0", port="5432"
    )

    return conn


# how to use db in code
# conn = connect_to_db()
# cur = conn.cursor()

# # cur.execute()
# conn.commit()

# cur.close()
# conn.close()


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
