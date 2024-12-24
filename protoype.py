class Node:  #Represents a single node in the expression tree
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None

class Tree:    # Builds and evaluates an expression tree
    def __init__(self, expression):
        self.expression = expression
        self.root = None

    def build_tree(self): #Converts the expression into tokens and builds the tree
        tokens = self.tokenize(self.expression)
        self.root = self.construct_tree(tokens)

    def tokenize(self, expression): #Splits the expression into numbers and operators
        tokens = []
        number = ''
        for char in expression:
            if char.isdigit() or char == '.':
                number += char
            else:
                if number:
                    tokens.append(number)
                    number = ''
                if char in '+-*/()':
                    tokens.append(char)
        if number:
            tokens.append(number)
        return tokens

    def construct_tree(self, tokens):   #Constructs the expression tree from tokens
        def priority(operator):
            return {'+': 1, '-': 1, '*': 2, '/': 2}.get(operator, 0)

        def apply_operator(operands, operators):
            right = operands.pop()
            left = operands.pop()
            operator = operators.pop()
            node = Node(operator)
            node.left = left
            node.right = right
            operands.append(node)

        operands, operators = [], []
        for token in tokens:
            if token.isdigit() or '.' in token:
                operands.append(Node(token))
            elif token == '(':
                operators.append(token)
            elif token == ')':
                while operators[-1] != '(':
                    apply_operator(operands, operators)
                operators.pop()
            else:
                while operators and priority(operators[-1]) >= priority(token):
                    apply_operator(operands, operators)
                operators.append(token)

        while operators:
            apply_operator(operands, operators)

        return operands[0]

    def evaluate(self, node):
        # Recursively evaluates the expression tree
        if node.left is None and node.right is None:
            return float(node.value)
        left_value = self.evaluate(node.left)
        right_value = self.evaluate(node.right)
        if node.value == '+':
            return left_value + right_value
        elif node.value == '-':
            return left_value - right_value
        elif node.value == '*':
            return left_value * right_value
        elif node.value == '/':
            return left_value / right_value

expression = "3 + 5 * (2 - 8)"
tree = Tree(expression)
tree.build_tree()
result = tree.evaluate(tree.root)
print(f"Result of '{expression}' is: {result}")
