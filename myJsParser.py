# JavaScript grammar
#
# The starting non-terminal is "js" for "JavaScript program" -- which is
# just a list of "elements" (to be defined shortly). The parse tree you
# must return is simply a list containing all of the elements.  
#
#       js -> element js
#       js -> 
#
# An element is either a function declaration: 
#
#       element -> FUNCTION IDENTIFIER ( optparams ) compoundstmt
#
# or a statement following by a semi-colon: 
#
#       element -> stmt ; 
#       
# The parse tree for the former is the tuple ("function",name,args,body),
# the parse tree for the latter is the tuple ("stmt",stmt). 
#
#       optparams ->
#       optparams -> params
#       params -> IDENTIFIER , params
#       params -> IDENTIFIER
#
# optparams is a comma-separated list of zero or more identifiers. The
# parse tree for optparams is the list of all of the identifiers. 
#
#       compoundstmt -> { statements } 
#       statements -> stmt ; statements
#       statements -> 
#
# A compound statement is a list of zero or more statements, each of which
# is followed by a semicolon. (In real JavaScript, some statements do not
# need to be followed by a semicolon. For simplicity, we will assume that
# they all have to.) The parse tree for a compound statement is just the
# list of all of the statements. 
#
# We will consider six kinds of possible statements: 
#
#       stmt -> IF exp compoundstmt     
#       stmt -> IF exp compoundstmt ELSE compoundstmt
#       stmt -> IDENTIFIER = exp 
#       stmt -> RETURN exp 
#
# The "if", "assignment" and "return" statements should be familiar. It is
# also possible to use "var" statements in JavaScript to introduce new
# local variables (this is not necessary in Python): 
#
#       stmt -> VAR IDENTIFIER = exp 
#
# And it is also possible to treat an expression as a statement. This is
#
#       stmt -> exp 
#
# The parse trees for statements are all tuples:
#       ("if-then", conditional, then_branch)
#       ("if-then-else", conditional, then_branch, else_branch)
#       ("assign", identifier, new_value) 
#       ("return", expression)
#       ("var", identifier, initial_value) 
#       ("exp", expression) 
#
# To simplify things, for now we will assume that there is only one type of
# expression: identifiers that reference variables. In the next assignment,
# we'll encoding the parsing rules for expressions.
#
# Recall the names of our tokens: 
#
# 'ANDAND',       # &&          | 'LT',           # <
# 'COMMA',        # ,           | 'MINUS',        # -
# 'DIVIDE',       # /           | 'NOT',          # !
# 'ELSE',         # else        | 'NUMBER',       # 1234 
# 'EQUAL',        # =           | 'OROR',         # ||
# 'EQUALEQUAL',   # ==          | 'PLUS',         # +
# 'FALSE',        # FALSE       | 'RBRACE',       # }
# 'FUNCTION',     # function    | 'RETURN',       # return
# 'GE',           # >=          | 'RPAREN',       # )
# 'GT',           # >           | 'SEMICOLON',    # ;
# 'IDENTIFIER',   # factorial   | 'STRING',       # "hello"
# 'IF',           # if          | 'TIMES',        # *
# 'LBRACE',       # {           | 'TRUE',         # TRUE
# 'LE',           # <=          | 'VAR',          # var 
# 'LPAREN',       # (           |

import ply.yacc as yacc
import ply.lex as lex
import myJsLexer                 # use my JavaScript lexer
from myJsLexer import tokens     # use my JavaScript tokens


start = 'js'

precedence = (
    ('left', 'OROR'),
	('left', 'ANDAND'),
	('left', 'EQUALEQUAL'),
	('left', 'LT', 'GT', 'LE', 'GE'),
	('left', 'PLUS', 'MINUS'),
	('left', 'TIMES', 'DIVIDE'),
	('right', 'NOT'),
) 

def p_js(p): 
    'js : element js'
    p[0] = [p[1]] + p[2]

def p_js_empty(p):
    'js : '
    p[0] = []

def p_element_function(p):
	'element : FUNCTION IDENTIFIER LPAREN optparams RPAREN compoundstmt'
	p[0] = ('function', p[2], p[4], p[6])

def p_element_stmt(p):
	'element : stmt SEMICOLON'
	p[0] = ('stmt', p[1])

def p_optparams(p):
	'optparams : params'
	p[0] = p[1]

def p_optparams_empty(p):
	'optparams : '
	p[0] = []

def p_params_one(p):
	'params : IDENTIFIER'
	p[0] = [p[1]]

def p_params_multi(p):
	'params : IDENTIFIER COMMA params'
	p[0] = [p[1]] + p[3]

def p_compoundstmt(p):
	'compoundstmt : LBRACE stmts RBRACE'
	p[0] = p[2]

def p_statements(p):
	'stmts : stmt SEMICOLON stmts'
	p[0] = [p[1]] + p[3]

def p_statements_empty(p):
	'stmts : '
	p[0] = []

def p_stmt_if(p):
	'stmt : IF exp compoundstmt'
	p[0] = ('if-then', p[2], p[3])

def p_stmt_ifelse(p):
	'stmt : IF exp compoundstmt ELSE compoundstmt'
	p[0] = ('if-then-else', p[2], p[3], p[5])

def p_stmt_IDENTIFIER(p):
	'stmt : IDENTIFIER EQUAL exp'
	p[0] = ('assign', p[1], p[3])

def p_stmt_RETURN(p):
	'stmt : RETURN exp'
	p[0] = ('return', p[2])

def p_stmt_VAR(p):
	'stmt : VAR IDENTIFIER EQUAL exp'
	p[0] = ('var', p[2], p[4])

def p_stmt_exp(p):
	'stmt : exp'
	p[0] = ('exp', p[1])

# Here's the rules for simple expressions.

def p_exp_identifier(p): 
    'exp : IDENTIFIER'
    p[0] = ("identifier",p[1]) 

def p_exp_number(p):
    'exp : NUMBER'
    p[0] = ('number',p[1])

def p_exp_string(p):
    'exp : STRING'
    p[0] = ('string',p[1])
    
def p_exp_true(p):
    'exp : TRUE'
    p[0] = ('true','true')
    
def p_exp_false(p):
    'exp : FALSE'
    p[0] = ('false','false')
    
def p_exp_not(p):
    'exp : NOT exp'
    p[0] = ('not', p[2])

def p_exp_parens(p):
    'exp : LPAREN exp RPAREN'
    p[0] = p[2]

def p_exp_andand(p):
	'''exp : exp OROR exp
	       | exp ANDAND exp
	       | exp EQUALEQUAL exp
	       | exp LT exp
	       | exp GT exp
	       | exp LE exp
	       | exp GE exp
	       | exp PLUS exp
	       | exp MINUS exp
	       | exp TIMES exp
	       | exp DIVIDE exp'''
	p[0] = ('binop', p[1], p[2], p[3])

def p_exp_IDENTIFIER(p):
	'exp : IDENTIFIER LPAREN optargs RPAREN'
	p[0] = ('call', p[1], p[3])

def p_optargs_empty(p):
	'optargs : '
	p[0] = []

def p_optargs(p):
	'optargs : args'
	p[0] = p[1]

def p_args_multi(p):
	'args : exp COMMA args'
	p[0] = [p[1]] + p[3]

def p_args_one(p):
	'args : exp'
	p[0] = [p[1]]

