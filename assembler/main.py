'''
Copyright 2013 Adrian Nackov
Released under BSD Licence (3 clause):
http://www.opensource.org/licenses/bsd-license.php
'''

import sys

from parser import parse
from symbols import get_symbols
from translator import make_machine_code


def fatal(error):
    print error
    sys.exit(1)

def prepare_machine_code(assembler_lines):
    symbols = get_symbols()
    parsed_lines = parse(assembler_lines)
    machine_code = make_machine_code(symbols, parsed_lines)
    return machine_code

def write_machine_code_file(machine_code, asm_file):
    mcode_filename = asm_file[:-4] + '.hck'
    with open(mcode_filename, 'w') as f:
        for line in machine_code:
            f.write(line + '\n')

def parse_args(args):
    class ParsedArgs(object):
        pass
    if len(args) != 2:
        fatal("Usage: ./main.py <file>.asm")
    asm_file = args[1]
    if not asm_file.endswith('.asm'):
        fatal('%s filename does not end with .asm' % asm_file)
    ParsedArgs.asm_file = asm_file
    return ParsedArgs

def main(args):
    args = parse_args(args)
    with open(args.asm_file, 'r') as f:
        assembler_lines = f.readlines()
    machine_code = prepare_machine_code(assembler_lines)
    write_machine_code_file(machine_code, args.asm_file)
    return 0

if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
