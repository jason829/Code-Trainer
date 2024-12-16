import re
import time
import csv

def open_csv(file_path):
    with open(file_path, 'r') as file:
        csv_reader = csv.DictReader(file)
        data = []

        for row in csv_reader:
            for key, value in row.items():
                if value.isdigit():
                    row[key] = int(value)
            data.append(row)
    
    return data

def questions(score, level, question_level):
    for question in (x for x in level if x["level"] == question_level):
        answer = input(f"{question["question"]}\n")
        correct_answer = question["answer"]
        pattern = re.compile(r"" + re.escape(correct_answer))
        
        if re.match(pattern, answer):
            print("CORRECT\n\n")
            score += 1
        else:
            print(f"INCORRECT, Here is a hint \n{question["hint"]}\n\nYour input was: {answer}")
    
    return score

def check_score(passed_levels, score, level):
    if level == 1:
        if score < 10:
            print(f"You got {score}/3 correct. Please Retry the questions")
            time.sleep(1)
            return False
        else:
            print("WELL DONE!! Move on to level 2")
            return passed_levels
    elif level == 2:
        if score < 8:
            print(f"You got {score}/3 correct. Please Retry the questions")
            time.sleep(1)
            return False
        else:
            print("WELL DONE!!")
            return passed_levels

def main():
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
        print(f"Using the following template: \n{template}\n Can you complete level 1...\n")
        score = questions(score, all_questions, 1)
        check = check_score(passed_levels, score, 1)
        
        if not check:
            keep_trying = str(input("Do you want to continue? Y - yes, N - no"))
            if keep_trying.lower() == "y":
                continue
            else:
                break
        else:
            passed_levels += 1
            break

main()