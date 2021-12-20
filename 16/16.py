"""
TODO EXPLAIN

This script is part of a solution set devised to complete the 'Advent of Code' puzzles, year 2021:
https://adventofcode.com/2021
"""

import typing


class Packet:
    # Various field-lengths defined by the puzzle are encoded here
    VERSION_ENCODING_LENGTH = 3
    TYPE_CODE_LENGTH = 3
    LITERAL_GROUP_LENGTH = 5  # 4 bits + 1 end-indicator

    # Code defined by puzzle to indicate a packet which is of the "literal" format
    PACKET_TYPE_LITERAL = 4  # defined by puzzle parameters

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

    @property
    def is_literal(self):
        return self._type == Packet.PACKET_TYPE_LITERAL

    @property
    def value(self):
        if self.is_literal:
            return self._payload
        else:
            raise RuntimeError(f"Illegal attempt to read value of non-literal packet")

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
            return "[" + ", ".join(repr(child) for child in self.children) + "]"


def load_input(path="input.txt"):
    """
    TODO EXPLAIN

    :param str path: path to the file to read as input to this script

    :return: list of ``0`` and ``1`` characters
    :rtype: str
    """
    with open(path) as infile:
        lines = [str.strip(line) for line in infile.readlines()]

    # The leading line should be a string of hex digits; convert each such digit into its own string of bits
    bits = []  # type: typing.List[str]
    for hex_digit in lines[0]:
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
        group = bits[read_pos:read_pos+Packet.LITERAL_GROUP_LENGTH]
        read_pos += Packet.LITERAL_GROUP_LENGTH
        if len(group) != Packet.LITERAL_GROUP_LENGTH:
            raise \
                ValueError(
                    f"Expecting {Packet.LITERAL_GROUP_LENGTH} bits in literal group; encountered {len(group)} for "
                    f"group '{group}'"
                )

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
    packet_version_encoding = bits[read_pos:read_pos+Packet.VERSION_ENCODING_LENGTH]
    packet_version = int(packet_version_encoding, 2)
    read_pos += Packet.VERSION_ENCODING_LENGTH

    # Extract the 3-bit type-code
    type_code_expression = bits[read_pos:read_pos+Packet.TYPE_CODE_LENGTH]
    type_code = int(type_code_expression, 2)
    read_pos += Packet.TYPE_CODE_LENGTH

    # If this packet is a literal, parse it out
    if type_code == Packet.PACKET_TYPE_LITERAL:
        literal_value, read_pos = parse_literal_payload(bits, read_pos)
        result = Packet(type_code, packet_version, literal_value)
    else:
        pass

    return result, read_pos


def main():
    """
    TODO EXPLAIN

    :return: None
    """
    bits = load_input()
    packet = parse_packet("110100101111111000101000")


if __name__ == "__main__":
    main()
