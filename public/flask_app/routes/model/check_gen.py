import ollama

ollama.create(
    model="deepseek-r1:analyser",
    from_="deepseek-r1:latest",
    system="""You are a Python 3.8+ instructor responsible for grading student code submissions. Your task is to assess their implementation based on a structured logical programming approach. 

### **Grading Criteria (Total: 30 Marks)**
You will assess the student's implementation based on the following three categories:

1. **Input Handling (0 - 10 marks)**  
   - Is input handled correctly and efficiently?  
   - Are there any missing or incorrect implementations?
   - For some questions this is section is not necessary and can be skipped.

2. **Processing Logic (0 - 10 marks)**  
   - Is the logic implemented correctly according to the problem statement?  
   - Are there any errors or inefficiencies in the processing logic?
   - For some questions this is section is not necessary and can be skipped.

3. **Output Handling (0 - 10 marks)**  
   - Is the output displayed correctly and meaningfully?  
   - Does it follow the expected format?  
   - Are there any formatting or logical errors in output generation?

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
Only return the following:
```Input Handling: X/10
Processing Logic: Y/10
Output Handling: Z/10
Final Score: (X + Y + Z) / 30

Feedback:
- [Provide concise, constructive feedback on each section]```""",
)

ollama.create(
    model="deepseek-r1:creator",
    from_="deepseek-r1:latest",
    system="""You are a Python 3.8+ instructor responsible for creating practice questions to test students programming skills using the structured logical programming approach below. 

THERE IS A LOGICAL STRUCTURE THAT IS SORTED IN LEVELS, PLEASE FOLLOW THAT STRUCTURE BELOW
JHFDAKSLFJDSAKLJFDAS;LKFJDSAKL;

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


""",
)

# response = ollama.chat(
#     model="deepseek-r1:analyser",
#     messages=[
#         {
#             "role": "user",
#             "content": """ Question: Output 'Hello World!' using 'print()'
#          Student Response:
#          def main():
#             print('Hello World!')
        
#         main()""",
#         },
#     ],
# )
# print(response["message"]["content"])

def grade_question(student_response, question):
    """Generate mark summary and feedback for a student's code submission."""
    response = ollama.chat(
        model="deepseek-r1:analyser",
        messages=[
            {
                "role": "user",
                "content": f"Question: {question}, Student submission: {student_response}",
            },
        ],
    )
    return response["message"]["content"]

def create_question(level):
    """Create a new question in the system."""
    response = ollama.chat(
        model="deepseek-r1:creator",
        messages=[
            {
                "role": "user",
                "content": f"Create a question for level {level}",
            },
        ],
    )
    return response["message"]["content"]
