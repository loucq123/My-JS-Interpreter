import ply.lex as lex


states = (('comment', 'exclusive'),)

# comment state rules

def t_comment(t):
    r'\/\*'
    t.lexer.begin('comment')

def t_comment_END(t):
    r'\*\/'
    #t.lexer.lineno += t.value.count('\n')
    t.lexer.begin('INITIAL')
    pass

def t_comment_newline(t):
    r'\n'
    t.lexer.lineno += 1

def t_comment_error(t):
    # print "JavaScript Lexer (comment state): Illegal character " + t.value[0]
    t.lexer.skip(1)

reserved = {
    'if' : 'IF',
    'else' : 'ELSE',
    'false' : 'FALSE',
    'true' : 'TRUE',
    'return' : 'RETURN',
    'function' : 'FUNCTION',
    'var' : 'VAR',
}

tokens = [
        'ANDAND',       # &&
        'COMMA',        # ,
        'DIVIDE',       # /
        'ELSE',         # else
        'EQUAL',        # =
        'EQUALEQUAL',   # ==
        'FALSE',        # false
        'FUNCTION',     # function
        'GE',           # >=
        'GT',           # >
        'IDENTIFIER',   #### Not used in this problem.
        'IF',           # if
        'LBRACE',       # {
        'LE',           # <=
        'LPAREN',       # (
        'LT',           # <
        'MINUS',        # -
        'NOT',          # !
        'NUMBER',       #### Not used in this problem.
        'OROR',         # ||
        'PLUS',         # +
        'RBRACE',       # }
        'RETURN',       # return
        'RPAREN',       # )
        'SEMICOLON',    # ;
        'STRING',       #### Not used in this problem. 
        'TIMES',        # *
        'TRUE',         # true
        'VAR',          # var
] + list(reserved)

def t_EOLCOMMENT(t):
    r'//.*'
    pass

def t_newline(t):
    r'\n'
    t.lexer.lineno += 1

def t_error(t):
    print ("JavaScript Lexer: Illegal character " + t.value[0])
    t.lexer.skip(1)

t_ANDAND = r'&&'
t_COMMA = r','
t_DIVIDE = r'/'
t_ELSE = r'else'
t_EQUALEQUAL = r'=='
t_EQUAL = r'='
t_FALSE = r'false'
t_FUNCTION = r'function'
t_GE = r'>='
t_GT = r'>'
t_IF = r'if'
t_LBRACE = r'{'
t_LE = r'<='
t_LPAREN = r'\('
t_LT = r'<'
t_MINUS = r'-'
t_NOT = r'!'
t_OROR = r'\|\|'
t_PLUS = r'\+'
t_RBRACE = r'}'
t_RETURN = r'return'
t_RPAREN = r'\)'
t_SEMICOLON = r';'
t_TIMES = r'\*'
t_TRUE = r'true'
t_VAR = r'var'

def t_IDENTIFIER(t):
    r'[A-Za-z][A-Za-z_]*' 
    t.type = reserved.get(t.value, 'IDENTIFIER')   
    return t

def t_NUMBER(t):
    r'-?[0-9]+(?:\.[0-9]*)?'
    t.value = float(t.value)
    return t

def t_STRING(t):
    r'"(?:[^"\\]|(?:\\.))*"'
    t.value = t.value[1:-1]
    return t

t_ignore = ' \t\v\r' # whitespace
t_comment_ignore = ' \t\v\r'
