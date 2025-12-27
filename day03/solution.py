"""Day 3: Lobby - Advent of Code

For each bank of batteries (line of digits), find the maximum joltage by
selecting exactly N batteries (preserving order).
Part 1: N=2 batteries (2-digit number)
Part 2: N=12 batteries (12-digit number)
"""

from typing import List


def max_joltage_from_bank(s: str, num_batteries: int = 2) -> int:
    """Return the maximum number obtainable from string of digits s
    by selecting exactly num_batteries positions (preserving order).
    """
    s = s.strip()
    if len(s) < num_batteries:
        return 0
    
    if num_batteries == 2:
        # Optimized algorithm for Part 1
        digits: List[int] = [ord(c) - 48 for c in s]
        max_right = -1
        max_val = 0
        for d in reversed(digits):
            if max_right >= 0:
                val = d * 10 + max_right
                if val > max_val:
                    max_val = val
            if d > max_right:
                max_right = d
        return max_val
    
    # For Part 2: select num_batteries digits to maximize the result
    digits = [int(c) for c in s]
    n = len(digits)
    
    if n == num_batteries:
        return int(s)
    
    # Greedy: for each position in result, pick the largest digit we can
    # while leaving enough digits for remaining positions
    result = []
    start = 0
    
    for pos in range(num_batteries):
        remaining = num_batteries - pos - 1
        end = n - remaining
        
        # Find the max digit in valid range
        max_digit = -1
        max_idx = start
        for i in range(start, end):
            if digits[i] > max_digit:
                max_digit = digits[i]
                max_idx = i
        
        result.append(str(max_digit))
        start = max_idx + 1
    
    return int(''.join(result))


def solve(input_path: str = "input.txt", num_batteries: int = 2) -> int:
    """Solve the problem for a given number of batteries to select."""
    total = 0
    banks_processed = 0
    
    with open(input_path, "r") as f:
        for line in f:
            line = line.strip()
            if not line or not line.isdigit():
                continue
            banks_processed += 1
            total += max_joltage_from_bank(line, num_batteries)

    if banks_processed == 0:
        print("No battery banks found in input.")
        return 0

    return total


if __name__ == "__main__":
    # Part 1: Select 2 batteries
    part1 = solve(num_batteries=2)
    print(f"Part 1 (2 batteries): {part1}")
    
    # Part 2: Select 12 batteries
    part2 = solve(num_batteries=12)
    print(f"Part 2 (12 batteries): {part2}")