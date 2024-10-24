grammar = {
    'Program': ['StatementList'],
    'StatementList': ['Statement StatementList', 'ε'],
    'Statement': ['Expression ;', 'IfStatement', 'LoopStatement'],
    'Expression': ['Term ExpressionPrime'],
    'ExpressionPrime': ['+ Term ExpressionPrime', '- Term ExpressionPrime', 'ε'],
    'Term': ['Factor TermPrime'],
    'TermPrime': ['* Factor TermPrime', '/ Factor TermPrime', 'ε'],
    'Factor': ['( Expression )', 'NUM', 'ID'],
    'IfStatement': ['if ( Expression ) { StatementList } ElsePart'],
    'ElsePart': ['else { StatementList }', 'ε'],
    'LoopStatement': ['for ( Expression ; Expression ; Expression ) { StatementList }', 
                      'do { StatementList } while ( Expression )']
}

precedence = {
    '+': 1,
    '-': 1,
    '*': 2,
    '/': 2
}

associativity = {
    '+': 'L',
    '-': 'L',
    '*': 'L',
    '/': 'L'
}

class Parser:
    def __init__(self, grammar, precedence, associativity):
        self.grammar = grammar
        self.precedence = precedence
        self.associativity = associativity
        self.stack = []
        self.input_tokens = []

    def parse(self, tokens):
        self.input_tokens = tokens + ['$']  # Add end-of-input symbol
        self.stack = [0]  # Initial state
        while True:
            state = self.stack[-1]
            lookahead = self.input_tokens[0]

            action = self.get_action(state, lookahead)
            if action.startswith("shift"):
                self.shift(action)
            elif action.startswith("reduce"):
                self.reduce(action)
            elif action == "accept":
                print("Parsing successful!")
                return True
            else:
                print(f"Error: Unexpected token {lookahead}")
                return False

    def get_action(self, state, lookahead):
        # Simplified table lookup (for demonstration)
        if lookahead in ['+', '-', '*', '/']:
            return "shift"
        elif lookahead == ';' or lookahead == '$':
            return "reduce"
        else:
            return "error"

    def shift(self, action):
        # Push state to the stack and consume input token
        print(f"Shifting: {self.input_tokens[0]}")
        self.stack.append(self.input_tokens.pop(0))

    def reduce(self, action):
        # Pop from stack and apply reduction rule
        print(f"Reducing: {self.stack[-1]}")
        self.stack.pop()

def resolve_shift_reduce_conflict(self, operator):
    stack_operator = self.stack[-1]
    if (self.precedence[operator] > self.precedence[stack_operator]):
        return "shift"
    elif (self.precedence[operator] < self.precedence[stack_operator]):
        return "reduce"
    else:
        return self.associativity[operator]

# Example usage
tokens = ['NUM', '+', 'NUM', '*', 'NUM', ';']
parser = Parser(grammar, precedence, associativity)
parser.parse(tokens)
