def run_program(program):
    variables = {}
    lines = program.strip().split('\n')
    output = []
    message_buffer = []
    processing_block = False
    condition_met = False
    command_active = False

    print("Starting to run the program...")
    
    for line in lines:
        print(f"Processing line: {line.strip()}")
        cleaned_line = line.strip()

        if cleaned_line == '˙':
            if condition_met or command_active:
                message = ' '.join(message_buffer)
                output.append(message)
                print(f"Outputting: {message}")
            processing_block = False
            condition_met = False
            command_active = False
            message_buffer = []
            continue

        if processing_block:
            if cleaned_line.startswith('#') or cleaned_line.startswith('@say'):
                if message_buffer and (condition_met or command_active):
                    message = ' '.join(message_buffer)
                    output.append(message)
                    print(f"Outputting: {message}")
                message_buffer = []
                condition_met = False
                command_active = False

            if '`' in cleaned_line:
                message_buffer.append(cleaned_line.strip('`').strip())
                continue

        tokens = cleaned_line.split()
        if 'E' in tokens:
            var_index = tokens.index('E')
            var_name = tokens[var_index - 1]
            var_value = int(tokens[var_index + 1])
            variables[var_name] = var_value
            print(f"Assigned {var_value} to {var_name}")

        elif cleaned_line.startswith('@say'):
            processing_block = True
            command_active = True
            continue

        elif '#' in tokens:
            processing_block = True
            var_name = tokens[1]
            operator = tokens[2]
            comp_value = int(tokens[3])
            actual_value = variables.get(var_name, 0)
            condition_met = eval_condition(operator, actual_value, comp_value)
            print(f"Condition check for {var_name}: {actual_value} {operator} {comp_value} = {condition_met}")

    if output:
        result = "\n".join(output)
    else:
        result = "No conditions met or output generated."

    print("Finished running the program.")
    return result

def eval_condition(operator, actual_value, comp_value):
    return ((operator == 'S' and actual_value < comp_value) or
            (operator == 'SE' and actual_value <= comp_value) or
            (operator == '!S' and actual_value > comp_value) or
            (operator == '!SE' and actual_value >= comp_value))

def run_program_from_file(file_name):
    with open(file_name, 'r') as file:
        program = file.read()
        return run_program(program)

# Example DSL program file name
dsl_program_file = "dsl_program.lhs"

# Run the interpreter using the DSL program file
result = run_program_from_file(dsl_program_file)
print("Result of DSL program execution:")
print(result)