import ply.lex as lex
import ply.yacc as yacc
import myJsLexer
import myJsParser


jslexer = lex.lex(module=myJsLexer)
jsparser = yacc.yacc(debug=0, write_tables=0, module=myJsParser)


def test_parser(input_string):
    jslexer.input(input_string)
    ast = jsparser.parse(input_string, lexer=jslexer)
    return ast


def test_expression():
    assert test_parser('x;') == [('stmt', ('exp', ('identifier', 'x')))]                        # test identifier
    assert test_parser('1;') == [('stmt', ('exp', ('number', 1)))]                              # test number
    assert test_parser('"hello world!";') == [('stmt', ('exp', ('string', 'hello world!')))]    # test string

    assert test_parser('true;') == [('stmt', ('exp', ('true', 'true')))]                        # test true
    assert test_parser('false;') == [('stmt', ('exp', ('false', 'false')))]                     # test false
    assert test_parser('! true;') == [('stmt', ('exp', ('not', ('true', 'true'))))]             # test not
    assert test_parser('! 1;') == [('stmt', ('exp', ('not', ('number', 1))))]

    # test operations
    assert test_parser('1>2;') == [('stmt', ('exp', ('binop', ('number', 1), '>', ('number', 2))))]
    assert test_parser('1<2;') == [('stmt', ('exp', ('binop', ('number', 1), '<', ('number', 2))))]
    assert test_parser('1>=2;') == [('stmt', ('exp', ('binop', ('number', 1), '>=', ('number', 2))))]
    assert test_parser('1<=2;') == [('stmt', ('exp', ('binop', ('number', 1), '<=', ('number', 2))))]
    assert test_parser('1==2;') == [('stmt', ('exp', ('binop', ('number', 1), '==', ('number', 2))))]
    assert test_parser('1!=2;') == [('stmt', ('exp', ('binop', ('number', 1), '!=', ('number', 2))))]
    assert test_parser('1&&2;') == [('stmt', ('exp', ('binop', ('number', 1), '&&', ('number', 2))))]
    assert test_parser('1||2;') == [('stmt', ('exp', ('binop', ('number', 1), '||', ('number', 2))))]

    # Test precedence
    assert test_parser('1+2*3;') == [('stmt', ('exp', ('binop', ('number', 1), '+',
                                                       ('binop', ('number', 2), '*', ('number', 3)))))]
    assert test_parser('1*2+3;') == [('stmt', ('exp', ('binop',
                                                       ('binop', ('number', 1), '*', ('number', 2)),
                                                       '+', ('number', 3))))]
    assert test_parser('1-2+3;') == [('stmt', ('exp', ('binop',
                                                       ('binop', ('number', 1), '-', ('number', 2)),
                                                       '+', ('number', 3))))]
    assert test_parser('1+2>3;') == [('stmt', ('exp', ('binop', ('binop', ('number', 1), '+', ('number', 2)),
                                                       '>', ('number', 3))))]

    # test expression with parentheses
    assert test_parser('(2+3);') == [('stmt', ('exp', ('binop', ('number', 2), '+', ('number', 3))))]
    assert test_parser('("str");') == [('stmt', ('exp', ('string', 'str')))]
    assert test_parser('(id);') == [('stmt', ('exp', ('identifier', 'id')))]

    # test call function
    assert test_parser('fun();') == [('stmt', ('exp', ('call', 'fun', [])))]
    assert test_parser('fun(x);') == [('stmt', ('exp', ('call', 'fun', [('identifier', 'x')])))]
    assert test_parser('fun(1);') == [('stmt', ('exp', ('call', 'fun', [('number', 1)])))]
    assert test_parser('fun("hi");') == [('stmt', ('exp', ('call', 'fun', [('string', 'hi')])))]
    assert test_parser('fun(1,2);') == [('stmt', ('exp', ('call', 'fun', [('number', 1), ('number', 2)])))]
    assert test_parser('fun(1,"y");') == [('stmt', ('exp', ('call', 'fun', [('number', 1), ('string', 'y')])))]
    assert test_parser('fun(x,1);') == [('stmt', ('exp', ('call', 'fun', [('identifier', 'x'), ('number', 1)])))]


