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

def questions(score, level, question_level):
    '''
    Display question, check answer and increment score
    Returns score value after user has answered
    '''

    # Pick 5 random questions from CSV ensuring there's no dupes
    temp_q_arr = [x for x in level if x["level"] == question_level]
    test_q = []
    for _ in range(5):
        random_q = random.choice((temp_q_arr))
        test_q.append(random_q)
        temp_q_arr.remove(random_q)
    
    # Display question and check answer using regex
    for question in test_q:
        print("Enter your answer to the following question. When happy press enter on an empty line")
        print(f"{question["question"]}")
        lines = []
        # Multiple line answers
        while True:
            answer = input("Press enter on empty line to submit").strip()
            if answer == "":
                break
            lines.append(answer)
        answer_line = "".join(lines).strip()

        # Regex, check if answer matches pattern in CSV
        correct_answer = question["answer"]
        pattern = re.compile(r"" + correct_answer)
        if re.match(pattern, answer_line):
            print("CORRECT\n\n")
            score += 1
        else:
            print(f"INCORRECT, Here is a hint \n{question["hint"]}\n\nYour input was: {answer_line}")
    
    return score

def check_score(score, level):
    '''
    Checks score of the current level and determines if user should proceed.
    Returns False if failed and True if passed threshold
    '''

    if level == 1:
        if score < 4:
            print(f"You got {score}/3 correct. Please Retry the questions")
            time.sleep(1)
            return False
        else:
            print("WELL DONE!! Move on to level 2")
            return True
    elif level == 2:
        if score < 4:
            print(f"You got {score}/3 correct. Please Retry the questions")
            time.sleep(1)
            return False
        else:
            print("WELL DONE!!")
            return True

def main():
    '''
    Main
    '''

    template = """
        def main():
            # Step 1: Get input
            # e.g userInput = input("Enter some input: ")
            
            # Step 2: Process input
            # e.g processedData = # do something with the parameters
            
            # Step 3: Display or use the processed output
            # e.g print('Processed output:', processedData)

            # Call the main function to run the main

        main()
    """
    passed_levels = 0
    score = 0
    passed = False

    all_questions = open_csv("pvar/all_questions.csv")
    
    while not passed:
        print(f"Using the following template: \n{template}\nCan you complete level 1...\n")
        score = questions(score, all_questions, 1)
        check = check_score(passed_levels, score, 1)
        
        if not check:
            keep_trying = str(input("Do you want to continue? Y - yes, N - no"))
            if keep_trying.lower() == "y":
                score = 0
                continue
            else:
                break
        else:
            score = 0
            passed_levels += 1
            score = questions(score, all_questions, 2)
            check = check_score(passed_levels, score, 1)
            if not check:
                keep_trying = str(input("Do you want to continue? Y - yes, N - no"))
                if keep_trying.lower() == "y":
                    score = 0
                    continue
                else:
                    break
            else:
                print("well done")
            
main()