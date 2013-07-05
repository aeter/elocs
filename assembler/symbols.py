'''
Copyright 2013 Adrian Nackov
Released under BSD Licence (3 clause):
http://www.opensource.org/licenses/bsd-license.php
'''

_SYMBOLS = None


def get_symbols():
    '''A singleton for the _Symbols class'''
    global _SYMBOLS
    if _SYMBOLS is None:
        _SYMBOLS = _Symbols()
    return _SYMBOLS


class _Symbols(object):
    SYMBOLS = {}
    # By specification, first defined variable gets this address. 
    LAST_ALLOCATED_ADDRESS = 16

    def __init__(self):
        self.SYMBOLS.update({
            "SP": 0,
            "LCL": 1,
            "ARG": 2,
            "THIS": 3,
            "THAT": 4,  
            "SCREEN": 16384,
            "KBD": 24576,
        })
        for num in range(15):
            self.SYMBOLS["R%s" % num] = num

    def _strip_variable_declarations(self, name):
        # strip variable declarators like "(name)" or "@name"
        if name.startswith('(') and name.endswith(')'):
            return name[1:-1]
        elif name.startswith('@'):
            return name[1:]

    def add_symbol_variable(self, name):
        '''
        name (str)
            like '@i'
        '''
        name = self._strip_variable_declarations(name)
        # each new @variable gets allocated a consecutive memory address
        self.SYMBOLS[name] = self.LAST_ALLOCATED_ADDRESS
        self.LAST_ALLOCATED_ADDRESS += 1

    def add_label_variable(self, name, address):
        '''
        name (str)
            like '(end)' or '(loop)', etc.
        address (int)
        '''
        name = self._strip_variable_declarations(name)
        self.SYMBOLS[name] = address

    def contains(self, name):
        name = self._strip_variable_declarations(name)
        return bool(name in self.SYMBOLS)
