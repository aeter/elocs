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
        line, comment = parse_comment(line)
        parsed = {'comment': comment}

        if not line: # the whole line is one comment, starting with '//'
            parsed.update({'type': 'comment'})
        elif is_symbol_variable(line):
            parsed.update({'type': 'symbol_variable', 'symbol': line,})
        elif is_label_variable(line):
            parsed.update({'type': 'label_variable', 'symbol': line,})
        else: # an instruction?
            try:
                parsed.update(parse_instruction(line))
            except ValueError:
                raise ParserError('Invalid assembler: %s' % line)
        parsed_lines.append(parsed)
    return parsed_lines

def parse_comment(line):
    try:
        line, comment = line.split('//', 1)
    except ValueError:
        comment = None
    return line, comment

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
    parsed = {
        'type': 'instruction',
        'dest': 'null',
        'jump': 'null',
    }
    if '=' in line:
        dest, line = line.split('=')
        parsed.update({'dest': dest.strip()})
    if ';' in line:
        comp, jump = line.split(';')
        parsed.update({'comp': comp.strip(), 'jump': jump.strip()})
    else:
        parsed.update({'comp': line.strip()})
    return parsed
