import sys
import os

def run_python_file(file_path):
    current_path = os.getcwd()
    print(current_path)
    context = {
        'codePath': [file_path, current_path],
    }

    with open(file_path, 'r') as file:
        code = file.read()
        exec(code, {}, context)

run_python_file("checkuit/"+sys.argv[1])



#checkuit/C/IA/2024/Structures/Exercice1/test_python.py
