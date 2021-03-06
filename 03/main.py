import typing

_ALPHABET = {"0", "1"}  # TODO: explain


def calculate_optima(line_indices_by_glyph, expected_count=None, tie_breaker=None):
    """
    TODO EXPLAIN

    :param dict[str,set[int]] line_indices_by_glyph:
    :param int expected_count:
    :param str tie_breaker:

    :return: 2-tuple giving...
      1. (str) least-populous digit among the set
      2. (str) most-populous digit among the set
    :rtype: (str, str)
    """

    digits_and_counts = [(digit, len(indices)) for digit, indices in line_indices_by_glyph.items()]
    max_digit, max_count = digits_and_counts[0]
    min_digit, min_count = digits_and_counts[0]

    i = 1
    total_count = max_count
    while i < len(digits_and_counts):
        next_digit, next_count = digits_and_counts[i]
        total_count += next_count

        # Update the maximum if necessary
        if next_count == max_count and tie_breaker in {next_digit, max_digit}:
            max_digit = tie_breaker
        elif next_count > max_count:
            max_digit = next_digit
            max_count = next_count

        # Update the minimum if necessary
        if next_count == min_count and tie_breaker in {next_digit, min_digit}:
            min_digit = tie_breaker
        elif next_count < min_count:
            min_digit = next_digit
            min_count = next_count

        i += 1

    # Ensure that the total digit count across all digits is that which is expected
    if expected_count and total_count != expected_count:
        raise ValueError(f"Expecting a count of {expected_count}, but tallied a total of {total_count}")

    # Ensure that the optima are authoritative (there isn't a tie for 1st or a tie for last)
    if not tie_breaker:
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

    return min_digit, max_digit


def filter_(lines_by_glyph_by_pos, prefer_max):
    """
    TODO EXPLAIN

    :param list[dict[str,set[int]]] lines_by_glyph_by_pos:
    :param bool prefer_max:

    :return:
    :rtype: int
    """

    # Resolve the total line-count; should be the sum of the sizes of any of the glyph sets for a position
    total_line_count = sum(len(lines) for glyph, lines in lines_by_glyph_by_pos[0].items())
    candidates = set(range(total_line_count))
    tie_breaker = "1" if prefer_max else "0"

    for i, lines_by_glyph in enumerate(lines_by_glyph_by_pos):
        if len(candidates) == 1:
            break
        next_lines_by_glyph = lines_by_glyph_by_pos[i]
        filtered_lines_by_glyph = {
            glyph: candidates.intersection(lines) for glyph, lines in next_lines_by_glyph.items()
        }

        min_digit, max_digit = calculate_optima(filtered_lines_by_glyph, tie_breaker=tie_breaker)
        selector = max_digit if prefer_max else min_digit
        candidates = filtered_lines_by_glyph[selector]

    if len(candidates) != 1:
        raise \
            ValueError(
                f"Expecting a decisive candidate, but remaining candidate set contains {len(candidates)} elements"
            )
    result_index = next(iter(candidates))
    return result_index


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
      3. (int) O2 RATING
      4. (int) C02 RATING
    :rtype: (int, int, int, int)
    """

    with open(path) as infile:
        lines = [line.strip() for line in infile.readlines()]

    # Initialize a vector of dictionaries, as many dictionaries as there are glyphs for any line; as we iterate over the
    # lines of the file, and the characters of each line, we'll go to that index's dictionary and add the line index to
    # the set corresponding to the character found
    counter_sequence = []     # type: typing.List[typing.Dict[str,typing.Set[int]]]  # (str)glyph->set[int] line indices
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
            line_indices_by_glyph = counter_sequence[j]
            if glyph in line_indices_by_glyph:
                line_indices = line_indices_by_glyph[glyph]
            else:
                line_indices = set()    # type: typing.Set[int]
                line_indices_by_glyph[glyph] = line_indices
            line_indices.add(i)

    # All the lines' glyphs have been counted; time to find the winning glyph per line
    gamma_digits = []       # type: typing.List[str]
    epsilon_digits = []     # type: typing.List[str]
    for line_indices_by_glyph in counter_sequence:
        # The next gamma digit is that which is most-frequently found at this position
        epsilon_digit, gamma_digit = calculate_optima(line_indices_by_glyph, len(lines))
        gamma_digits.append(gamma_digit)
        epsilon_digits.append(epsilon_digit)

    gamma_value = evaluate_expression(gamma_digits)
    epsilon_value = evaluate_expression(epsilon_digits)

    oxygen_rating = evaluate_expression(list(lines[filter_(counter_sequence, True)]))
    c02_rating = evaluate_expression(list(lines[filter_(counter_sequence, False)]))

    return gamma_value, epsilon_value, oxygen_rating, c02_rating


def do():
    """
    TODO EXPLAIN

    :return: None
    """

    gamma_rate, epsilon_rate, o2_rating, c02_rating = load_values()
    rates_product = gamma_rate * epsilon_rate
    ratings_product = o2_rating * c02_rating
    print(f"{rates_product}")
    print(f"{ratings_product}")


if __name__ == "__main__":
    do()
