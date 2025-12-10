def parse_rotation(line):
    """Parse a rotation line like 'L68' or 'R48'."""
    direction = line[0]
    distance = int(line[1:])
    return direction, distance


def rotate_dial(current_pos, direction, distance):
    """
    Rotate the dial and return the new position.
    The dial has numbers 0-99.
    """
    if direction == 'L':
        new_pos = (current_pos - distance) % 100
    else:  # direction == 'R'
        new_pos = (current_pos + distance) % 100
    return new_pos


def count_zeros_during_rotation(start_pos, direction, distance):
    """
    Count how many times the dial points at 0 during a rotation.
    This includes intermediate positions but NOT the final position.
    """
    count = 0
    current = start_pos
    
    for _ in range(distance):
        if direction == 'L':
            current = (current - 1) % 100
        else:  # direction == 'R'
            current = (current + 1) % 100
        
        if current == 0:
            count += 1
    
    return count


def solve_part1(rotations):
    """
    Count how many times the dial points at 0 AFTER completing a rotation.
    """
    position = 50  # Starting position
    zero_count = 0
    
    for direction, distance in rotations:
        position = rotate_dial(position, direction, distance)
        if position == 0:
            zero_count += 1
    
    return zero_count


def solve_part2(rotations):
    """
    Count how many times the dial points at 0 during ANY click.
    This includes both during rotations and at the end of rotations.
    """
    position = 50  # Starting position
    zero_count = 0
    
    for direction, distance in rotations:
        # Count zeros during the rotation (intermediate positions)
        zeros_during = count_zeros_during_rotation(position, direction, distance)
        zero_count += zeros_during
        
        # Update position
        position = rotate_dial(position, direction, distance)
        
        # Note: We don't add 1 here if position == 0 because 
        # count_zeros_during_rotation already counted it as the final click
    
    return zero_count


def main():
    # Read the input file
    with open('input_day1.txt', 'r') as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]
    
    # Parse rotations
    rotations = [parse_rotation(line) for line in lines]
    
    # Part 1: Count zeros after rotations
    result_part1 = solve_part1(rotations)
    print(f"Part 1 - Password (zeros after rotations): {result_part1}")
    
    # Part 2: Count zeros during all clicks
    result_part2 = solve_part2(rotations)
    print(f"Part 2 - Password (zeros during all clicks): {result_part2}")


if __name__ == "__main__":
    main()
