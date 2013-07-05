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
        for num in range(16):
            self.SYMBOLS["R%s" % num] = num

    def _cleanup(self, name):
        # strip "(name)" or "@name" to "name"
        if name.startswith('(') and name.endswith(')'):
            return name[1:-1]
        elif name.startswith('@'):
            return name[1:]
        else:
            return name

    def allocate(self, name, address=None):
        '''
        name (str)
            like '@i' or '(loop)' or '(end)', etc.
        address (int)
        '''
        name = self._cleanup(name)
        if address is None:
            # each new @variable gets allocated a consecutive memory address
            self.SYMBOLS[name] = self.LAST_ALLOCATED_ADDRESS
            self.LAST_ALLOCATED_ADDRESS += 1
        else:
            # the '(word)' variables are allocated at specific ROM address 
            self.SYMBOLS[name] = address

    def contains(self, name):
        '''name (str)'''
        name = self._cleanup(name)
        return bool(name in self.SYMBOLS)

    def get_address(self, name):
        '''name (str)'''
        name = self._cleanup(name)
        return self.SYMBOLS[name]
