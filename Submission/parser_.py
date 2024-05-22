import token_ as token

# KeywordNode, BinaryNode, UnaryNode, VariableNode and ValueNode will be referred to as a 'Node' instance.


class KeywordNode:
    def __init__(self, kw_token, node):
        """
        Create a new KeywordNode for storing ReservedKeyword and Node
        :param kw_token: Token
        :param node: Node
        """
        self.kw_token = kw_token
        self.node = node


class UnaryNode:
    def __init__(self, op_token, node):
        """
        Create a new UnaryNode for storing Operator and Node
        :param op_token: String
        :param node: Node
        """
        self.op_token = op_token
        self.node = node


class BinaryNode:
    def __init__(self, left, op_token, right):
        """
        Create a new BinaryNode for storing LeftNode, Operator and RightNode
        :param left: Node
        :param op_token: String
        :param right: Node
        """
        self.left = left
        self.op_token = op_token
        self.right = right


class VariableNode:
    def __init__(self, var_token, val_node):
        """
        Create a new VariableNode for storing a variable and its value
        :param var_token: Token
        :param val_node: Node
        """
        self.var_token = var_token
        self.val_node = val_node


class ValueNode:
    def __init__(self, tk):
        """
        Create a new ValueNode for storing a primary Token
        :param tk: Token
        """
        self.token = tk


