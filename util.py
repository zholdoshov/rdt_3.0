def create_checksum(packet_wo_checksum):
    """create the checksum of the packet (MUST-HAVE DO-NOT-CHANGE)

    Args:
      packet_wo_checksum: the packet byte data (including headers except for checksum field)

    Returns:
      the checksum in bytes

    """

    total = 0

    # Add up 16-bit words
    to_hex = list(map(''.join, zip(*[iter(packet_wo_checksum.hex())]*4)))
    for i in to_hex:
        total += int(i, 16)

    # Add any left over byte
    if len(packet_wo_checksum) % 2:
        total += packet_wo_checksum[-1] << 8

    # Fold 32-bits into 16-bits
    total = (total >> 16) + (total & 0xffff)
    total += total >> 16
    
    return (~total + 0x10000 & 0xffff).to_bytes(2, byteorder='big')


def verify_checksum(packet):
    """verify packet checksum (MUST-HAVE DO-NOT-CHANGE)

    Args:
      packet: the whole (including original checksum) packet byte data

    Returns:
      True if the packet checksum is the same as specified in the checksum field
      False otherwise

    """

    total = 0

    # Add up 16-bit words
    to_hex = list(map(''.join, zip(*[iter(packet.hex())]*4)))
    for i in to_hex:
        total += int(i, 16)

    # Add any left over byte
    if len(packet) % 2:
        total += packet[-1] << 8

    # Fold 32-bits into 16-bits
    total = (total >> 16) + (total & 0xffff)
    total += total >> 16

    return True if total == 0xffff else False


def make_packet(data_str, ack_num, seq_num):
    """Make a packet (MUST-HAVE DO-NOT-CHANGE)

    Args:
      data_str: the string of the data (to be put in the Data area)
      ack: an int tells if this packet is an ACK packet (1: ack, 0: non ack)
      seq_num: an int tells the sequence number, i.e., 0 or 1

    Returns:
      a created packet in bytes

    """

    const_bytes = "COMPNETW".encode()

    # returns a binary string of length 14
    length = calculate_packet_size(len(data_str.encode()) + 12, 14)

    # a string of size 16-bits consists of only 1s and 0s
    last_two = length + str(ack_num) + str(seq_num)

    # last two bytes of the header (Length with ACK and sequence number)
    last_two_bytes = int(last_two, 2).to_bytes(2, byteorder='big')

    # packet without checksum for creating checksum
    packet_wo_checksum = const_bytes + last_two_bytes + data_str.encode()
    
    packet = const_bytes + create_checksum(packet_wo_checksum) + last_two_bytes + data_str.encode()

    return packet

    # make sure your packet follows the required format!


def calculate_packet_size(data_plus_header, n):
    """Returns a binary string with n length

      :type data_plus_header: int
      :rtype: str

    """

    int_to_bin_str = str(bin(data_plus_header))[2:]
    bin_str = int_to_bin_str[::-1] + (n - len(int_to_bin_str)) * '0'
    return bin_str[::-1]


def extract_ack_number(packet):
    """Returns an ack number of the packet

      :type packet: bytes
      :rtype: int

    """

    length_byte = packet[10:12]
    to_decimal = int.from_bytes(length_byte, 'big')
    to_binary = str(bin(to_decimal))[2:]
    ack_number_bit = to_binary[-2:-1]

    return int(ack_number_bit)


def extract_seq_number(packet):
    """Returns a sequence number of the packet

      :type packet: bytes
      :rtype: int

    """

    length_byte = packet[10:12]
    to_decimal = int.from_bytes(length_byte, 'big')
    to_binary = str(bin(to_decimal))[2:]
    seq_number_bit = to_binary[-1:]

    return int(seq_number_bit)


###### These three functions will be automatically tested while grading. ######
###### Hence, your implementation should NOT make any changes to         ######
###### the above function names and args list.                           ######
###### You can have other helper functions if needed.                    ######
