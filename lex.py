import ply.lex as lex 
import sys

tokens = [
  'ID',
  'CORK',
  'AND',
  'OR',
  'LEFTBRACKET',
  'RIGHTBRACKET',
  'DOT'
]

t_ID= r'[a-zA-Z_][a-zA-Z_0-9]*'
t_CORK = r':-'
t_AND = ','
t_OR = ';'
t_LEFTBRACKET = '\('
t_RIGHTBRACKET = '\)'
t_DOT = '\.'

t_ignore = ' \t'

def t_newline(t): 
  r'\n+'
  t.lexer.lineno += len(t.value)

def t_error(t): 
  raise SyntaxError

lexer = lex.lex() 