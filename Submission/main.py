import interpreter_ as interpreter


def eval_stage(stage_expressions):
    for expression in stage_expressions:
        prog_interpreter.execute(expression)


if __name__ == "__main__":
    prog_interpreter = interpreter.Interpreter(debug=False)
    
    try:
        with open('program.txt', 'r') as file:
            code = ["".join(file.readlines())]
            eval_stage(code)
            
    except FileNotFoundError:
        raise SystemExit(f"--- PROGRAM ERROR ---\n"
                         f"FileError: Program file not found\n"
                         f"in File: 'program.txt'\n"
                         f"--- PROGRAM ERROR ---")
    
