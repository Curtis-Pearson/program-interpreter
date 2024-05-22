import token_ as token
import lexer_ as lexer
import parser_ as parser


class Interpreter:
    def __init__(self, debug=False):
        """
        Create a new Interpreter
        """
        self.debug = debug
        self.lexer = lexer.Lexer()
        self.parser = parser.Parser()
        self.variables = dict()

    def eval_ast(self, ast):
        """
        Evaluate a given Abstract Syntax Tree (AST)
        :param ast: Node
        :return: Node or Token
        """
        # Evaluate KeywordNode
        if isinstance(ast, parser.KeywordNode):
            self.eval_kw_node(ast)

        # Evaluate UnaryNode
        elif isinstance(ast, parser.UnaryNode):
            return self.eval_unary_node(ast)

        # Evaluate BinaryNode
        elif isinstance(ast, parser.BinaryNode):
            return self.eval_binary_node(ast)

        elif isinstance(ast, parser.VariableNode):
            return self.eval_variable_node(ast)

        # Provide Token from ValueNode
        elif isinstance(ast, parser.ValueNode):
            return ast.token

        # Provided AST/Node not valid
        # Previous Node requires current Node to have value
        else:
            raise SystemExit(f"--- INTERPRETER ERROR ---\n"
                             f"SyntaxError: AST Node contains 'None' value\n"
                             f"--- INTERPRETER ERROR ---")

    def eval_kw_node(self, kw_node):
        """
        Evaluate a given KeywordNode
        :param kw_node: KeywordNode
        :return: Nothing
        """
        # Printing an expression
        if kw_node.kw_token.value == 'print':
            # Evaluate Node of print expression
            to_print = self.eval_ast(kw_node.node)

            # Printing a single Variable
            if to_print.type == token.TokenType.Variable:
                # Does the Variable exist?
                try:
                    print(self.variables[to_print.value].value)

                # Variable does not exist
                except KeyError:
                    raise SystemExit(f"--- INTERPRETER ERROR---\n"
                                     f"PrintError: Cannot Print non-existent Variable\n"
                                     f"in Variable: '{to_print.value}'\n"
                                     f"in Keyword: '{kw_node.kw_token.value}'\n"
                                     f"--- INTERPRETER ERROR---")

            # Print entire valid expression
            else:
                print(to_print.value)

        # Delete a Variable from the program memory
        elif kw_node.kw_token.value == 'del':
            # Does the Variable exist?
            try:
                self.variables.pop(kw_node.node.token.value)

            # Variable does not exist
            except KeyError:
                # Cannot delete
                if isinstance(kw_node.node, parser.ValueNode):
                    # Attempt to delete non-existent Variable
                    if kw_node.node.token.type == token.TokenType.Variable:
                        raise SystemExit(f"--- INTERPRETER ERROR---\n"
                                         f"DeletionError: Cannot delete non-existent Variable\n"
                                         f"in Variable: '{kw_node.node.token.value, kw_node.node.token.type}'\n"
                                         f"in Keyword: '{kw_node.kw_token.value}'\n"
                                         f"--- INTERPRETER ERROR---")

                    # Attempt to delete non-Variable Token
                    else:
                        raise SystemExit(f"--- INTERPRETER ERROR---\n"
                                         f"DeletionError: Cannot delete non-Variable Token\n"
                                         f"in Token: '{kw_node.node.token.value, kw_node.node.token.type}'\n"
                                         f"in Keyword: '{kw_node.kw_token.value}'\n"
                                         f"--- INTERPRETER ERROR---")

                # Attempt to delete non-Variable Node
                else:
                    raise SystemExit(f"--- INTERPRETER ERROR---\n"
                                     f"DeletionError: Cannot delete non-Variable Node\n"
                                     f"in Node: '{kw_node.node}'\n"
                                     f"in Keyword: '{kw_node.kw_token.value}'\n"
                                     f"--- INTERPRETER ERROR---")

            # Attempt to delete Node
            except AttributeError:
                raise SystemExit(f"--- INTERPRETER ERROR---\n"
                                 f"DeletionError: Cannot delete Node\n"
                                 f"in Node: '{kw_node.node}'\n"
                                 f"in Keyword: '{kw_node.kw_token.value}'\n"
                                 f"--- INTERPRETER ERROR---")

    def eval_unary_node(self, unary_node):
        """
        Evaluate a given UnaryNode
        :param unary_node: UnaryNode
        :return: Token
        """
        # Evaluate Node of UnaryNode (Operator, Node) to get Token
        sub_node = self.eval_ast(unary_node.node)

        # Token is Variable
        if sub_node.type == token.TokenType.Variable:
            # Does the Variable exist?
            try:
                sub_node = self.variables[sub_node.value]

            # Cannot unary non-existent Variable
            except KeyError:
                raise SystemExit(f"--- INTERPRETER ERROR ---\n"
                                 f"ValueError: Cannot perform Unary Operation on non-existent Variable\n"
                                 f"in Variable: '{sub_node.value, sub_node.type}'\n"
                                 f"in Operation: '{unary_node.op_token.value}'\n"
                                 f"--- INTERPRETER ERROR ---")

        # Token is Numeric
        if sub_node.type in [token.TokenType.Integer, token.TokenType.Float]:
            return self.eval_numeric_unary_expr(sub_node, unary_node.op_token.value)

        # Token is Boolean
        elif sub_node.type == token.TokenType.Boolean:
            return self.eval_conditional_unary_expr(sub_node, unary_node.op_token.value)

        # Cannot perform Unary operation on non-Numeric or non-Boolean TokenType
        raise SystemExit(f"--- INTERPRETER ERROR ---\n"
                         f"ValueError: Cannot perform Unary Operation on TokenType '{sub_node.type}'\n"
                         f"in Token: '{sub_node.value, sub_node.type}'\n"
                         f"in Operation: '{unary_node.op_token.value}'\n"
                         f"--- INTERPRETER ERROR ---")

    def eval_numeric_unary_expr(self, num_token, op_val):
        """
        Evaluate numeric UnaryNode expression
        :param num_token: Token
        :param op_val: String
        :return: Token
        """
        # Invert sign
        if op_val == '-':
            # Convert Token from string ('10' = 10)
            num_token.convert_from_string()
            # Flip the number's sign
            num_token.value = -num_token.value
            # Convert Token back to string
            num_token.convert_to_string()
        return num_token

    def eval_conditional_unary_expr(self, bool_token, op_val):
        """
        Evaluate boolean UnaryNode expression
        :param bool_token: Token
        :param op_val: String
        :return: Token
        """
        # Operator is unary operation '!' or 'not' keyword
        if op_val in ['!', 'not']:
            # Convert Token from string ('true' = True, 'false' = False)
            bool_token.convert_from_string()
            # Flip the boolean value
            bool_token.value = not bool_token.value
            # Convert Token back to string
            bool_token.convert_to_string()
        return bool_token

    def eval_binary_node(self, binary_node):
        """
        Evaluate a given BinaryNode
        :param binary_node: BinaryNode
        :return: Token
        """
        # Evaluate LeftNode and RightNode of BinaryNode (LeftNode, Operator, RightNode) to get Tokens
        left = self.eval_ast(binary_node.left)
        right = self.eval_ast(binary_node.right)

        # LeftToken is Variable
        if left.type == token.TokenType.Variable:
            # Token.value Variable exists
            try:
                left = self.variables[left.value]

            # Variable does not exist
            except KeyError:
                raise SystemExit(f"--- INTERPRETER ERROR ---\n"
                                 f"ValueError: Variable used before assignment\n"
                                 f"in Variable '{left.value}'\n"
                                 f"--- INTERPRETER ERROR ---")

        # RightToken is Variable
        if right.type == token.TokenType.Variable:
            # Token.value Variable exists
            try:
                right = self.variables[right.value]

            # Variable does not exist
            except KeyError:
                raise SystemExit(f"--- INTERPRETER ERROR ---\n"
                                 f"ValueError: Variable used before assignment\n"
                                 f"in Variable '{right.value}'\n"
                                 f"--- INTERPRETER ERROR ---")

        # LeftToken and RightToken are Numeric
        if (left.type in [token.TokenType.Integer, token.TokenType.Float]) and \
                (right.type in [token.TokenType.Integer, token.TokenType.Float]):

            # Operator is numeric binary operation keyword
            if binary_node.op_token.value in ['+', '-', '*', '/', '%', '**']:
                return self.eval_numeric_binary_expr(left, right, binary_node.op_token.value)

            # Operator is boolean binary operation expression
            elif binary_node.op_token.value in ['==', '!=', '>', '<', '>=', '<=']:
                return self.eval_boolean_binary_expr(left, right, binary_node.op_token.value)

        # LeftToken and RightToken are Boolean
        elif (left.type == token.TokenType.Boolean) and (right.type == token.TokenType.Boolean):
            return self.eval_conditional_binary_expr(left, right, binary_node.op_token.value)

        # LeftToken and RightToken are String
        elif (left.type == token.TokenType.String) and (right.type == token.TokenType.String):
            return self.eval_string_binary_expr(left, right, binary_node.op_token.value)

        # Cannot perform action on non-matching LeftToken and RightToken TokenType
        raise SystemExit(f"--- INTERPRETER ERROR ---\n"
                         f"ValueError: Mis-match in Binary Operation TokenType\n"
                         f"in Left: '{left.value, left.type}'\n"
                         f"in Right: '{right.value, right.type}'\n"
                         f"in Operator: '{binary_node.op_token.value}'\n"
                         f"--- INTERPRETER ERROR ---")

    def eval_numeric_binary_expr(self, left_token, right_token, op_val):
        """
        Evaluate numeric BinaryNode expression
        :param left_token: Token
        :param right_token: Token
        :param op_val: String
        :return: Token
        """
        # Convert LeftToken and RightToken values from strings
        left_token.convert_from_string()
        right_token.convert_from_string()

        # Obtain LeftToken and RightToken values
        left_val = left_token.value
        right_val = right_token.value
        result = None

        # Addition
        if op_val == '+':
            result = str(left_val + right_val)

        # Subtraction
        elif op_val == '-':
            result = str(left_val - right_val)

        # Multiplication
        elif op_val == '*':
            result = str(left_val * right_val)

        # Division
        elif op_val == '/':
            # Division by Zero
            if right_val == 0.0:
                result = str(0.0)
            else:
                result = str(left_val / right_val)

        # Modulus
        elif op_val == '%':
            # Modulus by Zero
            if right_val == 0.0:
                result = str(0.0)
            else:
                result = str(left_val % right_val)

        # Indices
        elif op_val == '**':
            result = str(left_val ** right_val)

        # Return new Token
        return token.Token(result)

    def eval_boolean_binary_expr(self, left_token, right_token, op_val):
        """
        Evaluate boolean BinaryNode expression
        :param left_token: Token
        :param right_token: Token
        :param op_val: String
        :return: Token
        """
        # Convert LeftToken and RightToken from strings
        left_token.convert_from_string()
        right_token.convert_from_string()

        # Obtain LeftToken and RightToken values
        left_val = left_token.value
        right_val = right_token.value
        result = None
        # Boolean comparisons must be converted to str().lower() to identify TokenType

        # Equal to
        if op_val == '==':
            result = str(left_val == right_val).lower()

        # Not equal to
        elif op_val == '!=':
            result = str(left_val != right_val).lower()

        # Greater than
        elif op_val == '>':
            result = str(left_val > right_val).lower()

        # Less than
        elif op_val == '<':
            result = str(left_val < right_val).lower()

        # Greater than or equal to
        elif op_val == '>=':
            result = str(left_val >= right_val).lower()

        # Less than or equal to
        elif op_val == '<=':
            result = str(left_val <= right_val).lower()

        # Return new token
        return token.Token(result)

    def eval_conditional_binary_expr(self, left_token, right_token, op_val):
        """
        Evaluate conditional BinaryNode expression
        :param left_token: Token
        :param right_token: Token
        :param op_val: String
        :return: Token
        """
        # Convert LeftToken and RightToken from strings
        left_token.convert_from_string()
        right_token.convert_from_string()

        # Obtain LeftToken and RightToken values
        left_val = left_token.value
        right_val = right_token.value
        result = None

        # And
        if op_val == 'and':
            result = left_val and right_val

        # Or
        elif op_val == 'or':
            result = left_val or right_val

        # Equal to
        elif op_val == '==':
            result = left_val is right_val

        # Not equal to
        elif op_val == '!=':
            result = left_val is not right_val

        # Create new Token and manually define TokenType as Boolean
        result_token = token.Token(result, t_type=token.TokenType.Boolean)
        # Convert Boolean to String and return new Token
        result_token.convert_to_string()
        return result_token

    def eval_string_binary_expr(self, left_token, right_token, op_val):
        """
        Evaluate string BinaryNode expression
        :param left_token: Token
        :param right_token: Token
        :param op_val: String
        :return: Token
        """
        # Obtain LeftToken and RightToken String values
        left_val = left_token.value
        right_val = right_token.value
        result = None
        t_type = None
        # Concatenation generates new String whilst Comparison generates Boolean

        # Concatenate
        if op_val == '+':
            result = left_val + right_val
            t_type = token.TokenType.String

        # Equal to
        elif op_val == '==':
            result = str(left_val == right_val).lower()
            t_type = token.TokenType.Boolean

        # Not equal to
        elif op_val == '!=':
            result = str(left_val != right_val).lower()
            t_type = token.TokenType.Boolean

        # Create new Token and manually define TokenType by Operation, then return new Token
        return token.Token(result, t_type=t_type)

    def eval_variable_node(self, var_node):
        val_token = self.eval_ast(var_node.val_node)
        self.variables[var_node.var_token.value] = val_token
        return self.variables[var_node.var_token.value]

    def execute(self, expr):
        """
        Execute a given expression for its result
        :param expr: String
        """
        # Clear memory
        self.variables = dict()

        # Tokenize expression
        tokens = self.lexer.tokenize(expr)

        if self.debug:
            self.lexer.print_tokens()

        # Parse Tokens to Abstract Syntax Tree (AST)
        ast = self.parser.parse(expr, tokens)

        if self.debug:
            self.parser.print_ast()

        # Evaluate AST
        for statement in ast:
            self.eval_ast(statement)
