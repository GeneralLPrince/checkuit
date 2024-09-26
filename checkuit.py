import sys
import os

current_path = os.path.dirname(os.path.abspath(__file__))

def run_python_file(file_path):
    context = {
        'codePath': [file_path, os.getcwd()],
    }

    with open(file_path, 'r') as file:
        code = file.read()
        exec(code, {}, context)

run_python_file(f"{current_path}/"+sys.argv[1])



#checkuit/C/IA/2024/Structures/Exercice1/test_python.py
