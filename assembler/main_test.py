import os
import tempfile
import unittest

from main import prepare_machine_code


ASSEMBLER_CODE_SUM_HUNDRED = """// Adds 1 + ... + 100
    @i
    M=1   // i = 1
    @sum
    M=0   // sum=0
(LOOP)
    @i
    D=M // D=i
    @100
    D=D-A //D=i-100
    @END
    D;JGT // if (i - 100) > 0 goto END
    @i
    D=M // D=i
    @sum
    M=D+M // sum=sum+i
    @i
    M=M+1 // i=i+1
    @LOOP
    0;JMP // goto LOOP
(END)
    @END
    0;JMP //infinite loop, exits program."""

def remove_whitespaces(text):
    return ''.join(text.split())
MACHINE_CODE_SUM_HUNDRED = remove_whitespaces(
"""0000 0000 0001 0000
1110 1111 1100 1000
0000 0000 0001 0001
1110 1010 1000 1000
0000 0000 0001 0000
1111 1100 0001 0000
0000 0000 0110 0100
1110 0100 1101 0000
0000 0000 0001 0010
1110 0011 0000 0001
0000 0000 0001 0000
1111 1100 0001 0000
0000 0000 0001 0001
1111 0000 1000 1000
0000 0000 0001 0000
1111 1101 1100 1000
0000 0000 0000 0100
1110 1010 1000 0111
0000 0000 0001 0010
1110 1010 1000 0111""")


class TestMain(unittest.TestCase):
    '''
    An integration test of several modules.
    '''
    def test_translating_to_machine_code(self):
        result = prepare_machine_code(ASSEMBLER_CODE_SUM_HUNDRED)
        expected_result = MACHINE_CODE_SUM_HUNDRED
        self.assertEqual(result, expected_result)


if __name__ == '__main__':
    unittest.main()
