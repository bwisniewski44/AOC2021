"""
TODO EXPLAIN

This script is part of a solution set devised to complete the 'Advent of Code' puzzles, year 2021:
https://adventofcode.com/2021
"""

import typing
import math
from structures import KeySet


class Packet:
    # Various field-lengths defined by the puzzle are encoded here
    VERSION_ENCODING_LENGTH = 3
    TYPE_CODE_LENGTH = 3
    LITERAL_GROUP_LENGTH = 5  # 4 bits + 1 end-indicator

    # Code defined by puzzle to indicate a packet which is of the "literal" format
    OPERATOR_LENGTH_FORMAT_STATIC = 0
    OPERATOR_LENGTH_FORMAT_DYNAMIC = 1

    PACKET_TYPES = KeySet()  # type: KeySet[int,typing.Callable[[typing.Union[int,typing.List[Packet]]], int]]
    PACKET_TYPE_SUM,                \
        PACKET_TYPE_PRODUCT,        \
        PACKET_TYPE_MINIMUM,        \
        PACKET_TYPE_MAXIMUM,        \
        PACKET_TYPE_LITERAL,        \
        PACKET_TYPE_GREATER_THAN,   \
        PACKET_TYPE_LESS_THAN,      \
        PACKET_TYPE_EQUAL_TO,       \
        = PACKET_TYPES.enumerate(
            [
                lambda content: sum(node.value for node in content),
                lambda content: math.prod(node.value for node in content),
                lambda content: min(node.value for node in content),
                lambda content: max(node.value for node in content),
                lambda content: content,
                lambda content: int(content[0].value > content[1].value),
                lambda content: int(content[0].value < content[1].value),
                lambda content: int(content[0].value == content[1].value),
            ]
        )

    def __init__(self, type_code, version, payload):
        """
        :param int type_code: TODO EXPLAIN
        :param int version:
        :param int|list[Packet] payload:
        """

        # Verify that one of two situations holds:
        # 1. this is a literal packet with an 'int' payload
        # 2. this is a non-literal packet with a non-'int' payload
        is_literal = (type_code == Packet.PACKET_TYPE_LITERAL)
        is_numeric = isinstance(payload, int)
        is_compatible = is_literal == is_numeric  # it better be that these are all-true, or all-false
        if not is_compatible:
            raise \
                ValueError(
                    f"Packet-type/payload mismatch for packet type {type_code} and payload of type {type(payload)}"
                )

        self._type = type_code
        self.version = version
        self._payload = payload

        try:
            compute_value = Packet.PACKET_TYPES[type_code]
        except KeyError:
            raise KeyError(f"Unrecognized packet type-code {type_code}")
        else:
            self._value = compute_value(payload)

    @property
    def is_literal(self):
        return self._type == Packet.PACKET_TYPE_LITERAL

    @property
    def value(self):
        return self._value

    @property
    def children(self):
        if self.is_literal:
            raise RuntimeError(f"Illegal attempt to access children from non-parent, literal packet")
        else:
            return self._payload

    def __repr__(self):
        if self.is_literal:
            return str(self.value)
        else:
            return "<" + ",".join(repr(child) for child in self.children) + ">"


def load_input(path="input.txt"):
    """
    TODO EXPLAIN

    :param str path: path to the file to read as input to this script

    :return: list of ``0`` and ``1`` characters
    :rtype: str
    """
    with open(path) as infile:
        lines = [str.strip(line) for line in infile.readlines()]
    return hex_to_bits(lines[0])


def hex_to_bits(hexadecimal_expression):
    """
    TODO EXPLAIN

    :param str hexadecimal_expression:

    :return:
    :rtype: str
    """

    # The leading line should be a string of hex digits; convert each such digit into its own string of bits
    bits = []  # type: typing.List[str]
    for hex_digit in hexadecimal_expression:
        # Get the abstract integer value represented by this hex digit
        value = int(hex_digit, 16)

        # Resolve the 4-bit binary expression which expresses that value
        binary_expression = bin(value)[2:]  # leading two chars are the '0b' prefix
        binary_expression = binary_expression.zfill(4)
        if len(binary_expression) != 4:
            raise \
                ValueError(
                    f"Expecting 4 binary digits, but found {len(binary_expression)} in binary expression "
                    f"'{binary_expression}'"
                )

        # Add those bits to the bit-list
        bits.extend(binary_expression)

    return "".join(bits)


def read(bits, read_pos, count):
    """
    TODO EXPLAIN

    :param str bits:
    :param int read_pos:
    :param int count:

    :raises IndexError: if unable to read ``count`` bits from the given position

    :return: 2-tuple giving...
      1. (str) substring of bits
      2. (int) new read-position
    :rtype: (str, int)
    """

    end_pos = read_pos + count
    if len(bits) < end_pos:
        raise IndexError(f"Unable to read {count} bits from index {read_pos} for {len(bits)}-length string")
    result = bits[read_pos:end_pos]

    return result, end_pos


