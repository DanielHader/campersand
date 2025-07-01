from __future__ import annotations
from decimal import Decimal, getcontext
from inspect import signature

getcontext().prec = 50

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
            
            sig = signature(func)
            num_args = len(sig.parameters)
            
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