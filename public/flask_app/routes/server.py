""" 
Server side code for the python learning project
"""

import sys
import os
import psycopg2
from dotenv import load_dotenv
from flask import Blueprint, render_template, jsonify, request
from .pvar.global_f import *
from .model.check_gen import *

main_blueprint = Blueprint("main", __name__)

client_data, server_data = interpret_csv()[0], interpret_csv()[1]
user_data = {"userID": 0, "level": 1, "score": 0}


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


@main_blueprint.route("/api/questions")
def get_questions():
    """
    Send data to client as JSON
    """
    return jsonify(client_data)


@main_blueprint.route("/json/mark", methods=["POST"])
def check_answer():
    """
    Get JSON data from client
    """
    data = request.get_json()
    check = grade_question(data["answer"], data["question"])

    return {"result": check}

@main_blueprint.route("/json/create", methods=["GET"])
def create_question():
    """
    Create a new question
    """
    level = request.get_json()
    question = create_question(level)
    
    return {"result": "success", "data": question}