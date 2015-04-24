import myJsLexer
from myJsLexer import tokens
import ply.lex as lex


jslexer = lex.lex(module=myJsLexer)
def test_lexer(input_string):
	jslexer.input(input_string)
	result = []
	while True:
		tok = jslexer.token()
		if not tok:
			break
		result = result + [tok.type]
	return result

def test():
	input1 = """ - !  && () * , / ; { || } + < <= = == > >= else false function
		if return true var """
	output1 = ['MINUS', 'NOT', 'ANDAND', 'LPAREN', 'RPAREN', 'TIMES', 'COMMA',
		'DIVIDE', 'SEMICOLON', 'LBRACE', 'OROR', 'RBRACE', 'PLUS', 'LT', 'LE',
		'EQUAL', 'EQUALEQUAL', 'GT', 'GE', 'ELSE', 'FALSE', 'FUNCTION', 'IF',
		'RETURN', 'TRUE', 'VAR']
		
	input2 = """
		if // else mystery  
		=/*=*/= 
		true /* false 
		*/ return"""
	output2 = ['IF', 'EQUAL', 'EQUAL', 'TRUE', 'RETURN']

	input3 = 'some_identifier -12.34 "a \\"escape\\" b" if'
	output3 = ['IDENTIFIER', 'NUMBER', 'STRING', 'IF']

	assert test_lexer(input1) == output1
	assert test_lexer(input2) == output2
	assert test_lexer(input3) == output3
	print "tests pass"

if __name__ == '__main__':
	test()



