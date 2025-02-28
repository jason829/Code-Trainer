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
    DB_USER = os.getenv('fyp_db_user')
    DB_PASS = os.getenv('fyp_db_pass')

    conn = psycopg2.connect(database="fyp_db",  
                            user=DB_USER, 
                            password=DB_PASS,  
                            host="0.0.0.0", port="5432") 

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

@main_blueprint.route("/json", methods=["POST"])
def get_json():
    """
    Get JSON data from client
    """
    data = request.get_json()
    question = server_data[data["id"]]["question"]
    check = grade_question(data["answer"], question)
    
    return {"result": check}
