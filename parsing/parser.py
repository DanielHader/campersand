import math
from syntax_tree import Tokenizer, Token

operators = ['+', '-', '*', '/', '^']
functions = ['pi', 'sqrt', 'sin', 'cos']
left_parens = ['(', '[']
right_parens = [')', ']']

function_arity = {
    'pi': 0,
    'sqrt': 1,
    'sin': 2,
    'cos': 2,
}

operator_left_assoc = {
    '+': True,
    '-': True,
    '*': True,
    '/': True,
    '^': False,
}

operator_precidence = {
    '+': 0,
    '-': 0,
    '*': 1,
    '/': 1,
    '^': 2,
}

def parse(tokens: list[Token]):    
    stack = []
    output = []

    for token in tokens:
        if token.type == 'number':
            output.append(token)
        
        elif token.type == 'function':
            stack.append(token)
        
        elif token.type == 'comma':
            
            while stack[-1].type != 'left paren':
                output.append(stack.pop())

        elif token.type == 'left paren':
            stack.append(token)

        elif token.type == 'right paren':
            while stack[-1].type != 'left paren':
                output.append(stack.pop())
            assert stack[-1].type == 'left paren'
            stack.pop()

        else: # an operator
            while len(stack) > 0 and stack[-1].type != 'left paren':
                if stack[-1].precedence > token.precedence or (stack[-1].precedence == token.precedence and token.left_associative):
                    output.append(stack.pop())
                else:
                    break
            stack.append(token)

    while len(stack) > 0:
        top = stack.pop()
        assert top.type != 'left paren'
        output.append(top)

    return output

if __name__ == "__main__":
    
    tokenizer = Tokenizer()
    tokenizer.register_operator('+',  True, 0, lambda x, y: x + y)
    tokenizer.register_operator('-',  True, 0, lambda x, y: x - y)
    tokenizer.register_operator('*',  True, 1, lambda x, y: x * y)
    tokenizer.register_operator('/',  True, 1, lambda x, y: x / y)
    tokenizer.register_operator('^', False, 2, lambda x, y:  x**y)

    expr = '1 * (2 + 3) + (2 * -5.2)'
    tokens = tokenizer.tokenize(expr)

    for token in tokens:
        print(token)

    print()

    for token in parse(tokens):
        print(token)