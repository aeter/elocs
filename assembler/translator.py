'''
Copyright 2013 Adrian Nackov
Released under BSD Licence (3 clause):
http://www.opensource.org/licenses/bsd-license.php
'''

# DESTS, JUMPS, COMPS tables regarding how exactly 
# the machine code is made out of assembler instructions
DESTS = {
    'null': [0, 0, 0],
    'M': [0, 0, 1],
    'D': [0, 1, 0],
    'MD': [0, 1, 1],
    'A': [1, 0, 0],
    'AM': [1, 0, 1],
    'AD': [1, 1, 0],
    'AMD': [1, 1, 1],
}

JUMPS = {
    'null': [0, 0, 0],
    'JGT': [0, 0, 1],
    'JEQ': [0, 1, 0],
    'JGE': [0, 1, 1],
    'JLT': [1, 0, 0],
    'JNE': [1, 0, 1],
    'JLE': [1, 1, 0],
    'JMP': [1, 1, 1],
}

COMPS = {
    
}


class TranslatorError(Exception):
    '''A generic TranslatorError'''


def make_machine_code(symbols, parsed_lines):
    '''
    parsed_lines (list of dicts)
    symbols (assembler.symbols._Symbols instance)
    '''
    # first pass: just collecting all label symbols and their ROM address.
    collect_label_symbols(symbols, parsed_lines)

    # second pass
    translated = []
    for line in lines:
        if line['type'] in ('comment', 'label_variable',):
            continue
        # TODO

def collect_label_symbols(symbols, lines):
    '''
    symbols (assembler.symbols._Symbols instance)
    lines (list of dicts)
    '''
    address_ROM = 0
    for line in lines:
        if line['type'] == 'label_variable':
            if symbols.contains(line['symbol']):
                raise TranslatorError('Label %s can be defined only once' %
                        line['symbol'])
            symbols.add_label_variable(line['symbol'], address_ROM)
        else:
            address_ROM += 1

