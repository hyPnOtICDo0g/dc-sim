from sys import argv
from argparse import (ArgumentParser, ArgumentDefaultsHelpFormatter, Namespace)

class cmd:
    def parseArgs(self) -> Namespace:
        # global flags
        parser = ArgumentParser(description='Simulate data communication techniques.')
        parser.add_argument('-V', '--version', action='version', version='%(prog)s 1.0.1')
        subparsers = parser.add_subparsers(title='utilities', dest='subcommand')

        crc = subparsers.add_parser('crc', help='Simulate the CRC error detection technique.')
        crc.add_argument('-d', '--dataword', help='Data to be sent to the receiver.', metavar='WORD', required=True)
        crc.add_argument('-g', '--generator', help='Generator polynomial.', metavar='POLY', required=True)
        crc.add_argument('-i', '--bitinvert', help='Simulate a bit flip.', action='store_true')

        hamming = subparsers.add_parser('hamming', help='Calculate the Hamming Distance between two codewords.')
        hamming.add_argument('-c', '--codeword', help='Specify two codewords.', nargs=2, required=True)

        stopwait = subparsers.add_parser('stopwait', help='Simulate the Stop and Wait protocol.', formatter_class=ArgumentDefaultsHelpFormatter)
        stopwait.add_argument('-a', '--host', help='Specify an alternate bind address.', metavar='ADDRESS', default='127.0.0.1')
        stopwait.add_argument('-p', '--port', help='Specify an alternate port.', type=int, default='8000')
        stopwait.add_argument('-n', '--packets', help='Specify the number of packets to be created.', type=int, default='5')
        stopwait.add_argument('-m', '--mode', help='Switch between sender or receiver modes.', choices=['sender', 'receiver'], required=True)

        if(len(argv) == 1):
            parser.print_help()
            exit(1)

        return parser.parse_args()

args = cmd().parseArgs()
