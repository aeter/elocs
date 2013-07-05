'''
Copyright 2013 Adrian Nackov
Released under BSD Licence (3 clause):
http://www.opensource.org/licenses/bsd-license.php
'''

import sys

from parser import parse
from symbols import get_symbols


def fatal(error):
    print error
    sys.exit(1)

def main(args):
    if len(args) != 2:
        fatal("Usage: ./main.py <file>.asm")
    asm_file = args[1]
    symbols = get_symbols()
    with open(asm_file, 'r') as f:
        assembler_lines = f.readlines()
    parsed_lines = parse(assembler_lines, symbols)
    # TODO - translate parsed lines into machine code
    # TODO - write the machine code in a file.
    return 0

if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
