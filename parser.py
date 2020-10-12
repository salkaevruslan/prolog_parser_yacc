import os, sys, glob

import ply.yacc as yacc 

from lex import tokens 


def p_program(p):
  '''program : relation
             | program relation'''
  if len(p) == 2:
    p[0] = p[1]
  elif len(p) == 3:
    p[0] = p[1] + '\n' + p[2]



def p_relation(p):
  '''relation : atom DOT
              | atom CORK disjunction DOT'''
  if len(p) == 3:
    p[0] = 'relation\n' + add_tab('head\n' + add_tab(p[1]))
  elif len(p) == 5:
    p[0] = 'relation\n' + add_tab('head\n' + add_tab(p[1]) + '\n'+ 'body\n' + add_tab(p[3]))



def p_atom(p):
  '''atom : ID
          | ID atom_end'''
  if len(p) == 2:
    p[0] = 'identifier = ' + p[1]
  elif len(p) == 3:
    p[0] = 'atom\n' + add_tab('identifier = ' + p[1] + '\n' + p[2])


def p_bracket_atom(p):
  '''bracket_atom : LEFTBRACKET bracket_atom RIGHTBRACKET
                  | ID
                  | ID atom_end'''
  if len(p) == 2:
    p[0] = 'identifier = ' + p[1]
  elif len(p) ==3:
    p[0] = 'identifier = ' + p[1] + '\n' + p[2]
  elif len(p) == 4:
    p[0] = 'atom\n' + add_tab(p[2])


def p_atom_end(p):
  '''atom_end : ID
              | ID atom_end
              | LEFTBRACKET bracket_atom RIGHTBRACKET
              | LEFTBRACKET bracket_atom RIGHTBRACKET atom_end'''
  if len(p) == 2:
    p[0] = 'identifier = ' + p[1]
  elif len(p) ==3:
    p[0] = 'identifier = ' + p[1] + '\n' + p[2]
  elif len(p) == 4:
    p[0] = 'atom\n' + add_tab(p[2])
  elif len(p) == 5:
    p[0] = 'atom\n' + add_tab(p[2]) + p[4]


def p_disjunction(p):
  '''disjunction : conjunction OR disjunction
                 | conjunction'''
  if len(p) == 4:
    p[0] = 'disjunction\n' + add_tab(p[1] + '\n' + p[3])
  elif len(p) == 2:
    p[0] = p[1] 



def p_conjunction(p):
  '''conjunction : element AND conjunction
                 | element'''
  if len(p) == 4:
    p[0] = 'conjunction\n' + add_tab(p[1] + '\n' + p[3])
  elif len(p) == 2:
    p[0] = p[1]



def p_element(p):
  '''element : LEFTBRACKET disjunction RIGHTBRACKET
             | atom'''
  if len(p) == 4:
    p[0] = p[2]
  elif len(p) == 2:
    p[0] = p[1]



def p_error(p): 
  if p == None:
    raise SyntaxError("Missing dot at the end")
  else:
    raise SyntaxError("Illegal character: line", p.lineno, 'col', p.lexpos)

def add_tab(str):
   return '\t'+ '\t'.join(str.splitlines(True))

parser = yacc.yacc()

if sys.argv[1] == 'tests':
  current_dir = os.path.dirname(os.path.abspath(__file__))
  result = True
  for filename in glob.glob(current_dir + '/tests/correct*.txt'):
    file = open(filename, 'r')
    output_file = open(filename + '.out', 'r')
    inputtext = file.read().strip('\n')
    correcttext = output_file.read().strip('\n')
    if correcttext.replace("\n", " ") != parser.parse(inputtext).replace("\n", " "):
      print('Test \'{0}\' failed'.format(os.path.basename(filename)))
      result = False
  for filename in glob.glob(current_dir + '/tests/incorrect*.txt'):
    file = open(filename, 'r')
    inputtext = file.read().strip('\n')
    try:
      parser.parse(inputtext)
      print('Test \'{0}\' failed'.format(os.path.basename(filename)))
      result = False
    except SyntaxError:
      pass
  if result:
    print('Tests passed')
  else:
    print('Tests failed')
else:
  sys.stdout = open(sys.argv[1] + '.out', 'w')
  with open(sys.argv[1], 'r') as inputfile:
    try:
      result = parser.parse(inputfile.read())
      print(result)
    except SyntaxError:
      sys.stdout = sys.__stdout__
      type, value, traceback = sys.exc_info()
      print(value)

