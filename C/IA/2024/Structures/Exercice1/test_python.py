import subprocess
import math
import sys
import textwrap

input_data = ["3", "Ali", "20", "Rayan", "16", "Saad", "0"]
input_str = "\n".join(input_data)

compile_command = ["gcc", codePath[1]+"/student_program.c", "-o", "student_program"]
compilation = subprocess.run(compile_command, capture_output=True, text=True)

if compilation.returncode != 0:
    print("\033[31m:( student_program.c ne se compile pas correctement\033[0m")
    print(compilation.stderr)

    for number in range(4):
        print(f"\033[33m:| Factorielle de {number} est {math.factorial(number)}\033[0m")

    exit(1)

print("\033[32m:) student_program.c se compile correctement\033[0m")

process = subprocess.Popen(
    ["./student_program"],
    stdin=subprocess.PIPE,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    text=True
)

try:
    output, errors = process.communicate(input=input_str, timeout=5)
except subprocess.TimeoutExpired:
    process.kill()
    print(f"Test failed: Program timed out.")
    sys.exit(1)

if errors:
    print(f"Test failed with errors:")
    print(errors)
    sys.exit(1)

if len(output.split("------------")) < 2:
    padded_lines = "\n".join(line.rjust(10) for line in output.splitlines())
    print("\033[31m:( student_program.c renvoie correctement la note d'Ali, Rayan et Saad selon l'ordre d'insertion !\033[0m")
    print(f"\033[33mRetour: \n{padded_lines}\033[0m")
    sys.exit(1)
else:
    answer = output.split("------------")[1].strip()
    padded_lines = textwrap.indent(answer, '   ')

    if answer == "Nom: Ali\nNote: 20\n\nNom: Rayan\nNote: 16\n\nNom: Saad\nNote: 0":
        print("\033[32m:) student_program.c renvoie correctement la note d'Ali, Rayan et Saad selon l'ordre d'insertion !\033[0m")
    else:
        print("\033[31m:( student_program.c renvoie correctement la note d'Ali, Rayan et Saad selon l'ordre d'insertion !\033[0m")
        print(f"\033[33mRetour: \n{padded_lines}\033[0m")

