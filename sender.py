from socket import *

# imports all functions inside util.py
from util import *


class Sender:

    SERVER_ADDRESS_PORT = ("127.0.0.1", 10373)

    SOCKET_TIMEOUT_SECONDS = 4

    BUFFER_SIZE = 1024

    # Total number of packets that are sent to the receiver.
    totalPacketCount = 0

    seq_number = 0
    ack_number = 0


    def __init__(self):
        """ 
        Your constructor should not expect any argument passed in,
        as an object will be initialized as follows:
        sender = Sender()
        
        Please check the main.py for a reference of how your function will be called.
        """


    def rdt_send(self, app_msg_str):
        """reliably send a message to the receiver (MUST-HAVE DO-NOT-CHANGE)

        Args:
        app_msg_str: the message string (to be put in the data field of the packet)

        """
        
        print('original message string: {}'.format(app_msg_str))

        sndpkt = make_packet(app_msg_str, self.ack_number, self.seq_number)
        print('packet is created: {}'.format(sndpkt))

        udpClientSocket = socket(family=AF_INET, type=SOCK_DGRAM)
        self.udp_send(udpClientSocket, sndpkt)

        while True:
            recpkt = b''
            udpClientSocket.settimeout(self.SOCKET_TIMEOUT_SECONDS)
            try:
                recpkt, _ = udpClientSocket.recvfrom(self.BUFFER_SIZE)
            except:
                print('socket timeout! Resend!')
                print('\n[timeout retransmission]: {}'.format(app_msg_str))
                self.udp_send(udpClientSocket, sndpkt)
                recpkt, _ = udpClientSocket.recvfrom(self.BUFFER_SIZE)

            if extract_ack_number(recpkt) != self.seq_number or verify_checksum(recpkt) == False:
                print('receiver acked the previous pkt, resend!\n')
                print('[ACK-Previous retransmission]: {}'.format(app_msg_str))
                self.udp_send(udpClientSocket, sndpkt)
                recpkt, _ = udpClientSocket.recvfrom(self.BUFFER_SIZE)

            print('packet is received correctly: seq. num {} = ACK num {}. all done!\n'.format(extract_seq_number(recpkt), extract_ack_number(recpkt)))
            self.seq_number = 1 if self.seq_number == 0 else 0
            break

        udpClientSocket.close()


    def udp_send(self, udpClienSocket, sndpkt):
        udpClienSocket.sendto(sndpkt, self.SERVER_ADDRESS_PORT)
        self.totalPacketCount += 1
        print('packet num.{} is successfully sent to the receiver.'.format(self.totalPacketCount))



  ####### Your Sender class in sender.py MUST have the rdt_send(app_msg_str)  #######
  ####### function, which will be called by an application to                 #######
  ####### send a message. DO NOT change the function name.                    #######
  ####### You can have other functions if needed.                             #######