from .cli import args
from .StopAndWait import StopAndWait
from .CRC import CyclicRedundancyCheck
from .HammingDistance import HammingDistance

class dc_sim:
    def main(self) -> None:
        try:
            if(args.subcommand == 'crc'):
                # check if C1 and C2 are binary strings
                int(args.dataword, 2) and int(args.generator, 2)
                app = CyclicRedundancyCheck(args.dataword, args.generator)
                app.send()
                app.BitInvert(args.bitinvert)
                app.receive()
                app.check()

            elif(args.subcommand == 'hamming'):
                app = HammingDistance()
                dist = app.calculate(args.codeword[0], args.codeword[1])
                print('Hamming Distance:', dist)

            else:
                app = StopAndWait()
                getattr(app, args.mode)()

        except ValueError:
            print('Enter binary numbers only.')

        except KeyboardInterrupt:
            print('\nKeyboard interrupt received, exiting.')
            exit(1)

def main() -> None:
    try:
        app = dc_sim()
        app.main()
    except Exception as e:
        print(f'[ERROR] - {e}')
