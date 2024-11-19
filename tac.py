class TACGenerator:
    def __init__(self):
        self.temp_count = 0
        self.code = []

    def new_temp(self):
        """Generate a new temporary variable."""
        self.temp_count += 1
        return f"t{self.temp_count}"

    def emit(self, op, arg1=None, arg2=None, result=None):
        """Emit a TAC instruction."""
        if arg2:
            self.code.append(f"{result} = {arg1} {op} {arg2}")
        elif arg1:
            self.code.append(f"{result} = {op} {arg1}")
        else:
            self.code.append(f"{result} = {op}")

    def generate_expression(self, expression):
        """Generate TAC for an arithmetic expression."""
        if isinstance(expression, tuple):  # Binary operation: (op, left, right)
            op, left, right = expression
            left_temp = self.generate_expression(left)
            right_temp = self.generate_expression(right)
            result = self.new_temp()
            self.emit(op, left_temp, right_temp, result)
            return result
        else:  # It's a variable or constant
            return expression

    def generate_if(self, condition, true_block, false_block=None):
        """Generate TAC for an if statement."""
        cond_temp = self.generate_expression(condition)
        true_label = self.new_label()
        false_label = self.new_label() if false_block else None
        end_label = self.new_label()

        self.code.append(f"if {cond_temp} goto {true_label}")
        if false_block:
            self.code.append(f"goto {false_label}")
            self.code.append(f"label {false_label}")
            self.generate_block(false_block)
        self.code.append(f"label {true_label}")
        self.generate_block(true_block)
        self.code.append(f"label {end_label}")

    def generate_block(self, block):
        """Generate TAC for a block of code."""
        for statement in block:
            self.generate_statement(statement)

    def generate_statement(self, statement):
        """Generate TAC for a single statement."""
        if statement[0] == "assign":  # Assignment: ("assign", var, expr)
            _, var, expr = statement
            expr_temp = self.generate_expression(expr)
            self.emit("=", expr_temp, result=var)
        elif statement[0] == "if":  # If: ("if", condition, true_block, false_block)
            _, condition, true_block, false_block = statement
            self.generate_if(condition, true_block, false_block)
        elif statement[0] == "call":  # Function call: ("call", func_name, args)
            _, func_name, args = statement
            arg_temps = [self.generate_expression(arg) for arg in args]
            self.code.append(f"call {func_name}({', '.join(arg_temps)})")
        # Add more cases as needed (e.g., loops, return statements).

    def new_label(self):
        """Generate a new label."""
        self.temp_count += 1
        return f"L{self.temp_count}"

    def get_code(self):
        """Return the generated TAC code."""
        return "\n".join(self.code)


# Example Zara program in abstract syntax
zara_program = [
    ("assign", "x", ("/", 10, 2)),  # x = 10 / 2
    ("assign", "y", ("+", "x", 3)),  # y = x + 3
    ("if", (">", "y", 5),  # if y > 5
        [("assign", "z", 1)],  # true block: z = 1
        [("assign", "z", 0)]),  # false block: z = 0
    ("call", "print", ["z"])  # call print(z)
]

# Generate TAC
tac_generator = TACGenerator()
tac_generator.generate_block(zara_program)

# Print the generated TAC
print("Generated Three-Address Code (TAC):")
print(tac_generator.get_code())
