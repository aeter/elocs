import unittest

from symbols import get_symbols


class SymbolsTest(unittest.TestCase):

    def test_symbols_initialization(self):
        symbols = get_symbols()
        self.assertTrue(symbols.contains('R15'))
        self.assertEqual(symbols.get_address('R15'), 15)

if __name__ == '__main__':
    unittest.main()
