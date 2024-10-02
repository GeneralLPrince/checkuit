import subprocess
import sys
import textwrap
import os

if not os.path.exists(codePath[1]+"/Exercice2.c"):
    print(f"\033[31m:( Exercice1.c n'existe pas sous {codePath[1]}\033[0m")
    exit(1)

compile_command = ["gcc", codePath[1]+"/Exercice2.c", "-o", "Exercice2"]
compilation = subprocess.run(compile_command, capture_output=True, text=True)

if compilation.returncode != 0:
    print("\033[31m:( Exercice2.c ne se compile pas correctement\033[0m")
    print(f"\033[33m:| Exercice2.c affiche Bonjour\033[0m")
    print(compilation.stderr)

    exit(1)

print("\033[32m:) Exercice2.c se compile correctement\033[0m")

numbers = ["123","321","000","001"]

for num in numbers:
    process = subprocess.Popen(
    ["./Exercice2"],
    stdin=subprocess.PIPE,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    text=True
    )
    
    try:
        output, errors = process.communicate(input=num,timeout=5)
    except subprocess.TimeoutExpired:
        process.kill()
        print(f"Test failed: Program timed out.")
        sys.exit(1)

    if errors:
        print(f"Test failed with errors:")
        print(errors)
        sys.exit(1)

    answer = output.split("Veuillez entrer un nombre constitué de 3 chiffres:")

    if len(answer) == 2:
        answer = answer[1].strip()
        if answer == num[::-1]:
            print(f"\033[32m:) Exercice2.c affiche {num[::-1]} avoir saisi {num}\033[0m")
        else:
            print("\033[31m:( Exercice2.c affiche {num[::-1]} avoir saisi {num}\033[0m")
            print(f"\033[33mRetour: \n{answer}\033[0m")
    else:
        print("\033[31m:( Exercice2.c affiche {num[::-1]} avoir saisi {num}\033[0m")
        print(f"\033[33mRetour: \n{output}\033[0m")
