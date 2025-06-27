from dataclasses import dataclass
from enum import Enum
import math
import re

class TokenKind(Enum):
    NUMBER = 0
    PAREN_L = 1
    PAREN_R = 2
    CONSTANT = 3
    OPERATOR = 4
    FUNCTION = 5

@dataclass
class Token:
    symbol: str
    kind: TokenKind

def starts_with_any(expr: str, symbs: list[str]) -> str | None:
    for s in symbs:
        if expr.startswith(s):
            return s
    return None

def tokenize(expr: str, **kwargs):
    left_parens  = list(map(lambda x: x.lower(), kwargs.get('left_parens',  ['(', '['])))
    right_parens = list(map(lambda x: x.lower(), kwargs.get('right_parens', [')', ']'])))
    constants    = list(map(lambda x: x.lower(), kwargs.get('constants',    ['pi'])))
    operators    = list(map(lambda x: x.lower(), kwargs.get('operators',    ['+', '-', '*', '/'])))
    functions    = list(map(lambda x: x.lower(), kwargs.get('functions',    ['sin', 'cos'])))

    tokens = []

    while len(expr) > 0:
        if symb := starts_with_any(expr, left_parens):
            tokens.append(Token(symb, TokenKind.PAREN_L))
            expr = expr.removeprefix(symb)
        elif symb := starts_with_any(expr, right_parens):
            tokens.append(Token(symb, TokenKind.PAREN_R))
            expr = expr.removeprefix(symb)
        elif symb := starts_with_any(expr, constants):
            tokens.append(Token(symb, TokenKind.CONSTANT))
            expr = expr.removeprefix(symb)
        elif symb := starts_with_any(expr, operators):
            tokens.append(Token(symb, TokenKind.OPERATOR))
            expr = expr.removeprefix(symb)
        elif symb := starts_with_any(expr, functions):
            tokens.append(Token(symb, TokenKind.PAREN_R))
            expr = expr.removeprefix(symb)
        else:
            number_regex = re.compile(r'\-?\d*\.?\d+')
            match = number_regex.match(expr)
            if match:
                symb = match.group(0)
                tokens.append(Token(symb, TokenKind.NUMBER))
                expr = expr.removeprefix(symb)
            else:
                raise Exception(f'could not parse expression "{expr}"')
        expr = expr.lstrip()
    return tokens

operator_table = {
    '+': lambda x, y: x + y,
    '-': lambda x, y: x - y,
    '*': lambda x, y: x * y,
    '/': lambda x, y: x / y,
}

function_table = {
    'pi': (0, lambda: math.pi),
    'sin': (1, lambda x : math.sin(x)),
}

left_parens = ['(', '[']
right_parens = [')', ']']


def parse(expr: str):
    pass

if __name__ == "__main__":
    
    expr = '1 * (2 + 3) + sin(2 * pi)'
    tokens = tokenize(expr)

    for token in tokens:
        print(token)