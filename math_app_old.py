class Node:
    # Represents a single node in the expression tree
    def __init__(self, value):
        self.value = value  # Value of the node (number or operator)
        self.left = None  # Left child node
        self.right = None  # Right child node


class Tree:
    # Builds and evaluates an expression tree from a mathematical expression
    def __init__(self, expression):
        self.expression = expression  # Expression to be parsed
        self.root = None  # Root of the tree

    def build_tree(self):
        # Parses the expression into tokens and builds the tree
        tokens = self._tokenize(self.expression)
        self.root = self._build_tree(tokens)

    def _tokenize(self, expression):
        # Converts a mathematical expression into a list of tokens
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

    def _build_tree(self, tokens):
        # Constructs the tree using tokens and operator precedence
        def priority(operator):
            if operator in ('+', '-'):
                return 1
            if operator in ('*', '/'):
                return 2
            return 0

        def apply_operator(operands, operators):
            right = operands.pop()
            left = operands.pop()
            operator = operators.pop()
            
            node = Node(operator)
            node.left = left
            node.right = right
            
            operands.append(node)

        operands = []
        operators = []

        i = 0
        while i < len(tokens):
            token = tokens[i]

            if token.isdigit() or '.' in token:
                operands.append(Node(token))

            elif token == '(':
                operators.append(token)

            elif token == ')':
                while operators and operators[-1] != '(':
                    apply_operator(operands, operators)
                operators.pop()

            else:
                while (operators and operators[-1] != '(' and
                       priority(operators[-1]) >= priority(token)):
                    apply_operator(operands, operators)
                operators.append(token)
            i += 1

        while operators:
            apply_operator(operands, operators)

        return operands[-1]

    def evaluate(self):
        # Evaluates the expression tree and returns the result
        return self._evaluate_node(self.root)

    def _evaluate_node(self, node):
        # Recursively evaluates a subtree rooted at the given node
        if node is None:
            return 0
        if node.left is None and node.right is None:
            return float(node.value)

        left_value = self._evaluate_node(node.left)
        right_value = self._evaluate_node(node.right)

        if node.value == '+':
            return left_value + right_value
        elif node.value == '-':
            return left_value - right_value
        elif node.value == '*':
            return left_value * right_value
        elif node.value == '/':
            if right_value == 0:
                raise ValueError("Division by zero.")
            return left_value / right_value


def main():
    # Entry point for the program
    print("Enter a mathematical expression:")
    expression = input()

    try:
        tree = Tree(expression)
        tree.build_tree()

        result = tree.evaluate()
        print(f"Result: {result}")
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
