'''
Copyright 2013 Adrian Nackov
Released under BSD Licence (3 clause):
http://www.opensource.org/licenses/bsd-license.php
'''

import re


LABEL_SYMBOL_RE = re.compile(r'^\(\w+\)$')


class ParserError(Exception):
    '''A generic ParserError'''


def parse(assembler_lines, symbols):
    '''
    symbols (assembler.lib._Symbols instance)
    assembler lines (list of strings)

    returns: (list of dicts)
    '''
    assembler_lines = strip_lines(assembler_lines)

    # first pass: just collecting all label symbols and their ROM address.
    collect_label_symbols(symbols, assembler_lines)

    # second pass, actually parse the stuff.
    parsed_lines = []
    for line in assembler_lines:
        if line.startswith('@'):
            parsed_lines.append({
                'type': 'symbol_variable',
                'symbol': line,
            })
        elif line.startswith('('):
            # on the second pass label symbols are skipped
            # they don't result in machine code instructions
            continue
        else:
            parsed_lines.append(parse_instruction(line))

    return parsed_lines

def strip_lines(lines):
    '''
    Removes whitespace, \n, \t. Removes comment lines.
    lines (list of strings)

    returns: (list of strings)
    '''
    lines = map(strip, lines)
    return [line for line in lines if not is_comment(line)]

def is_comment(line):
    '''line (str)'''
    return bool(line.startswith('//'))

def collect_label_symbols(symbols, lines):
    '''
    symbols (assembler.lib._Symbols instance)
    assembler lines (list of strings)
    '''
    address_ROM = 0
    for line in lines:
        if re.match(LABEL_SYMBOL_RE, line):
            if symbols.contains(line):
                raise ParserError('Label symbol %s can be defined only once' %
                        line)
            symbols.add_label_variable(line, address_ROM)
        else:
            address_ROM += 1

def parse_instruction(line):
    '''
    line (str)

    returns: (dict)
        like ...
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
    return parsed

