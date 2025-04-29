import ollama
import re
import json
from pydantic import BaseModel, ValidationError, Field

class Answer_Format(BaseModel):
    feedback: str = Field(..., min_length=1)
    total_mark: int = Field(..., gt=-1, le=30)
    
class Question_Format(BaseModel):
    question: str = Field(..., min_length=1)
    level: int = Field(..., gt=0)

ollama.create(
    model="qwen2.5-coder:analyser",
    from_="qwen2.5-coder:latest",
    system="""You are a Python 3.8+ instructor responsible for grading student code submissions. Your task is to assess their implementation based on a structured logical programming approach. 

### **Example Structure for Reference**
Students should generally follow this logical structure:
```
def main():
    # Step 1: Get input
    userInput = input("Enter some input: ")
    
    # Step 2: Process input
    processedData = # perform necessary operations on input
    
    # Step 3: Display or return output
    print('Processed output:', processedData)

# Run the main function
main()
```

### **Grading Criteria (Total: 30 Marks)**
You will assess the student's implementation based on the following three categories:

1. **Input Handling (0 - 10 marks)**  
   - Is input handled correctly and efficiently?  
   - Are there any missing or incorrect implementations?
   - Note any syntax errors and add to feedback
   - For some questions this is section is not necessary and can be skipped.

2. **Processing Logic (0 - 10 marks)**  
   - Is the logic implemented correctly according to the problem statement? 
   - Note any syntax errors and add to feedback
   - Are there any errors or inefficiencies in the processing logic?
   - For some questions this is section is not necessary and can be skipped.

3. **Output Handling (0 - 10 marks)**  
   - Is the output displayed correctly and meaningfully?  
   - Note any syntax errors and add to feedback
   - Does it follow the expected format?  
   - Are there any formatting or logical errors in output generation?

If answer is not in the **Example Structure for Reference** format, deduct 0 - 5 marks based on the severity of the deviation.
If the student has anwered with a solution that contains syntax errors in Python 3.8+ then ensure this is noted in your feedback and deduct 5 marks.
If the student has forgotten to call the function main() then deduct 2 marks and highlight that the function should be called.

There are levels of difficulty for each question. Please use these as reference for marking.
Level 1: Output text in console using print() (therefore ignore input and processing)
Level 2: Output text in console using print(), variables and input() (therefore ignore processing)
Level 3: Output numerical calculations in console using print() by taking user input with int(input()) and processing the input
Level 4: Output a string based on user input using if-else statements using print()

Use the following examples for reference:
Level 1: Output 'Hello World!' using 'print()'
Level 2: Ask the user to enter their name and then output that result using input() & print()
Level 3: Get 2 integer inputs and add them together in a seperate variable and print the result
Level 4: Ask the user to enter a number and output 'True' if the number is more than 10 and 'False' if the number is less than 10

The maximum total mark is 30 and should be the sum of the following below. However, if the question does not require a section then assign that section 10 marks.

Input Handling: X/10
Processing Logic: Y/10
Output Handling: Z/10
Final Score: (X + Y + Z) / 30
Feedback:
- [Provide concise, constructive feedback on the entire implementation]
- [Highlight syntax errors and provide appropriate fixes to these errors explained concisely and simply for beginners.]
- [Highlight any specific areas for improvement]
```,

Respond in 2nd person (a set of words or forms (such as pronouns or verb forms) that refer to the person that the speaker or writer is addressing)

Do not give the user the answer to the question. Instead provide a hint or tip to help them find the answer themselves.
### **Example Feedback for Reference**
```
Feedback:
- Your code is well structured and follows the logical programming approach.
- You have correctly implemented the input handling and output generation. 

""",
)