def parse_literal_payload(bits, read_pos):
    """
    TODO EXPLAIN

    :param str bits:
    :param int read_pos:

    :return: 2-tuple giving...
      1. int - the value encoded in the payload
      2. int - end-index (exclusive) of the literal's encoding
    :rtype: (int, int)
    """

    # Iterate over the bit-string to collect those bits which form the literal value
    literal_bits = []  # type: typing.List[str]
    parsing = True
    while parsing:
        # Read the next group of bits; the group is composed of a prefix (giving whether there are more groups) followed
        # by this group's bits
        group, read_pos = read(bits, read_pos, Packet.LITERAL_GROUP_LENGTH)

        # All but the first bit of this group get appended to the literal's bit-expression
        literal_bits.extend(group[1:])

        # The first bit gives whether there are remaining groups to parse
        parsing = (group[0] == "1")

    # Condense the bits into a single expression, and resolve the value thereof
    literal_expression = "".join(literal_bits)
    literal_value = int(literal_expression, 2)

    return literal_value, read_pos


def parse_packet(bits, read_pos=0):
    """
    TODO EXPLAIN

    :param str bits:
    :param int read_pos:

    :return:
    :rtype: (Packet, int)
    """

    # Extract the 3-bit packet version
    packet_version_encoding, read_pos = read(bits, read_pos, Packet.VERSION_ENCODING_LENGTH)
    packet_version = int(packet_version_encoding, 2)

    # Extract the 3-bit type-code
    type_code_expression, read_pos = read(bits, read_pos, Packet.TYPE_CODE_LENGTH)
    type_code = int(type_code_expression, 2)

    # If this packet is a literal, parse it out
    if type_code == Packet.PACKET_TYPE_LITERAL:
        literal_value, read_pos = parse_literal_payload(bits, read_pos)
        result = Packet(type_code, packet_version, literal_value)
    else:
        # Extract the length descriptor
        inner_packets = []  # type: typing.List[Packet]
        length_descriptor, read_pos = read(bits, read_pos, 1)

        # If the length descriptor indicates a length specifying the number of bits...
        if length_descriptor == "0":
            length_expression, read_pos = read(bits, read_pos, 15)
            length = int(length_expression, 2)
            destination_pos = read_pos + length

            while read_pos < destination_pos:
                inner_packet, read_pos = parse_packet(bits, read_pos)
                inner_packets.append(inner_packet)

            if read_pos != destination_pos:
                raise \
                    RuntimeError(
                        f"Packet parsing over-consumed; expecting inner packet parse to terminate at "
                        f"{destination_pos}, but actually terminated at index {read_pos}"
                    )

        # Otherwise, length descriptor indicates a length which specifies the number of inner-nested packets
        else:
            length_expression, read_pos = read(bits, read_pos, 11)
            length = int(length_expression, 2)

            for _ in range(length):
                inner_packet, read_pos = parse_packet(bits, read_pos)
                inner_packets.append(inner_packet)

        result = Packet(type_code, packet_version, inner_packets)

    return result, read_pos


def parse_input(bits):
    """
    TODO EXPLAIN

    :param str bits:

    :return:
    :rtype: list[Packet]
    """

    packets = []

    read_pos = 0
    while read_pos < len(bits):
        try:
            next_packet, read_pos = parse_packet(bits, read_pos)
        except IndexError as error:
            # This might not be the worst thing in the world; we may have run into a situation where the remaining bits
            # are 'padding 0s': non-significant bits which were required by the original hex
            remaining_bits = len(bits) - read_pos
            if remaining_bits < 8 and all(bit == "0" for bit in bits[-remaining_bits:]):
                read_pos = len(bits)
                break
            else:
                print(f"ERROR during parse: {error}")
                raise

        packets.append(next_packet)

    if read_pos != len(bits):
        raise \
            RuntimeError(
                f"Packet-parsing stopped at index {read_pos}, failing to exactly consume {len(bits)}-bit string"
            )

    return packets


def _recursive_sum_versions(packet):
    """
    TODO EXPLAIN

    :param Packet packet:

    :return:
    :rtype: int
    """

    # Version sum is the this packet's version plus the sum of all child versions
    result = packet.version
    if not packet.is_literal:
        for child in packet.children:
            result += _recursive_sum_versions(child)

    return result


def sum_versions(packets):
    """
    TODO EXPLAIN

    :param list[Packet] packets:

    :return:
    :rtype: int
    """

    return sum(_recursive_sum_versions(packet) for packet in packets)


def main():
    """
    TODO EXPLAIN

    :return: None
    """
    bits = load_input()

    # Part 1: sum the version numbers associated with every packet (including nested packets)
    packets = parse_input(bits)
    print(sum_versions(packets))

    # Part 2: print the value of the packet
    print(packets[0].value)


if __name__ == "__main__":
    main()
