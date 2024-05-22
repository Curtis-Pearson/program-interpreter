import token_ as token


class Lexer:
    def __init__(self):
        """
        Create a new Lexer
        """
        self.expr = ""
        self.text = ""
        self.tokens = []

    def convert_escape_chars(self):
        """
        Convert '\' Python reserved characters to token-able characters
        :return: Nothing
        """
        text = self.text

        # Counter to maintain same length when changing characters in-place
        j = 0
        for i in range(0, len(text), 1):
            char = text[i]

            # Character is a Backslash
            if char == '\\' and i < (len(text) - 1):
                # Check next character
                next_char = text[i + 1]
                replacement_char = ' '

                # New Line (EOL)
                if next_char == 'n':
                    replacement_char = '\n'
                # Tab
                elif next_char == 't':
                    replacement_char = '\t'

                # If the '\' character combined with the next character is '\n' or '\t'
                if replacement_char != ' ':
                    # Remove the extra '\' in-place
                    self.text = self.text[:i - j] + replacement_char + self.text[i + 2 - j:]
                    j += 1

    def get_next_identifier(self):
        """
        Get the next whole Token value from the rest of the expression
        :return: String
        """
        # Set local variables for current Token
        # Defined in token_.py
        identifier_type = token.IdentifierType.Unknown
        # Token value
        next_identifier = ''
        # Token end index
        next_identifier_end = 0
        # String identifier
        is_string = False

        # For each char in text
        for char in self.text:
            # If not currently is_string
            if not is_string:
                # Character denotes the start of a string
                if char == '\"':
                    # Start a new string
                    is_string = True
                    next_identifier_end += 1
                    next_identifier += char
                    continue

            # Store entire string as a single Token
            if is_string:
                next_identifier_end += 1
                next_identifier += char

                # Character doesn't denote the end of a string
                if char != '\"':
                    continue
                # Character denotes the end of a string
                else:
                    break

            # Character is parenthesis
            if char in '()':
                # Only allow Token length of 1 for single parenthesis
                if next_identifier_end == 0:
                    next_identifier_end += 1
                    next_identifier += char
                break

            # Ignore space and tab characters
            if char not in ' \t':
                # Character is line break and nothing else
                if char == '\n' and len(next_identifier) == 0:
                    next_identifier_end += 1
                    next_identifier += char
                    break

                # Get IdentifierType from first character
                current_identifier_type = token.IdentifierType.get_identifier_type(char)

                # Start of identifier, assign to type of character
                if identifier_type == token.IdentifierType.Unknown:
                    identifier_type = current_identifier_type

                # Not the start of identifier
                else:
                    # IdentifierType is number
                    if identifier_type == token.IdentifierType.Numeric:
                        # Current Token isn't empty and character isn't numeric, e.g. '0-4' becomes ['0', '-4']
                        if len(next_identifier) > 0 and \
                                (char == '-' or current_identifier_type != token.IdentifierType.Numeric):
                            break

                    # Prevent symbolic Tokens from merging with other Tokens
                    if (identifier_type == token.IdentifierType.Symbolic and
                        current_identifier_type != token.IdentifierType.Symbolic) or \
                            (identifier_type != token.IdentifierType.Symbolic and
                             (current_identifier_type == token.IdentifierType.Symbolic or char == '-')):
                        break

                # Add character to current Token
                next_identifier += char

            # If character is space or tab, and Token has characters already
            elif len(next_identifier) > 0:
                break

            # Increment Token end index
            next_identifier_end += 1

        # Remove identified Token from self.text and return Token
        self.text = self.text[next_identifier_end:]
        return next_identifier

    def tokenize(self, expr):
        """
        Tokenize the current expression
        :param expr: String
        :return: List[Token]
        """
        self.expr = expr
        self.text = expr
        self.tokens = []
        self.convert_escape_chars()

        # Iterate over each token in the text
        while len(self.text) > 0:
            next_identifier = self.get_next_identifier()

            # Ignore None Tokens
            if not next_identifier:
                continue

            # Append self.tokens with new Token
            new_token = token.Token(next_identifier)
            self.tokens.append(new_token)

        # Append self.tokens with End of File (EOF) for the Parser
        self.tokens.append(token.Token("EOF", token.TokenType.EOF))
        return self.tokens

    def print_tokens(self):
        """
        Print all Tokens from Lexer (token.value, token.type). Used for debugging
        :return: Nothing
        """
        print(self.expr)
        tka = [tk.value for tk in self.tokens]
        print(tka)
        for tkb in self.tokens:
            print(tkb.value, "\t", tkb.type)
