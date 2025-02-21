"""
Library of useful functions for server side of the application
"""
import re
import time
import csv
import random

def open_csv(file_path):
    '''
    Open csv based on relative file path
    Will ensure numerical values will be int type
    Returns dictionary of csv
    '''

    with open(file_path, 'r') as file:
        csv_reader = csv.DictReader(file)
        data = []

        # Check convert numerical values to int type
        for row in csv_reader:
            for key, value in row.items():
                if value.isdigit():
                    row[key] = int(value)
            data.append(row)
    
    return data

def check_answer(user_answer_data, server_data):# +++++++++++ FINISH THIS FUNCTION  need chagne how checking works as well+++++++++++++
    """
    Check user answer against the correct answer
    """
    q_id = user_answer_data["id"]
    user_answer = user_answer_data["answer"]
    user_answer.strip()
    clean_output = user_answer.strip().replace("\n", "")
    
    # Regex, check if answer matches pattern in CSV
    correct_answer = server_data[q_id]["answer"]
    pattern = re.compile(r"" + correct_answer)
    if re.match(pattern, clean_output):
        print("Provided answer is correct")
        return True
    else:
        print("Provided answer is incorrect")
        return False

def interpret_csv():
    """
    Formatting the data from the csv into 2 variables
    1 for sending to client and other to remain on server
    """
    all_data = open_csv("public/flask_app/routes/pvar/all_questions.csv")
    client_data = []
    server_data = []
    for data in all_data:
        client_data.append({"id": data["id"], "level": data["level"], "question": data["question"], "hint": data["hint"]})
        server_data.append({"id": data["id"], "level": data["level"], "question": data["question"], "answer": data["answer"]})
        
    return client_data, server_data

def questions(score, level, question_level): # this is for the console version of code, moving to flask
    '''
    Display question, check answer and increment score
    Returns score value after user has answered
    '''

    # Pick 5 random questions from CSV ensuring there's no dupes
    temp_q_arr = [x for x in level if x["level"] == question_level]
    test_q = []
    for _ in range(3):
        random_q = random.choice((temp_q_arr))
        test_q.append(random_q)
        temp_q_arr.remove(random_q)
    
    # Display question and check answer using regex
    for question in test_q:
        print("Enter your answer to the following question. When happy press enter on an empty line")
        print(f"{question["question"]}")
        lines = []
        # Multiple line answers
        print("Press enter on empty line to submit\n")
        while True:
            answer = input().strip()
            if answer == "":
                break
            lines.append(answer)
        answer_line = "".join(lines).strip()

        # Regex, check if answer matches pattern in CSV
        correct_answer = question["answer"]
        pattern = re.compile(r"" + correct_answer)
        if re.match(pattern, answer_line):
            print("************************\nCORRECT\n\n************************")
            score += 1
        else:
            print(f"************************\nINCORRECT, Here is a hint \n{question["hint"]}\n\nYour input was: {answer_line}\n************************")
    
    return score

def check_score(score):
    '''
    Checks score of the current level and determines if user should proceed.
    Returns False if failed and True if passed threshold
    '''

    if score < 3:
        print(f"You got {score}/3 correct. Please Retry the questions")
        time.sleep(1)
        return False
    else:
        print("WELL DONE!! Move on to the next level")
        return True
    
def main():
    '''
    Main
    '''
    with open('pvar/template.txt') as f:
        v = f.read()

    all_questions = open_csv("pvar/all_questions.csv")
    passed_groups = 0
    score = 0
    passed = False
    cur_group = 1
    
    while not passed:
        print(f"Using the following template: \n{v}\nCan you complete the following questions...\n")
        if cur_group > passed_groups:
                passed_groups = cur_group
        score = questions(score, all_questions, cur_group)
        check = check_score(score)
        
        if not check:
            keep_trying = str(input("Do you want to continue? Y - yes"))
            if keep_trying.lower() == "y":
                group_select = int(input(f"Select a group to continue from. You can only continue from group {passed_groups} or less.\n"))
                if group_select <= passed_groups:
                    cur_group = group_select
                else:
                    print("Cannot select this level. Setting as group 1")
                    cur_group = 1
                score = 0
                continue
            else:
                break
        else:
            score = 0
            cur_group += 1
