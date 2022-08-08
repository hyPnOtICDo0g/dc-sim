from .cli import args
from time import sleep
from json import (dumps, loads)
from string import ascii_uppercase
from random import (uniform, choices)
from .constants import (SharedConstants, Colors)
from socket import (socket, timeout, AF_INET, SOCK_STREAM)

class StopAndWait:
    def __init__(self) -> None:
        self.address = f'{args.host}:{args.port}'
        self.bind = (args.host, args.port)

    def EncodePacket(self, packet: dict) -> bytes:
        # dict -> str -> bytes
        return dumps(packet).encode('utf-8')

    def DecodePacket(self, packet: bytes) -> dict:
        # loads() raises ValueError when it's forcefully interrupted
        # usually it is a keyboard interrupt or CTRL + C
        try:
            # bytes -> str -> dict
            return loads(packet.decode('utf-8'))
        except ValueError:
            # therefore we catch it and raise a KeyboardInterrupt to exit cleanly
            raise KeyboardInterrupt

    def GeneratePackets(self) -> list:
        # return a list of encoded packets
        return [self.EncodePacket(
            {
                # acknowledgment
                'ack': False,
                # sequence number
                'seq_num': x,
                # generate a random string of 5 uppercase letters
                'data': ''.join(choices(ascii_uppercase, k = 5))
            }
        ) for x in range(1, args.packets + 1)]


    def receiver(self) -> None:
        try:
            with socket(AF_INET, SOCK_STREAM) as sock:
                sock.bind(self.bind)
                sock.listen(1)
                print(f'> {Colors.OKCYAN}[listening on socket] {self.address}{Colors.ENDC}')
                conn = sock.accept()[0]
                with conn:
                    print(f'> {Colors.OKGREEN}sender connected.{Colors.ENDC}')
                    self.SimulateACK(conn)
        except OSError:
            print(f'{Colors.FAILRED}a receiver is already listening on {self.address}.{Colors.ENDC}')

    def sender(self) -> None:
        try:
            with socket(AF_INET, SOCK_STREAM) as sock:
                sock.connect(self.bind)
                print(f'> {Colors.OKCYAN}[connected to receiver] listening on {self.address}{Colors.ENDC}')
                # set the propagation time as the socket timeout
                sock.settimeout(SharedConstants.PROPAGATION_TIME)
                self.SimulatePacketLoss(sock)
                print(f'> {Colors.OKCYAN}disconnected from receiver{Colors.ENDC}')
        except ConnectionRefusedError:
            print(f'{Colors.FAILRED}receiver listening on {self.address} not found.{Colors.ENDC}')

    def SimulatePacketLoss(self, conn) -> None:
        PacketCount = 0
        # iterate through generated packets
        for packet in self.GeneratePackets():
            # resets at every iteration
            PacketCount += 1
            TimeoutTrialCount = SharedConstants.SENDER_TIMEOUT_TRIALS
            while TimeoutTrialCount:
                    try:
                        # send the packet
                        conn.sendall(packet)
                        print(f'> {Colors.OKBLUE}packet {PacketCount} sent, waiting for ACK{Colors.ENDC}')
                        # wait for response or timeout
                        res = conn.recv(SharedConstants.PACKET_SIZE)
                        # decode the packet if we get a response
                        DecodedPacket = self.DecodePacket(res)
                        # check if we recieved an ack
                        if DecodedPacket['ack'] == True:
                            print(f'> {Colors.OKGREEN}ACK received, packet {PacketCount} successfully transmitted{Colors.ENDC}')
                            break
                    except timeout:
                        print(f'> {Colors.WARNINGYELLOW}timeout: no ACK received, re-transmitting packet {PacketCount}{Colors.ENDC}')
                        TimeoutTrialCount -= 1
                        continue
            # disconnect if we run out of trials
            if not TimeoutTrialCount:
                print(f'> {Colors.FAILRED}transmission failed after {SharedConstants.SENDER_TIMEOUT_TRIALS} attempts, disconnecting now.{Colors.ENDC}')
                exit(1)

    def SimulateACK(self, conn) -> None:
        # infinitely accept packets
        while True:
            packet = conn.recv(SharedConstants.PACKET_SIZE)
            # if there are no more packets to send, we receive 0 bytes, therefore disconnect
            if not packet:
                print(f'> {Colors.OKCYAN}disconnected from sender{Colors.ENDC}')
                return
            # else decode the packet
            DecodedPacket = self.DecodePacket(packet)
            # if a random number < acknowledgement probability then send the ack
            if uniform(0, 1) < SharedConstants.ACKNOWLEDGEMENT_PROBABILITY:
                DecodedPacket['ack'] = True
                conn.sendall(self.EncodePacket(DecodedPacket))
                print(f'> {Colors.OKGREEN}packet {DecodedPacket["seq_num"]} received successfully, ACK sent{Colors.ENDC}')
                print(f'> {Colors.HEADER}decoded data in packet {DecodedPacket["seq_num"]}: {DecodedPacket["data"]}{Colors.ENDC}')
            else:
                # else drop the packet and sleep
                print(f'> {Colors.FAILRED}packet {DecodedPacket["seq_num"]} errored out, silently dropped{Colors.ENDC}')
                sleep(SharedConstants.PROPAGATION_TIME)
