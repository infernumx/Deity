from sly import Lexer as SlyLexer


class Lexer(SlyLexer):
    tokens = {SEP, ID, FN,
              OR, AND,
              EQUALITY, INEQUALITY, GTHAN, LTHAN,
              TRUE, FALSE,
              FLOAT, INT, STRING, NULL,
              FLOAT_TYPE, INT_TYPE, STRING_TYPE, BOOL_TYPE, NULL_TYPE, OBJ_TYPE,
              IF, ELSE, RETURN, FOR, WHILE}

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
    ID['void'] = NULL_TYPE
    ID['boolean'] = BOOL_TYPE
    ID['null'] = NULL
    ID['true'] = TRUE
    ID['false'] = FALSE
    ID['if'] = IF
    ID['else'] = ELSE
    ID['fn'] = FN
    ID['return'] = RETURN
    ID['for'] = FOR
    ID['while'] = WHILE

    @_(r'\d+\.\d+')
    def FLOAT(self, t):
        t.value = float(t.value)
        return t

    @_(r'\d+')
    def INT(self, t):
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
        chars = ((r'\n', '\n'), (r'\t', '\t'), (r'\\', '\\'),
                 (r'\"', '\"'), (r'\'', '\''), (r'\a', '\a'),
                 (r'\b', '\b'), (r'\r', '\r'), (r'\v', '\v'))
        for pair in chars:
            t.value = t.value.replace(*pair)
        return t
