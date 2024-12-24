import logging

#Config log
logging.basicConfig(
    level=logging.DEBUG,  #Minimum level of logs
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),  #Logs to console
        logging.FileHandler("app.log", mode='w')  #Logs to a file
    ]
)

class Node:  #Represents a single node in the expression tree
    def __init__(self, value):
        logging.debug(f"Creating Node with value: {value}")
        self.value = value
        self.left = None
        self.right = None


class Tree:  #Builds and evaluates an expression tree from a mathematical expression
    def __init__(self, expression):
        logging.info(f"Initializing Tree with expression: {expression}")
        self.expression = expression
        self.root = None

    def build_tree(self):  #Parses the expression into tokens and constructs the tree
        logging.info("Building tree...")
        tokens = self._tokenize(self.expression)
        logging.debug(f"Tokens: {tokens}")
        self.root = self._build_tree(tokens)

    def _tokenize(self, expression):  #Splits the expression into tokens (numbers and operators)
        logging.debug("Tokenizing expression...")
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

        logging.debug(f"Tokenized expression: {tokens}")
        return tokens

    def _build_tree(self, tokens):  #Constructs a binary tree using tokens and operator precedence
        logging.debug("Constructing the tree...")
        def priority(operator):
            return {'+': 1, '-': 1, '*': 2, '/': 2}.get(operator, 0)

        def apply_operator(operands, operators):  #Applies the operator at the top of the stack to the top operan
            right = operands.pop()
            left = operands.pop()
            operator = operators.pop()
            node = Node(operator)
            node.left = left
            node.right = right
            operands.append(node)
            logging.debug(f"Applied operator {operator}, created subtree.")

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

        logging.debug("Tree construction completed.")
        return operands[-1]

    def evaluate(self):  #Evaluates the expression tree and returns the result
        logging.info("Evaluating the tree...")
        return self._evaluate_node(self.root)

    def _evaluate_node(self, node):  #Recursively evaluates the subtree rooted at the given node
        if node is None:
            return 0
        if node.left is None and node.right is None:
            logging.debug(f"Evaluating leaf node: {node.value}")
            return float(node.value)

        left_value = self._evaluate_node(node.left)
        right_value = self._evaluate_node(node.right)

        result = 0    #Perform the operation based on the current node's operator
        if node.value == '+':
            result = left_value + right_value
        elif node.value == '-':
            result = left_value - right_value
        elif node.value == '*':
            result = left_value * right_value
        elif node.value == '/':
            if right_value == 0:
                logging.error("Division by zero.")
                raise ValueError("Division by zero.")
            result = left_value / right_value

        logging.debug(f"Evaluated {node.value}: {left_value} {node.value} {right_value} = {result}")
        return result


def main():
    logging.info("Starting program.")
    print("Welcome to the Math Expression Evaluator!")

    while True:
        print("Enter a mathematical expression (or type 'exit' to quit):")
        expression = input("> ")

        if expression.lower() == 'exit':
            logging.info("Exiting program.")
            print("Goodbye!")
            break

        try:
            tree = Tree(expression)
            tree.build_tree()

            result = tree.evaluate()
            print(f"Result: {result}")
        except Exception as e:
            logging.error(f"Error encountered: {e}")
            print(f"Error: {e}. Please try again.")


if __name__ == "__main__":
    main()
