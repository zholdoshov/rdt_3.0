from socket import *
from time import sleep

# imports all functions inside util.py
from util import *

## No other imports allowed
localIP = "127.0.0.1"
localPort = 10373
packetNumber = 1
BUFFER_SIZE = 1024
SLEEP_TIME_SECONDS = 5.0


# Creates a datagram socket
UDPServerSocket = socket(family=AF_INET, type=SOCK_DGRAM)

# Binds to address and ip
UDPServerSocket.bind((localIP, localPort))

expected_seq_number = 0

prev_received_packet = b''
prev_sent_response = b''

# Listens for incoming datagrams
while True:
    rcvpkt, sender_socket = UDPServerSocket.recvfrom(BUFFER_SIZE)

    # Detect duplicate packets received.
    # Sends previously prepared packet back. 
    if rcvpkt == prev_received_packet:
        UDPServerSocket.sendto(prev_sent_response, sender_socket)
        continue

    data = rcvpkt[12:].decode()
    received_seq_number = extract_seq_number(rcvpkt)

    if verify_checksum(rcvpkt) and received_seq_number == expected_seq_number:
        senderMsg = 'packet is expected, message string delivered: {}'.format(data)
        print('packet num.{} received: {}'.format(packetNumber, rcvpkt))
        if packetNumber % 3 == 0 and packetNumber % 6 != 0:
            print('simulating packet bit errors/corrupted: ACK the previous packet!')
            UDPServerSocket.sendto(prev_sent_response, sender_socket)
        elif packetNumber % 6 == 0:
            print('simulating packet loss: sleep a while to trigger timeout event on the send side...')
            sleep(SLEEP_TIME_SECONDS)
        else:
            print(senderMsg)
            print('packet is delivered, now creating and sending the ACK packet...')
            sndpkt = make_packet('', received_seq_number, received_seq_number)
            UDPServerSocket.sendto(sndpkt, sender_socket)

            prev_received_packet = rcvpkt
            prev_sent_response = sndpkt

            expected_seq_number = (expected_seq_number + 1) % 2

        print('all done for this packet!\n')
        packetNumber += 1
    else:
        print('Checksum is not correct!!!')