def test_stmt():
    # Because expression has been tested before
    # So Here I just choose a few situation to test the correctness in grammar

    # test if and if-else
    assert test_parser('if (true) {1;}') == [('stmt', ('if-then', ('true', 'true'),
                                                       [('stmt', ('exp', ('number', 1)))]))]
    assert test_parser('if (false) {"no";} else {"yes";}') == [('stmt', ('if-then-else', ('false', 'false'),
                                                                         [('stmt', ('exp', ('string', 'no')))],
                                                                         [('stmt', ('exp', ('string', 'yes')))]))]
    # test assign
    assert test_parser('id = "id";') == [('stmt', ('assign', 'id', ('string', 'id')))]
    assert test_parser('id = 3;') == [('stmt', ('assign', 'id', ('number', 3)))]
    assert test_parser('id = 3*4;') == [('stmt', ('assign', 'id', ('binop', ('number', 3), '*', ('number', 4))))]
    assert test_parser('id = -3;') == [('stmt', ('assign', 'id', ('negative', ('number', 3))))]
    assert test_parser('id = -(2+3);') == [('stmt', ('assign', 'id', ('negative', ('binop', ('number', 2),
                                                                                   '+', ('number', 3)))))]
    assert test_parser('id = -another;') == [('stmt', ('assign', 'id', ('negative', ('identifier', 'another'))))]

    # test return
    assert test_parser('return 0;') == [('stmt', ('return', ('number', 0)))]
    assert test_parser('return 1+2;') == [('stmt', ('return', ('binop', ('number', 1), '+', ('number', 2))))]
    assert test_parser('return id;') == [('stmt', ('return', ('identifier', 'id')))]

    # test variable declaration
    assert test_parser('var id = 1;') == [('stmt', ('var', 'id', ('number', 1)))]
    assert test_parser('var id = -1;') == [('stmt', ('var', 'id', ('negative', ('number', 1))))]


def test_topStmt_func():
    assert test_parser('function fun() {"yes";}') == [('function', 'fun', [], [('stmt', ('exp', ('string', 'yes')))])]
    assert test_parser('function fun() {"yes";2;}') == [('function', 'fun', [],
                                                        [('stmt', ('exp', ('string', 'yes'))),
                                                         ('stmt', ('exp', ('number', 2)))])]
    assert test_parser('function fun(x) {return 2;}') == [('function', 'fun', ['x'],
                                                           [('stmt', ('return', ('number', 2)))])]
    assert test_parser('function fun(x,y) {return x;}') == [('function', 'fun', ['x', 'y'],
                                                             [('stmt', ('return', ('identifier', 'x')))])]

    # test anonymous function
    assert test_parser('function() {return 1;}') == [('lambda', [], [('stmt', ('return', ('number', 1)))])]
    assert test_parser('function(x) {return x;}') == [('lambda', ['x'], [('stmt', ('return', ('identifier', 'x')))])]
    assert test_parser('function(x,y) {return "y";}') == [('lambda', ['x', 'y'], [('stmt', ('return',
                                                                                            ('string', 'y')))])]


def test_topStmts():
    assert test_parser('var x = 1; x = 1 + 2;') == [('stmt', ('var', 'x', ('number', 1))),
                                                    ('stmt', ('assign', 'x', ('binop', ('number', 1), '+',
                                                                              ('number', 2))))]
    assert test_parser('1+2;1-2;') == [('stmt', ('exp', ('binop', ('number', 1), '+', ('number', 2)))),
                                       ('stmt', ('exp', ('binop', ('number', 1), '-', ('number', 2))))]
    assert test_parser('function f(){1;} var x = 1;return x;') == [('function', 'f', [], [('stmt', ('exp',
                                                                                                    ('number', 1)))]),
                                                                   ('stmt', ('var', 'x', ('number', 1))),
                                                                   ('stmt', ('return', ('identifier', 'x')))]
    assert test_parser('var x = 1; function f(){}') == [('stmt', ('var', 'x', ('number', 1))),
                                                        ('function', 'f', [], [])]


def test():
    test_expression()
    test_stmt()
    test_topStmt_func()
    test_topStmts()
    print('tests pass')


if __name__ == '__main__':
    test()