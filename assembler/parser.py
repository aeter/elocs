'''
Copyright 2013 Adrian Nackov
Released under BSD Licence (3 clause):
http://www.opensource.org/licenses/bsd-license.php
'''

import re

LABEL_VARIABLE_RE = re.compile(r'^\(\w+\)$')


class ParserError(Exception):
    '''A generic ParserError'''


def parse(assembler_lines):
    '''
    assembler lines (list of strings)

    returns: (list of dicts)
    '''
    parsed_lines = []
    for line in assembler_lines:
        line = line.strip()
        if is_comment(line):
            parsed_lines.append({
                'type': 'comment',
                'symbol': line,
            })
        elif is_symbol_variable(line):
            parsed_lines.append({
                'type': 'symbol_variable',
                'symbol': line,
            })
        elif is_label_variable(line):
            parsed_lines.append({
                'type': 'label_variable',
                'symbol': line,
            })
        else: # an instruction?
            try:
                parsed_lines.append(parse_instruction(line))
            except ValueError:
                raise ParserError('Invalid assembler: %s' % line)
    return parsed_lines

def is_comment(line):
    '''line (str)'''
    return bool(line.startswith('//'))

def is_label_variable(line):
    '''line (str)'''
    return bool(re.match(LABEL_VARIABLE_RE, line))

def is_symbol_variable(line):
    '''line(str)'''
    return bool(line.startswith('@'))

def parse_instruction(line):
    '''
    line (str)

    returns: (dict)
    '''
    # an instruction is like any of:
    # ['dest=comp;jump', 'comp;jump', 'dest=comp']
    parsed = {'type': 'instruction'}
    if '=' in line:
        dest, line = line.split('=')
        parsed.update({'dest': dest})
    if ';' in line:
        comp, jump = line.split(';')
        parsed.update({'comp': comp, 'jump': jump})
    else:
        parsed.update({'comp': line})

    # fill defaults of 'null' for jump and dest
    if not 'dest' in parsed:
        parsed['dest'] = 'null'
    if not 'jump' in parsed:
        parsed['jump'] = 'null'
    return parsed

