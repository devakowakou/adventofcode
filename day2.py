def is_repeated_twice(num_str):
    """
    Check if a number is made of a sequence repeated exactly twice.
    E.g., 55 (5 twice), 6464 (64 twice), 123123 (123 twice)
    """
    length = len(num_str)
    
    # Must be even length to be repeated twice
    if length % 2 != 0:
        return False
    
    # Split in half and check if both halves are the same
    mid = length // 2
    first_half = num_str[:mid]
    second_half = num_str[mid:]
    
    return first_half == second_half


def is_repeated_pattern(num_str):
    """
    Check if a number is made of a sequence repeated at least twice.
    E.g., 12341234 (1234 two times), 123123123 (123 three times), etc.
    """
    length = len(num_str)
    
    # Try all possible pattern lengths from 1 to length//2
    for pattern_length in range(1, length // 2 + 1):
        # Check if the total length is divisible by pattern length
        if length % pattern_length == 0:
            pattern = num_str[:pattern_length]
            repetitions = length // pattern_length
            
            # Must repeat at least twice
            if repetitions >= 2:
                # Check if the entire number is this pattern repeated
                if pattern * repetitions == num_str:
                    return True
    
    return False


def parse_ranges(input_line):
    """Parse the comma-separated ranges."""
    ranges = []
    parts = input_line.strip().rstrip(',').split(',')
    
    for part in parts:
        start, end = part.split('-')
        ranges.append((int(start), int(end)))
    
    return ranges


def solve_part1(ranges):
    """
    Find all invalid IDs (repeated exactly twice) and sum them.
    """
    total = 0
    
    for start, end in ranges:
        for num in range(start, end + 1):
            num_str = str(num)
            if is_repeated_twice(num_str):
                total += num
    
    return total


def solve_part2(ranges):
    """
    Find all invalid IDs (repeated at least twice) and sum them.
    """
    total = 0
    
    for start, end in ranges:
        for num in range(start, end + 1):
            num_str = str(num)
            if is_repeated_pattern(num_str):
                total += num
    
    return total


def main():
    # Read the input file
    with open('input_day2.txt', 'r') as f:
        input_line = f.read().strip()
    
    # Parse ranges
    ranges = parse_ranges(input_line)
    
    print(f"Found {len(ranges)} ranges to check")
    
    # Part 1: IDs repeated exactly twice
    result_part1 = solve_part1(ranges)
    print(f"Part 1 - Sum of invalid IDs (repeated twice): {result_part1}")
    
    # Part 2: IDs repeated at least twice
    result_part2 = solve_part2(ranges)
    print(f"Part 2 - Sum of invalid IDs (repeated at least twice): {result_part2}")


if __name__ == "__main__":
    main()
