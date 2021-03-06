from sly import Parser as SlyParser
from .lexer import Lexer
from .types import *

class Parser(SlyParser):
    debugfile = 'logs/parser.out'
    tokens = Lexer.tokens

    precedence = (
        ('left', OR),
        ('left', AND),
        ('left', EQUALITY, INEQUALITY),
        ('left', '+', '-'),
        ('left', '*', '/', '%'),
        ('right', '!')
    )

    @_('empty')
    def program(self, p):
        return ()

    # Statement gatherer ruleset

    @_('statements')
    def program(self, p):
        return p.statements

    @_('statement')
    def statements(self, p):
        return (p.statement, )

    @_('statements statement')
    def statements(self, p):
        return p.statements + (p.statement,)

    @_('function_definition')
    def statement(self, p):
        return p.function_definition

    @_('expr SEP') # Expression;
    def statement(self, p):
        return p.expr

    # Function args ruleset

    @_('expr')
    def arg(self, p):
        return p.expr

    @_('arg')
    def args(self, p):
        return [p.arg]

    @_('args "," arg')
    def args(self, p):
        return p.args + [p.arg]

    @_('empty')
    def args(self, p):
        return []

    # Hold identifier precedence higher 
    @_('ID')
    def expr(self, p):
        return ('id', p.ID)

    # If statement

    @_('if_statement')
    def statement(self, p):
        return p.if_statement

    @_('IF expr block ELSE block')
    def if_statement(self, p):
        return ('if', ('condition', p.expr), ('block', p.block0), ('block', p.block1))

    @_('IF expr block')
    def if_statement(self, p):
        return ('if', ('condition', p.expr), ('block', p.block), None)

    @_('break_loop SEP')
    def statement(self, p):
        return p.break_loop

    @_('for_loop')
    def statement(self, p):
        return p.for_loop

    @_('while_loop')
    def statement(self, p):
        return p.while_loop

    @_('var_assign')
    def statement(self, p):
        return p.var_assign

    @_('data_type var')
    def var_assign(self, p):
        return ('var_assign', p.var, p.data_type)

    @_('BREAK')
    def break_loop(self, p):
        return ('break',)

    @_('FOR var_assign ":" "(" args ")" block')
    def for_loop(self, p):
        return (*p.var_assign, ('for', p.var_assign[1], ('args', p.args), ('block', p.block)))

    @_('WHILE expr block')
    def while_loop(self, p):
        return ('while', p.expr, ('block', p.block))

    # Function declaration

    @_('FN ID "(" params ")" ":" data_type block')
    def function_definition(self, p):
        return ('fn', p.ID, ('params', p.params), ('block', p.block))

    # Function params ruleset

    @_('params "," param')
    def params(self, p):
        return p.params + [p.param]

    @_('param')
    def params(self, p):
        return [p.param]

    @_('empty')
    def params(self, p):
        return []

    @_('data_type ID')
    def param(self, p):
        return (p.ID, p.data_type)

    # Dot notation accessor (a.b)

    @_('accessor "." ID')
    def accessor(self, p):
        return ('.', p.accessor, p.ID)

    @_('ID')
    def accessor(self, p):
        return p.ID

    # Variable Definitions & reassignment

    @_('var_def SEP')
    def statement(self, p):
        return p.var_def

    @_('data_type var "=" expr')
    def var_def(self, p):
        return ('var_define', p.var, p.expr, p.data_type)

    @_('data_type var')
    def var_def(self, p):
        return ('var_define_no_expr', p.var, p.data_type)

    @_('var "=" expr')
    def var_def(self, p):
        return ('var_redefine', p.var, p.expr)

    # Data types

    @_('INT_TYPE')
    def data_type(self, p):
        return int

    @_('STRING_TYPE')
    def data_type(self, p):
        return str

    @_('FLOAT_TYPE')
    def data_type(self, p):
        return float

    @_('NULL_TYPE')
    def data_type(self, p):
        return NullType

    @_('OBJ_TYPE')
    def data_type(self, p):
        return object
        
    @_('BOOL_TYPE')
    def data_type(self, p):
        return bool

    # Expressions

    @_('RETURN expr')
    def expr(self, p):
        return ('return', p.expr)

    @_('literal')
    def expr(self, p):
        return p.literal

    @_('"(" expr ")"') # (expression)
    def expr(self, p):
        return p.expr

    @_('var')
    def expr(self, p):
        return ('var', p.var)

    @_('accessor "(" args ")"') # identifier(args)
    def expr(self, p):
        return ('call', p.accessor, ('args', p.args))

    @_('ID "(" args ")"') # identifier(args)
    def expr(self, p):
        return ('call', p.ID, ('args', p.args))


    # Mathematical Operators

    @_('expr "+" expr')
    def expr(self, p):
        return ('+', p.expr0, p.expr1)

    @_('expr "-" expr')
    def expr(self, p):
        return ('-', p.expr0, p.expr1)

    @_('expr "*" expr')
    def expr(self, p):
        return ('*', p.expr0, p.expr1)

    @_('expr "/" expr')
    def expr(self, p):
        return ('/', p.expr0, p.expr1)

    @_('expr "%" expr')
    def expr(self, p):
        return ('%', p.expr0, p.expr1)

    @_('"!" expr')
    def expr(self, p):
        return ('!', p.expr)

    # logical Operators

    @_('expr OR expr')
    def expr(self, p):
        return ('or', p.expr0, p.expr1)

    @_('expr AND expr')
    def expr(self, p):
        return ('and', p.expr0, p.expr1)

    @_('"(" expr ")" "|" "(" ID ")"')
    def expr(self, p):
        return ('pipe', p.expr, p.ID)

    @_('"(" args ")" "|" "(" ID ")"')
    def expr(self, p):
        return ('pipe', p.args, p.ID)

    @_('expr EQUALITY expr')
    def expr(self, p):
        return ('equal', p.expr0, p.expr1, p.EQUALITY)

    @_('expr INEQUALITY expr')
    def expr(self, p):
        return ('inequal', p.expr0, p.expr1, p.INEQUALITY)

    @_('expr GTHAN expr')
    def expr(self, p):
        return ('gthan', p.GTHAN, p.expr0, p.expr1)

    @_('expr LTHAN expr')
    def expr(self, p):
        return ('lthan', p.LTHAN, p.expr0, p.expr1)

    @_('accessor')
    def expr(self, p):
        return p.accessor

    # Expression Constants

    @_('TRUE')
    def expr(self, p):
        return True

    @_('FALSE')
    def expr(self, p):
        return False

    @_('NULL')
    def expr(self, p):
        return LiteralNull

    # Type Literals

    @_('INT')
    def literal(self, p):
        return p.INT

    @_('FLOAT')
    def literal(self, p):
        return p.FLOAT

    @_('STRING')
    def literal(self, p):
        return p.STRING

    @_('NULL')
    def literal(self, p):
        return LiteralNull

    # Helpers

    @_('ID')
    def var(self, p):
        return p.ID

    @_('ID') 
    def literal(self, p):
        return p.ID

    @_('')
    def empty(self, p):
        pass

    @_('"{" program "}"')
    def block(self, p):
        return p.program

    @_('statement')
    def block(self, p):
        return (p.statement,)
