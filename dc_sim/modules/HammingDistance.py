class HammingDistance:
    def calculate(self, C1: str, C2: str) -> int:
        try:
            # check if both codewords are of same length
            assert len(C1) == len(C2)
            # convert binary strings to their equivalent integers and XOR
            # the obtained integer is converted to it's binary equivalent
            # count the number of 1s and return
            return bin(int(C1, 2) ^ int(C2, 2)).count('1')
        except AssertionError:
            print('C1 and C2 are of unequal lengths.')
            exit(1)
