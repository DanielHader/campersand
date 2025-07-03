from __future__ import annotations
from decimal import Decimal, getcontext
from dataclasses import dataclass
from inspect import signature
import re

getcontext().prec = 50

@dataclass
class Token:
    symbol: str
    type: str

class ASTNode:

    valid_types = ['function', 'number']

    def __init__(self, type, value, children):
        self.type = type
        self.value = value
        self.children = children

        self.__validate()

    def __validate(self):
        # ensure all children are ASTNodes
        for child in self.children:
            if not isinstance(child, ASTNode):
                raise Exception(f'Children of ASTNode must type "ASTNode", found child with type "{type(child).__name__}"')

        # ensure type is a valid type
        if self.type not in ASTNode.valid_types:
            raise Exception(f'Invalid ASTNode type "{self.type}"')

        # convert numbers into Decimal objects
        if self.type == "number":
            try:
                self.value = Decimal(self.value)
            except:
                raise Exception(f'Invalid number value "{self.value}"')

    def evaluate(self, function_map):
        if self.type == 'function':
            if self.value not in function_map:
                raise Exception(f'function "{self.value}" not found in function_map')
            
            func = function_map[self.value]
            if not callable(func):
                raise Exception(f'function "{self.value}" in function_map cannot be called as a function')
            
            num_args = len(signature(func).parameters)
            
            if num_args != len(self.children):
                raise Exception(f'function "{self.value}" in function_map expects {num_args} arguments, received {len(self.children)}')

            return func(*(c.evaluate(function_map) for c in self.children))
        else: # self.type == 'number':
            return self.value

    def __to_string(self, prefix, top_prefix, rest_prefix):
        # draws the abstract syntax sub-tree, rooted 
        #   at this node, using box drawing characters
        
        label = f'{self.type}[{self.value}]'
        s = f'{prefix}{top_prefix}{label}\n'
        prefix += rest_prefix
        for i, child in enumerate(self.children):
            if i < len(self.children) - 1:
                top_prefix = ' ├─ '
                rest_prefix = ' │  '
            else: # last child
                top_prefix = ' └─ '
                rest_prefix =  '    '
            s += child.__to_string(prefix, top_prefix, rest_prefix)
        return s

    def __str__(self):
        return self.__to_string('', '', '')

class Tokenizer:

    def __init__(self):
        self.function_map = {}
        self.function_arity = {}

        self.operator_map = {}
        self.operator_left_assoc = {}
        self.operator_prec = {}

        self.left_parens = ['(', '[']
        self.right_parens = [')', ']']
        self.commas = [',']

        self.used_symbols = set(self.left_parens + self.right_parens)

    def register_function(self, symbol, arity, func):
        num_args = len(signature(func).parameters)
        if arity != num_args:
            raise Exception(f'failed to register function "{symbol}", expecting arity {arity}, found {num_args}')
        if symbol in self.used_symbols:
            raise Exception(f'cannot register function "{symbol}", symbol already registered')
        
        self.function_map[symbol] = func
        self.function_arity[symbol] = arity
        self.used_symbols.add(symbol)

    def register_operator(self, symbol, left_assoc, precedence, func):
        num_args = len(signature(func).parameters)
        if num_args != 2:
            raise Exception(f'operator must use a function of arity 2, found {num_args}')
        if symbol in self.function_map:
            raise Exception(f'cannot register operator "{symbol}", symbol already registered')
        
        self.operator_map[symbol] = func
        self.operator_left_assoc[symbol] = left_assoc
        self.operator_prec[symbol] = precedence
        self.used_symbols.add(symbol)

    def tokenize(self, expr: str):
        tokens = []

        def starts_with_any(expr: str, symbs: list[str]) -> str | None:
            for s in symbs:
                if expr.startswith(s):
                    return s
            return None
        
        number_regex = re.compile(r'^\-?\d*\.?\d+')

        while len(expr) > 0:
            match = number_regex.match(expr)
            if match:
                symb = match.group(0)
                tokens.append(Token(symb, 'number'))
                expr = expr.removeprefix(symb)
            elif symb := starts_with_any(expr, self.left_parens):
                tokens.append(Token(symb, 'left paren'))
                expr = expr.removeprefix(symb)
            elif symb := starts_with_any(expr, self.right_parens):
                tokens.append(Token(symb, 'right paren'))
                expr = expr.removeprefix(symb)
            elif symb := starts_with_any(expr, self.commas):
                tokens.append(Token(symb, 'comma'))
                expr = expr.removeprefix(symb)
            elif symb := starts_with_any(expr, self.operator_map.keys()):
                token = Token(symb, 'operator')
                token.precedence = self.operator_prec[symb]
                token.left_associative = self.operator_left_assoc[symb]
                tokens.append(token)
                expr = expr.removeprefix(symb)          
            elif symb := starts_with_any(expr, self.function_map.keys()):
                token = Token(symb, 'function')
                token.arity = self.function_arity[symb]
                tokens.append(token)
                expr = expr.removeprefix(symb)
            else:
                raise Exception(f'could not parse expression "{expr}"')
            expr = expr.lstrip()
        return tokens

def test():
    root = ASTNode('function', 'add', [
        ASTNode('function', 'multiply', [
            ASTNode('number', '2', []), 
            ASTNode('number', '3', []),
        ]), 
        ASTNode('function', 'sqrt', [ 
            ASTNode('number', '4' , []),
        ]), 
    ])

    function_map = {
        'add': lambda x, y: x + y,
        'multiply': lambda x, y: x * y,
        'sqrt': lambda x: x.sqrt(),
    }

    print(str(root))

    print(root.evaluate(function_map))

if __name__ == "__main__":
    test()