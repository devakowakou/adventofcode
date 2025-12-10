def parse_worksheet_part2(filename):
    """
    Parse worksheet for Part 2: Read right-to-left, column by column.
    Each column forms a number (most significant digit at top).
    Problems are separated by columns of all spaces.
    """
    with open(filename, 'r') as f:
        lines = [line.rstrip('\n') for line in f.readlines()]
    
    # The last line contains the operations
    operations_line = lines[-1]
    number_lines = lines[:-1]
    
    # Find max width
    max_width = max(len(line) for line in lines)
    
    # Pad all lines
    padded_number_lines = [line.ljust(max_width) for line in number_lines]
    padded_operations = operations_line.ljust(max_width)
    
    # Process right-to-left, column by column
    problems = []
    current_numbers = []
    current_operation = None
    
    # Go through columns from right to left
    for col_idx in range(max_width - 1, -1, -1):
        # Check if this is a separator column (all spaces)
        is_separator = all(
            line[col_idx] == ' ' 
            for line in padded_number_lines
        ) and padded_operations[col_idx] == ' '
        
        if is_separator:
            # End of current problem if we have one
            if current_numbers and current_operation:
                problems.append((current_numbers, current_operation))
                current_numbers = []
                current_operation = None
        else:
            # Extract the number formed by this column (top to bottom)
            digits = []
            for line in padded_number_lines:
                char = line[col_idx]
                if char.isdigit():
                    digits.append(char)
            
            if digits:
                # Form number from digits (top = most significant)
                number = int(''.join(digits))
                current_numbers.append(number)
            
            # Get operation
            op_char = padded_operations[col_idx]
            if op_char in ['+', '*']:
                current_operation = op_char
    
    # Don't forget the last problem
    if current_numbers and current_operation:
        problems.append((current_numbers, current_operation))
    
    return problems


def parse_worksheet(filename):
    """
    Parse the worksheet for Part 1.
    Problems are separated by multiple spaces (columns of spaces).
    Each problem has numbers stacked vertically with an operation at the bottom.
    """
    with open(filename, 'r') as f:
        lines = [line.rstrip('\n') for line in f.readlines()]
    
    # The last line contains the operations
    operations_line = lines[-1]
    number_lines = lines[:-1]
    
    # Find max width
    max_width = max(len(line) for line in lines)
    
    # Pad all lines
    padded_number_lines = [line.ljust(max_width) for line in number_lines]
    padded_operations = operations_line.ljust(max_width)
    
    # Identify separator columns (spaces in all lines including operation)
    separator_positions = []
    for col_idx in range(max_width):
        is_separator = all(
            line[col_idx] == ' ' 
            for line in padded_number_lines
        ) and padded_operations[col_idx] == ' '
        
        if is_separator:
            separator_positions.append(col_idx)
    
    # Find continuous ranges of separators to identify problem boundaries
    problem_ranges = []
    start = 0
    i = 0
    while i <= max_width:
        if i == max_width or i in separator_positions:
            if i > start and i - 1 not in separator_positions:
                problem_ranges.append((start, i))
            if i < max_width and i in separator_positions:
                while i < max_width and i in separator_positions:
                    i += 1
                start = i
                continue
        i += 1
    
    # Extract problems from ranges
    problems = []
    for start, end in problem_ranges:
        problem_numbers = []
        for line in padded_number_lines:
            segment = line[start:end].strip()
            if segment:
                nums = segment.split()
                problem_numbers.extend([int(n) for n in nums])
        
        operation = padded_operations[start:end].strip()
        
        if problem_numbers and operation in ['+', '*']:
            problems.append((problem_numbers, operation))
    
    return problems


def solve_problem(numbers, operation):
    """
    Solve a single problem by applying the operation to all numbers.
    """
    if not numbers:
        return 0
    
    result = numbers[0]
    for num in numbers[1:]:
        if operation == '+':
            result += num
        elif operation == '*':
            result *= num
    
    return result


def main():
    # Part 1: Parse left-to-right
    problems_part1 = parse_worksheet('input_day6.txt')
    
    print(f"Part 1: Found {len(problems_part1)} problems")
    
    grand_total_part1 = 0
    for i, (numbers, operation) in enumerate(problems_part1):
        result = solve_problem(numbers, operation)
        grand_total_part1 += result
        
        if i < 3:
            nums_str = ' '.join(map(str, numbers))
            print(f"  Problem {i+1}: {nums_str} {operation} -> {result}")
    
    print(f"Part 1 Grand Total: {grand_total_part1}\n")
    
    # Part 2: Parse right-to-left, column by column
    problems_part2 = parse_worksheet_part2('input_day6.txt')
    
    print(f"Part 2: Found {len(problems_part2)} problems")
    
    grand_total_part2 = 0
    for i, (numbers, operation) in enumerate(problems_part2):
        result = solve_problem(numbers, operation)
        grand_total_part2 += result
        
        if i < 3:
            nums_str = ' '.join(map(str, numbers))
            print(f"  Problem {i+1}: {nums_str} {operation} -> {result}")
    
    print(f"Part 2 Grand Total: {grand_total_part2}")


if __name__ == "__main__":
    main()
