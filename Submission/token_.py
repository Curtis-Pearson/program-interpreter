from enum import Enum


# Identify if character is alpha, numeric, or symbolic during tokenization
class IdentifierType(Enum):
    Alpha = 1
    Numeric = 2
    Symbolic = 3
    Unknown = 4

    @classmethod
    def get_identifier_type(cls, char):
        if ('A' <= char <= 'Z') or ('a' <= char <= 'z') or char == '_':
            return cls.Alpha

        elif ('0' <= char <= '9') or char in '.-':
            return cls.Numeric

        else:
            return cls.Symbolic


# Token type identifiers for tokenization and parsing
class TokenType(Enum):
    Integer = "Integer"
    Float = "Float"
    Boolean = "Boolean"
    String = "String"
    Variable = "Variable"
    Equals = "Equals"
    UnaryOperation = "UnaryOperation"
    BinaryOperation = "BinaryOperation"
    LeftParen = "LeftParen"
    RightParen = "RightParen"
    EOL = "EOL"
    ReservedKeyword = "ReservedKeyword"
    NoneType = "NoneType"
    EOF = "EOF"
    Invalid = "Invalid"


# Specific reserved character(s) for each token type
TokenTypes = {
    'Boolean': ['true', 'false'],
    'String': ['"', "'"],
    'Equals': ['='],
    'UnaryOperation': ['!', 'not'],
    'BinaryOperation': ['+', '-', '*', '/', '%', '**', '==', '!=', '>', '<', '>=', '<=', 'and', 'or'],
    'LeftParen': ['('],
    'RightParen': [')'],
    'ReservedKeyword': ['print', 'del'],
    'NoneType': ['None'],
    'EOL': ['\n', '\r'],
    'EOF': ['EOF']
}


class Token:
    def __init__(self, value, t_type=None):
        """
        Create a new Token
        :param value: String
        :param t_type: TokenType
        """
        self.value = value

        # If self.type is pre-defined or not
        if t_type is None:
            self.type = self.identify_type()
        else:
            self.type = t_type

    def identify_type(self):
        """
        Identify TokenType by self.value
        :return: TokenType
        """
        # Is the token a Float?
        if '.' in self.value:
            try:
                float(self.value)
                return TokenType.Float
            except ValueError:
                pass
        # Is the token an Integer?
        else:
            try:
                int(self.value)
                return TokenType.Integer
            except ValueError:
                pass

        # If prefix and suffix are '" "', then TokenType is String
        if (self.value[0] == '\"') and self.value[-1] == '\"':
            return TokenType.String

        # Is self.value in TokenTypes reserved character(s)?
        for t_type in TokenTypes:
            if self.value in TokenTypes[t_type]:
                return TokenType(t_type)

        # Default to Variable
        return TokenType.Variable

    def convert_from_string(self):
        """
        Convert Numeric and Boolean values to String counter-parts
        :return: Integer, Float, or Boolean
        """
        if self.type == TokenType.Integer:
            self.value = int(self.value)

        elif self.type == TokenType.Float:
            self.value = float(self.value)

        elif self.type == TokenType.Boolean:
            if self.value == 'true':
                self.value = True
            else:
                self.value = False

    def convert_to_string(self):
        """
        Convert String to Numeric and Boolean counter-parts
        :return: String
        """
        if self.type in [TokenType.Integer, TokenType.Float]:
            self.value = str(self.value)

        elif self.type == TokenType.Boolean:
            if self.value:
                self.value = 'true'
            else:
                self.value = 'false'
