from sly import Lexer as SlyLexer


class Lexer(SlyLexer):
    # This is the set of tokens we are exporting to the Parser
    tokens = {SEP, ID, FN,
              OR, AND,
              EQUALITY, INEQUALITY, GTHAN, LTHAN,
              TRUE, FALSE,
              FLOAT, INT, STRING, NULL,
              FLOAT_TYPE, INT_TYPE, STRING_TYPE, NULL_TYPE, OBJ_TYPE,
              IF, ELSE}

    ignore = ' \t'
    ignore_comment_slash = r'//.*'

    literals = {'=', '+', '-', '/', '*',
                '(', ')', ',', '{', '}',
                '%', '[', ']', '!', '&',
                '|', '^', '?', ':', '~',
                '.'}

    OR = r'\|\|'
    AND = r'\&\&'
    EQUALITY = r'(===|==)'
    INEQUALITY = r'(!==|!=)'
    GTHAN = r'(>=|>)'
    LTHAN = r'(<=|<)'
    SEP = r';'

    ID = r'[a-zA-Z_][a-zA-Z0-9_]*'
    ID['obj'] = OBJ_TYPE
    ID['int'] = INT_TYPE
    ID['string'] = STRING_TYPE
    ID['float'] = FLOAT_TYPE
    ID['null'] = NULL
    ID['void'] = NULL_TYPE
    ID['true'] = TRUE
    ID['false'] = FALSE
    ID['if'] = IF
    ID['else'] = ELSE
    ID['fn'] = FN

    @_(r'\d+\.\d+')
    def FLOAT(self, t):
        """
        Parsing float numbers
        """
        t.value = float(t.value)
        return t

    @_(r'\d+')
    def INT(self, t):
        """
        Parsing integers
        """
        t.value = int(t.value)
        return t

    @_(r'\n+')
    def ignore_newline(self, t):
        self.lineno += len(t.value)

    def remove_quotes(self, text: str):
        if text.startswith('\"') or text.startswith('\''):
            return text[1:-1]
        return text

    @_(r'''("[^"\\]*(\\.[^"\\]*)*"|'[^'\\]*(\\.[^'\\]*)*')''')
    def STRING(self, t):
        t.value = self.remove_quotes(t.value)
        t.value = t.value.replace(r"\n", "\n")
        t.value = t.value.replace(r"\t", "\t")
        t.value = t.value.replace(r"\\", "\\")
        t.value = t.value.replace(r"\"", "\"")
        t.value = t.value.replace(r"\'", "\'")
        t.value = t.value.replace(r"\a", "\a")
        t.value = t.value.replace(r"\b", "\b")
        t.value = t.value.replace(r"\r", "\r")
        t.value = t.value.replace(r"\t", "\t")
        t.value = t.value.replace(r"\v", "\v")
        return t