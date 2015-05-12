import myJsLexer
import ply.lex as lex


jslexer = lex.lex(module=myJsLexer)


def test_lexer(input_string):
    jslexer.input(input_string)
    result = []
    while True:
        tok = jslexer.token()
        if not tok:
            break
        result += [(tok.type, tok.value)]
    return result


def test_single_token():
    single_tokens = '''if else false true return function var && || , ;  = == 
                       >= > <= < { } ( ) ! + - * / '''
    types_of_tokens = [('IF', 'if'), ('ELSE', 'else'), ('FALSE', 'false'), ('TRUE', 'true'),
                       ('RETURN', 'return'), ('FUNCTION', 'function'), ('VAR', 'var'),
                       ('ANDAND', '&&'), ('OROR', '||'), ('COMMA', ','), ('SEMICOLON', ';'),
                       ('EQUAL', '='), ('EQUALEQUAL', '=='), ('GE', '>='), ('GT', '>'),
                       ('LE', '<='), ('LT', '<'), ('LBRACE', '{'), ('RBRACE', '}'), ('LPAREN', '('),
                       ('RPAREN', ')'), ('NOT', '!'), ('PLUS', '+'), ('MINUS', '-'), ('TIMES', '*'),
                       ('DIVIDE', '/')]
    assert test_lexer(single_tokens) == types_of_tokens


def test_number():
    numbers = '1 0 -1 123 -123 1.12 -1.12 0.1 -0.1'
    types_of_numbers = [('NUMBER', 1), ('NUMBER', 0), ('NUMBER', -1), ('NUMBER', 123), ('NUMBER', -123),
                        ('NUMBER', 1.12), ('NUMBER', -1.12), ('NUMBER', 0.1), ('NUMBER', -0.1)]
    assert test_lexer(numbers) == types_of_numbers


def test_string():
    strings = '"fuck" "shit" "f" "s" "1" "123" "_+" "-+123" "123lou" "lou_+"'
    strings_types = [('STRING', 'fuck'), ('STRING', 'shit'), ('STRING', 'f'), ('STRING', 's'),
                     ('STRING', '1'), ('STRING', '123'), ('STRING', '_+'), ('STRING', '-+123'),
                     ('STRING', '123lou'), ('STRING', 'lou_+')]
    assert test_lexer(strings) == strings_types


def test_identifier():
    ids = 'x _ __ abc _cba iem9 _2 _c4 _4c c_4 c4_'
    id_types = [('IDENTIFIER', 'x'), ('IDENTIFIER', '_'), ('IDENTIFIER', '__'), ('IDENTIFIER', 'abc'),
                ('IDENTIFIER', '_cba'), ('IDENTIFIER', 'iem9'), ('IDENTIFIER', '_2'), ('IDENTIFIER', '_c4'),
                ('IDENTIFIER', '_4c'), ('IDENTIFIER', 'c_4'), ('IDENTIFIER', 'c4_')]
    assert test_lexer(ids) == id_types


def test_comment():
    input1 = ''' /*hello*/'''
    output1 = []

    input2 = '''if hello else /*nothing*/ "yes"'''
    output2 = [('IF', 'if'), ('IDENTIFIER', 'hello'), ('ELSE', 'else'), ('STRING', 'yes')]

    input3 = '''123 // can see this
                "yes!"'''
    output3 = [('NUMBER', 123), ('STRING', 'yes!')]

    input4 = '''"hello" /* how are you*/ 123 /* are you ok*/'''
    output4 = [('STRING', 'hello'), ('NUMBER', 123)]
    assert test_lexer(input1) == output1
    assert test_lexer(input2) == output2
    assert test_lexer(input3) == output3
    assert test_lexer(input4) == output4


def test():
    test_single_token()
    test_number()
    test_string()
    test_identifier()
    test_comment()
    print("tests pass")

if __name__ == '__main__':
    test()



