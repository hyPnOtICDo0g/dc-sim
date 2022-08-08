from random import randrange

class CyclicRedundancyCheck:
    def __init__(self, dataword: str, generator: str) -> None:
        self.dataword = dataword
        self.generator = generator.lstrip('0')
        self.crc = 0
        self.remainder = 0

    def EncodeDecode(self, mode: str) -> str:
        GeneratorLen = len(self.generator)
        DatawordLen = len(self.dataword)
        # append 0s or crc depending on the mode
        PaddedArray = list(self.dataword + ('0'*(GeneratorLen - 1) if mode == 'e' else self.crc))
        # shift until there are no 1s in the list
        while '1' in PaddedArray[:DatawordLen]:
            # get the index of the first occurrence of 1
            ShiftIndex = PaddedArray.index('1')
            for i in range(GeneratorLen):
                PaddedArray[ShiftIndex + i] = str(int(self.generator[i] != PaddedArray[ShiftIndex + i]))
        # obtain crc string
        crc = ''.join(PaddedArray)[DatawordLen:]
        return crc if mode == 'e' else str('1' not in crc)

    def PrintData(self, person: str) -> None:
        print(
            f'\n{person} Side:\n'
            f'Dataword: {self.dataword} | Generator: {self.generator}\n'
            f'CRC: {self.crc} | Codeword: {self.dataword + self.crc}'
        )

    def send(self) -> None:
        self.crc = self.EncodeDecode('e')
        self.PrintData('Sender')

    def receive(self) -> None:
        self.remainder = self.EncodeDecode('d')
        self.PrintData('Receiver')

    def BitInvert(self, action: bool) -> None:
        if action:
            rand = randrange(len(self.dataword) - 1)
            self.dataword = self.dataword[:rand] + str(int(self.dataword[rand]) ^ 1) + self.dataword[rand + 1:]

    def check(self) -> None:
        try:
            assert self.remainder == 'True'
            print('\nNo Error Detected.\n')
        except:
            print('\nError, Bit Inversion Detected.\n')