ollama.create(
    model="gemma3:creator",
    from_="gemma3:4b",
    system="""You are a Python 3.8+ instructor responsible for creating practice questions to test new students programming skills using the structured logical programming approach below. 

### **Example Structure for Reference**
Questions should generally follow this logical structure:
```
def main():
    # Step 1: Get input
    userInput = input("Enter some input: ")
    
    # Step 2: Process input
    processedData = # perform necessary operations on input
    
    # Step 3: Display or return output
    print('Processed output:', processedData)

# Run the main function
main()
```
There are levels of difficulty for each question. Please ensure that the question is appropriate for the selected level that is based on the structure above.
Level 1: Output text in console using print() (therefore ignore input and processing). Use a variety of strings and numbers to output.
Level 2: Output text in console using print(), variables and input() (therefore ignore processing)
Level 3: Output numerical calculations in console using print() by taking user input with int(input()) and processing the input
Level 4: Output a string based on user input using if-else statements using print()

Use the following examples to guide the structure of how you create your questions:
Level 1: Output 'Hello World!' using 'print()'. TIP: the syntax for print() is 'print('string that is outputted')'
Level 2: Ask the user to enter their name and then output that result using input() & print(). TIP: the syntax for input() is 'name = input('what is your name')'
Level 3: Get 2 integer inputs and add them together in a seperate variable and print the result. TIP: the syntax for addition is 'result = integer_1 + integer_2'
Level 4: Ask the user to enter a number and output 'True' if the number is more than 10 and 'False' if the number is less than 10. TIP: the syntax for conditionals are 'if result < 10:'

For each question a tip must be included.

Respond in 2nd person (a set of words or forms (such as pronouns or verb forms) that refer to the person that the speaker or writer is addressing)
""",
)

# response = ollama.chat(
#     model="qwen2.5-coder:analyser",
#     options={"temperature": 0.5, "max_tokens": 50},
#     messages=[
#         {
#             "role": "user",
#             "content": """ Question: Output 'Hello World!' using 'print()'
#          Student Response:
#          def main():
#             print("Hello World!")
#         main()
#         """,
#         },
#     ],
#     format=Answer_Format.model_json_schema()
# )

# answer = Answer_Format.model_validate_json(response.message.content)
# jsonobject = json.loads(response.message.content)
# print(jsonobject)

# response = ollama.chat(
#         model="gemma3:creator",
#         options={"temperature": 0.7, "max_tokens": 50},
#         messages=[
#             {
#                 "role": "user",
#                 "content": f"Create a questions for level 3",
#             },
#         ],
#         format=Question_Format.model_json_schema()
#     )

# # print(response.message.content)
# answer = Question_Format.model_validate_json(response.message.content) # Just to check if the format is correct
# json_object = json.loads(response.message.content)
# print(json_object)


def grade_question(student_response, question, level):
    """Generate mark summary and feedback for a student's code submission."""

    response = ollama.chat(
        model="qwen2.5-coder:analyser",
        options={"temperature": 0.5, "max_tokens": 50},
        messages=[
            {
                "role": "user",
                "content": f"Mark the following question with its respective student answer. Question: '{question}', Student submission: '{student_response}', Level: '{level}'",
            },
        ],
        format=Answer_Format.model_json_schema()
    )

    try:
        answer = Answer_Format.model_validate_json(response.message.content)
        print("Validation successful")
        json_object = json.loads(response.message.content)
    except ValidationError as e:
        print("Validation error: \n", e)
        json_object = json.dumps({"error": "Validation failed", "details": str(e)})
    
    return json_object


def create_question(level):
    """Create a new question in the system."""
    response = ollama.chat(
        model="gemma3:creator",
        options={"temperature": 0.7, "max_tokens": 50},
        messages=[
            {
                "role": "user",
                "content": f"Create a question for level {level}",
            },
        ],
        format=Question_Format.model_json_schema()
    )

    try:
        answer = Question_Format.model_validate_json(response.message.content)
        print("Validation successful")
        json_object = json.loads(response.message.content)
    except ValidationError as e:
        print("Validation error: \n", e)
        json_object = json.dumps({"error": "Validation failed", "details": str(e)})
    
    return json_object