class Parser:
    def __init__(self):
        """
        Create a new Parser
        """
        self.expr = None
        self.tokens = []
        self.idx = -1
        self.current_token = None
        self.prev_expr = []
        self.statements = []
        self.ast = None

    def get_next_token(self):
        """
        Get the next Token
        :return: Token
        """
        # Increment Token index
        self.idx += 1
        # Index is within length of Tokens
        if self.idx < len(self.tokens):
            return self.tokens[self.idx]
        # Reached the end of Tokens
        else:
            return None

    def is_eof(self):
        """
        Determine if Parser has reached the End of File (EOF) Token
        :return: Boolean
        """
        return self.current_token.type == token.TokenType.EOF

    def parse_statement(self):
        """
        Parse a statement (single line of code)
        :return: Node
        """
        # Reserved Keywords
        if self.current_token.type == token.TokenType.ReservedKeyword:
            new_expr = self.parse_kw_expr()

        # Variable assignment
        elif self.current_token.type == token.TokenType.Variable:
            new_expr = self.parse_var_expr()

        # Everything else
        else:
            new_expr = self.parse_expr()

        # If the Node exists and not EOL (None)
        if new_expr:
            # Append to previous expressions for precedence management
            self.prev_expr.append(new_expr)

        return new_expr

    def parse_kw_expr(self):
        """
        Parse a keyword expression
        :return: KeywordNode
        """
        # Get the KeywordToken
        kw_token = self.current_token
        self.current_token = self.get_next_token()
        # Parse expression for node
        node = self.parse_expr()
        return KeywordNode(kw_token, node)

    def parse_var_expr(self):
        """
        Parse a variable assignment expression
        :return: VariableNode
        """
        # Get the VariableToken
        var_token = self.current_token
        self.current_token = self.get_next_token()

        # If assigning value to a variable
        if self.current_token.type == token.TokenType.Equals:
            # Discard equals sign
            self.current_token = self.get_next_token()
            # Parse expression for value node
            val_node = self.parse_expr()
            return VariableNode(var_token, val_node)

        # Statements starting with variables must only be for assignment
        raise SystemExit(f"--- PARSER ERROR ---\n"
                         f"SyntaxError: Expected variable assignment\n"
                         f"in Variable {var_token.value}\n"
                         f"--- PARSER ERROR ---")

    def parse_expr(self):
        """
        Parse an expression in order of precedence
        :return: Node
        """
        return self.parse_logical_expr()

    def parse_logical_expr(self):
        """
        Parse a logical expression
        :return: Node
        """
        # Parse comparison expression for left node
        left = self.parse_comparison_expr()

        # Token.value is logic keyword
        if self.current_token.value in ["and", "or"]:
            # Get operator Token and increment to next Token
            op_token = self.current_token
            self.current_token = self.get_next_token()
            # Parse logical expression for right node
            right = self.parse_logical_expr()
            # Assign left node to BinaryNode
            left = BinaryNode(left, op_token, right)

        return left

    def parse_comparison_expr(self):
        """
        Parse a comparison expression
        :return: Node
        """
        # Parse primary comparison expression for left node
        left = self.parse_primary_comparison_expr()

        # Token.value is comparison keyword
        if self.current_token.value in ['==', '!=']:
            # Get operator Token and increment to next Token
            op_token = self.current_token
            self.current_token = self.get_next_token()
            # Parse comparison expression for right node
            right = self.parse_comparison_expr()
            # Assign left node to BinaryNode
            left = BinaryNode(left, op_token, right)

        return left

    def parse_primary_comparison_expr(self):
        """
        Parse a primary comparison expression
        :return: Node
        """
        # Parse addition/subtraction expression for left node
        left = self.parse_add_expr()

        # Token.value is primary comparison keyword
        if self.current_token.value in ['>', '<', '>=', '<=']:
            # Get operator Token and increment to next Token
            op_token = self.current_token
            self.current_token = self.get_next_token()
            # Parse primary comparison expression for right node
            right = self.parse_primary_comparison_expr()
            # Assign left node to BinaryNode
            left = BinaryNode(left, op_token, right)

        return left

    def parse_add_expr(self):
        """
        Parse an addition/subtraction expression
        :return: Node
        """
        # Parse multiplication/division expression for left node
        left = self.parse_mult_expr()

        # Token.value is addition/subtraction keyword
        if self.current_token.value in ['+', '-']:
            # Get operator Token and increment to next Token
            op_token = self.current_token
            self.current_token = self.get_next_token()
            # Parse multiplication/division expression for right node
            right = self.parse_add_expr()
            # Assign left node to BinaryNode
            left = BinaryNode(left, op_token, right)

        return left

    def parse_mult_expr(self):
        """
        Parse a multiplication/division expression
        :return: Node
        """
        # Parse unary expression for left node
        left = self.parse_unary_expr()

        # Token.value is multiplication/division keyword
        if self.current_token.value in ['*', '/', '%', '**']:
            # Get operator Token and increment to next Token
            op_token = self.current_token
            self.current_token = self.get_next_token()
            # Parse unary expression for right node
            right = self.parse_mult_expr()
            # Assign left node to BinaryNode
            left = BinaryNode(left, op_token, right)

        return left

    def parse_unary_expr(self):
        """
        Parse a unary expression
        :return: Node
        """
        # Token.value is unary keyword
        if self.current_token.value in ['!', 'not']:
            # Get operator Token and increment to next Token
            op_token = self.current_token
            self.current_token = self.get_next_token()
            # Parse unary expression for node
            node = self.parse_unary_expr()
            return UnaryNode(op_token, node)

        # Else, parse primary expression
        return self.parse_primary_expr()

    def parse_primary_expr(self):
        """
        Parse a primary expression
        :return: Node
        """
        # Token.type is Integer, Float, Boolean, String, Variable or NoneType
        if self.current_token.type in [token.TokenType.Integer, token.TokenType.Float, token.TokenType.Boolean,
                                       token.TokenType.String, token.TokenType.Variable, token.TokenType.NoneType]:
            # Create a new ValueNode
            node = ValueNode(self.current_token)

            # String Tokens require prefix and suffix '" "' to be removed before interpreter
            if self.current_token.type == token.TokenType.String:
                node.token.value = node.token.value[1:-1]

            # Increment to next Token
            self.current_token = self.get_next_token()
            return node

        # Token.type is BinaryOperation
        elif self.current_token.type == token.TokenType.BinaryOperation:
            # Invert BinaryOperator
            if self.current_token.value == '-':
                # Get operator Token and increment to next Token
                op_token = self.current_token
                self.current_token = self.get_next_token()

                # If inverting a Variable
                if self.current_token.type == token.TokenType.Variable:
                    # Parse expression for node
                    node = self.parse_expr()
                    return UnaryNode(op_token, node)

        # Token.type is LeftParen
        elif self.current_token.type == token.TokenType.LeftParen:
            # Increment to next Token and parse expression
            self.current_token = self.get_next_token()
            value = self.parse_expr()

            # No matching RightParen Token found
            if self.current_token.type != token.TokenType.RightParen:
                raise SystemExit(f"--- PARSER ERROR ---\n"
                                 f"SyntaxError: Left parenthesis '(' missing matching right parenthesis ')'\n"
                                 f"in Expression: '{self.expr}'\n"
                                 f"--- PARSER ERROR ---")

            # Increment to next Token, skipping RightParen Token
            self.current_token = self.get_next_token()
            return value

        # Token.type is EOL (e.g. '\n')
        elif self.current_token.type == token.TokenType.EOL:
            # Increment to next Token, skipping EOL Token
            self.current_token = self.get_next_token()
            return None

        # Assignment cannot occur here, must be a SyntaxError
        elif self.current_token.type == token.TokenType.Equals:
            raise SystemExit(f"--- PARSER ERROR ---\n"
                             f"SyntaxError: Cannot perform assignment\n"
                             f"in Character: '{self.current_token.value}'\n"
                             f"in Index: '{self.idx}'\n"
                             f"--- PARSER ERROR ---")

        # Token must be part of existing expression
        # If any previous expressions exist
        if self.prev_expr:
            # Assign current Token to previous expression
            return self.prev_expr.pop(0)

    def create_ast(self):
        """
        Create an Abstract Syntax Tree (AST) from Tokens using Nodes
        :return: Node
        """
        ast = None

        # Tokens exist?
        if len(self.tokens) == 0:
            return ast

        # Repeat until all Tokens are parsed to AST
        while not self.is_eof():
            ast = self.parse_statement()

            # If not EOL (None)
            if ast:
                self.statements.append(ast)

        return self.statements

    def parse(self, expr, tokens):
        """
        Parse a given expression into an Abstract Syntax Tree (AST)
        :param expr: String
        :param tokens: List[Token]
        :return: Node
        """
        self.expr = expr
        self.tokens = tokens
        self.idx = -1
        self.current_token = self.get_next_token()
        self.prev_expr = []
        self.statements = []

        # Create the AST
        self.ast = self.create_ast()
        return self.ast

    def get_ast_tree(self, ast):
        """
        Get entire AST as readable List. Used for debugging
        :param ast: Node
        :return: List[...]
        """
        p_ast = []

        # KeywordNode: (KeywordToken, Node)
        if isinstance(ast, KeywordNode):
            p_ast.append(ast.kw_token.value)
            node = self.get_ast_tree(ast.node)
            p_ast.append(node)

        # BinaryNode: (LeftNode, Operator, RightNode)
        elif isinstance(ast, BinaryNode):
            left = self.get_ast_tree(ast.left)
            p_ast.append(left)
            p_ast.append(ast.op_token.value)
            right = self.get_ast_tree(ast.right)
            p_ast.append(right)

        # UnaryNode: (Operator, Node)
        elif isinstance(ast, UnaryNode):
            p_ast.append(ast.op_token.value)
            node = self.get_ast_tree(ast.node)
            p_ast.append(node)

        # VariableNode: (VarToken, ValToken)
        elif isinstance(ast, VariableNode):
            p_ast.append(ast.var_token.value)
            node = self.get_ast_tree(ast.val_node)
            p_ast.append(node)

        # ValueNode: (Token)
        elif isinstance(ast, ValueNode):
            p_ast.append(ast.token.value)

        return p_ast

    def print_ast(self):
        """
        Print AST List. Used for debugging
        :return: Nothing
        """
        for statement in self.ast:
            p_ast = self.get_ast_tree(statement)
            print(p_ast)
