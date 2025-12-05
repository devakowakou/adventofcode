"""Day 3: Lobby

Read `input.txt` where each line is a bank of batteries represented by digits.
For each bank, turn on exactly two batteries (preserving order) to form a
two-digit joltage (tens from earlier battery, ones from later battery).
Compute the maximum such joltage per bank and print the sum across banks.

If no valid banks (lines containing only digits) are found, the script reports that.
"""

from typing import List


def max_joltage_from_bank(s: str, num_batteries: int = 2) -> int:
    """Return the maximum number obtainable from string of digits s
    by selecting exactly num_batteries positions (preserving order).
    
    For num_batteries=2: finds max two-digit number using O(n) scan.
    For larger num_batteries: skips the smallest digits to maximize result.
    """
    s = s.strip()
    if len(s) < num_batteries:
        return 0
    
    if num_batteries == 2:
        # Original O(n) algorithm for Part 1
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
    # Strategy: skip (len - num_batteries) smallest digits while maintaining order
    digits = [int(c) for c in s]
    n = len(digits)
    to_skip = n - num_batteries
    
    if to_skip == 0:
        return int(s)
    
    # Greedy: for each position in result, pick the largest digit we can
    # while leaving enough digits for remaining positions
    result = []
    start = 0
    
    for pos in range(num_batteries):
        remaining = num_batteries - pos - 1
        # We can pick from start to (n - remaining - 1)
        end = n - remaining
        
        # Find the max digit in this range
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
    banks_processed = 0
    total = 0
    per_bank = []
    with open(input_path, "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            # Only treat lines that are purely digits as banks
            if not line.isdigit():
                continue
            banks_processed += 1
            mj = max_joltage_from_bank(line, num_batteries)
            per_bank.append((line, mj))
            total += mj

    if banks_processed == 0:
        print("No battery banks found in input (no lines containing only digits).")
        return 0

    # Print a brief summary and result
    print(f"Part {'One' if num_batteries == 2 else 'Two'} (selecting {num_batteries} batteries):")
    print("Per-bank maxima:")
    for s, mj in per_bank:
        print(f"{s} -> {mj}")
    print("-" * 40)
    print(f"Total output joltage: {total}")
    return total


if __name__ == "__main__":
    print("=" * 60)
    solve(num_batteries=2)
    print("\n" + "=" * 60)
    solve(num_batteries=12)
