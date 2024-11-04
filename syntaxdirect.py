class IntermediateCodeGenerator:
    def __init__(self):
        self.temp_count = 0  # For generating temporary variables
        self.label_count = 0  # For generating labels
        self.code = []  # To store generated code

    def new_temp(self):
        self.temp_count += 1
        return f"t{self.temp_count}"

    def new_label(self):
        self.label_count += 1
        return f"L{self.label_count}"

    def emit(self, instruction):
        self.code.append(instruction)

    def generate_code(self):
        return "\n".join(self.code)

# Example syntax-directed translation functions for Zara constructs

# Translating an expression
def translate_expression(generator, expr):
    if isinstance(expr, tuple) and len(expr) == 3:
        left, op, right = expr
        left_code = translate_expression(generator, left)
        right_code = translate_expression(generator, right)
        temp_var = generator.new_temp()
        generator.emit(f"{temp_var} = {left_code} {op} {right_code}")
        return temp_var
    else:
        # If expr is just a single operand (e.g., a number or variable)
        return str(expr)

# Translating a for loop
def translate_for_loop(generator, init, condition, increment, body):
    start_label = generator.new_label()
    end_label = generator.new_label()
    
    # Initialize loop variable
    generator.emit(init)
    
    # Label for the start of the loop
    generator.emit(f"{start_label}:")
    
    # Condition check
    condition_var = translate_expression(generator, condition)
    generator.emit(f"if {condition_var} == 0 goto {end_label}")
    
    # Loop body
    for stmt in body:
        translate_statement(generator, stmt)
    
    # Increment
    generator.emit(increment)
    
    # Jump back to the start label
    generator.emit(f"goto {start_label}")
    
    # Label for end of loop
    generator.emit(f"{end_label}:")

# Translating a function call
def translate_function_call(generator, func_name, args):
    arg_vars = [translate_expression(generator, arg) for arg in args]
    for arg_var in arg_vars:
        generator.emit(f"param {arg_var}")
    result_temp = generator.new_temp()
    generator.emit(f"{result_temp} = call {func_name}, {len(arg_vars)}")
    return result_temp

# Translating a general statement (helper function)
def translate_statement(generator, stmt):
    if stmt["type"] == "expression":
        translate_expression(generator, stmt["value"])
    elif stmt["type"] == "for":
        translate_for_loop(generator, stmt["init"], stmt["condition"], stmt["increment"], stmt["body"])
    elif stmt["type"] == "function_call":
        translate_function_call(generator, stmt["func_name"], stmt["args"])

# Example of Zara program to translate
zara_program = [
    {"type": "expression", "value": (3, "+", 4)},
    {"type": "for", 
     "init": "i = 0", 
     "condition": ("i", "<", 10), 
     "increment": "i = i + 1", 
     "body": [
         {"type": "expression", "value": ("i", "*", 2)}
     ]},
    {"type": "function_call", "func_name": "foo", "args": [5, ("i", "*", 2)]}
]

# Generating intermediate code for the Zara program
generator = IntermediateCodeGenerator()
for stmt in zara_program:
    translate_statement(generator, stmt)

# Output the generated intermediate code
print("Generated Intermediate Code:")
print(generator.generate_code())
