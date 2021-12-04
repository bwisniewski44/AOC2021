import typing

_ALPHABET = {"0", "1"}  # TODO: explain


def calculate_optima(digits, expected_count):
    """
    TODO EXPLAIN

    :param dict[str,int] digits:
    :param int expected_count:

    :return: 2-tuple giving...
      1. (str) least-populous digit among the set
      2. (str) most-populous digit among the set
    :rtype: (str, str)
    """

    digits_and_counts = [(digit, count) for digit, count in digits.items()]
    max_digit, max_count = digits_and_counts[0]
    min_digit, min_count = digits_and_counts[0]

    i = 1
    total_count = max_count
    while i < len(digits_and_counts):
        next_digit, next_count = digits_and_counts[i]
        total_count += next_count
        if next_count > max_count:
            max_digit = next_digit
            max_count = next_count
        elif next_count < min_count:
            min_digit = next_digit
            min_count = next_count

        i += 1

    # Ensure that the total digit count across all digits is that which is expected
    if total_count != expected_count:
        raise ValueError(f"Expecting a count of {expected_count}, but tallied a total of {total_count}")

    # Ensure that the optima are authoritative (there isn't a tie for 1st or a tie for last)
    maxima_count = minima_count = 0
    for _, count in digits_and_counts:
        if count == max_count:
            maxima_count += 1
        if count == min_count:
            minima_count += 1
    if maxima_count != 1:
        raise \
            ValueError(
                f"There are {maxima_count} maxima, each having {max_count} presentations; expecting 1 such maximum"
            )
    elif minima_count != 1:
        raise \
            ValueError(
                f"There are {minima_count} minima, each having {min_count} presentations; expecting 1 such minimum"
            )

    return max_digit, min_digit


def evaluate_expression(digits):
    """
    TODO EXPLAIN

    :param list[str] digits:

    :return:
    :rtype: int
    """
    binary_expression = "".join(digits)
    result = int(binary_expression, 2)
    return result


def load_values(path="input.txt"):
    """
    TODO EXPLAIN

    :param str path:

    :return: 2-tuple giving...
      1. (int) GAMMA RATE
      2. (int) EPSILON RATE
    :rtype: (int, int)
    """

    with open(path) as infile:
        lines = [line.strip() for line in infile.readlines()]

    # Initialize a vector of dictionaries, as many dictionaries as there are glyphs for any line; as we iterate over the
    # lines of the file, and the characters of each line, we'll go to that index's dictionary and add 1 to the counter
    # for the respective character found
    counter_sequence = []     # type: typing.List[typing.Dict[str,int]]  # (str)glyph->(int)count, one for each index
    if len(lines) == 0:
        raise ValueError(f"File '{path}' has no lines")
    else:
        line_width = len(lines[0])
        while len(counter_sequence) < line_width:
            initialized_dict = {}
            counter_sequence.append(initialized_dict)

    # For each line...
    for i, line in enumerate(lines):
        # Validate that this line has a length exactly as that we're expecting
        if len(line) != len(counter_sequence):
            raise \
                ValueError(
                    f"Expecting lines of length {len(counter_sequence)}, but encountered {len(line)}-char line at "
                    f"line index {i}"
                )

        # ... and for each char in the respective line...
        for j, glyph in enumerate(line):
            # validate the character seen at this position
            if glyph not in _ALPHABET:
                raise ValueError(f"Encountered illegal character '{glyph}' at index {j} of line {i}")

            # ... retrieve the glyph-counter corresponding to this character's index
            glyph_counter = counter_sequence[j]
            old_count = glyph_counter.get(glyph, 0)     # find the tally of this glyph for this position (use 0 if none)
            glyph_counter[glyph] = old_count + 1        # ensure the counter has an incremented tally

    # All the lines' glyphs have been counted; time to find the winning glyph per line
    gamma_digits = []       # type: typing.List[str]
    epsilon_digits = []     # type: typing.List[str]
    for glyph_counter in counter_sequence:
        # The next gamma digit is that which is most-frequently found at this position
        epsilon_digit, gamma_digit = calculate_optima(glyph_counter, len(lines))
        gamma_digits.append(gamma_digit)
        epsilon_digits.append(epsilon_digit)

    gamma_value = evaluate_expression(gamma_digits)
    epsilon_value = evaluate_expression(epsilon_digits)

    return gamma_value, epsilon_value


def do():
    """
    TODO EXPLAIN

    :return: None
    """

    gamma_rate, epsilon_rate = load_values()
    rates_product = gamma_rate * epsilon_rate
    print(f"{rates_product}")


if __name__ == "__main__":
    do()
