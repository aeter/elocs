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
    '0' : [0, 1, 0, 1, 0, 1, 0],
    '1' : [0, 1, 1, 1, 1, 1, 1],
    '-1': [0, 1, 1, 1, 0, 1, 0],
    'D': [0, 0, 0, 1, 1, 0, 0],
    'A': [0, 1, 1, 0, 0, 0, 0],
    '!D': [0, 0, 0, 1, 1, 0, 1],
    '!A': [0, 1, 1, 0, 0, 0, 1],
    '-D': [0, 0, 0, 1, 1, 1, 1],
    '-A': [0, 1, 1, 0, 0, 1, 1],
    'D+1': [0, 0, 1, 1, 1, 1, 1],
    'A+1': [0, 1, 1, 0, 1, 1, 1],
    'D-1': [0, 0, 0, 1, 1, 1, 0],
    'A-1': [0, 1, 1, 0, 0, 1, 0],
    'D+A': [0, 0, 0, 0, 0, 1, 0],
    'D-A': [0, 0, 1, 0, 0, 1, 1],
    'A-D': [0, 0, 0, 0, 1, 1, 1],
    'D&A': [0, 0, 0, 0, 0, 0, 0],
    'D|A': [0, 0, 1, 0, 1, 0, 1],
    'M': [1, 1, 1, 0, 0, 0, 0],
    '!M': [1, 1, 1, 0, 0, 0, 1],
    '-M': [1, 1, 1, 0, 0, 1, 1],
    'M+1': [1, 1, 1, 0, 1, 1, 1],
    'M-1': [1, 1, 1, 0, 0, 1, 0],
    'D+M': [1, 0, 0, 0, 0, 1, 0],
    'D-M': [1, 0, 1, 0, 0, 1, 1],
    'M-D': [1, 0, 0, 0, 1, 1, 1],
    'D&M': [1, 0, 0, 0, 0, 0, 0],
    'D|M': [1, 0, 1, 0, 1, 0, 1],
}


class TranslatorError(Exception):
    '''A generic TranslatorError'''


def make_machine_code(symbols, parsed_lines):
    '''
    symbols (assembler.symbols._Symbols instance)
    parsed_lines (list of dicts)

    returns: (list of strings)
        like ['000000000001000', '0000110001010000', ...]
    '''
    # first pass: just collecting all label symbols and their ROM address.
    collect_label_variables(symbols, parsed_lines)

    # second pass, translate each translatable assembler line to machine code
    translated = []
    for line in lines:
        if line['type'] in ('comment', 'label_variable',):
            continue
        elif line['type'] == 'symbol_variable':
            if symbols.contains(line['symbol']):
                translated.append(to_binary(
                    symbols.get_address(line['symbol'])))
            else: # new variable?
                symbols.allocate(line['symbol'])
                translated.append(to_binary(
                    symbols.get_address(line['symbol'])))
        elif line['type'] == 'instruction':
            instruction = [1, 1, 1]
            instruction += COMPS[line['comp']]
            instruction += DESTS[line['dest']]
            instruction += JUMPS[line['jump']]
            translated.append(''.join(instruction))
    return translated

def to_binary(num):
    binary_num = bin(num)[2:] # bin(4) = '0b100', this strips 0b
    # add needed zeros, the instruction should be
    # 16 characters long, like 0000 0001 0011 0101
    return '0' * (16 - len(binary_num)) + binary_num

def collect_label_variables(symbols, lines):
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
            symbols.allocate(line['symbol'], address_ROM)
        else:
            address_ROM += 1

