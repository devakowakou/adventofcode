def is_invalid_id(num):
    """
    Check if a number is invalid (made of some sequence repeated twice).
    Examples: 55 (5 twice), 6464 (64 twice), 123123 (123 twice)
    """
    num_str = str(num)
    length = len(num_str)
    if length % 2 != 0:
        return False
    mid = length // 2
    first_half = num_str[:mid]
    second_half = num_str[mid:]
    if first_half[0] == '0':
        return False
    
    return first_half == second_half


def solve():
    with open('input.txt', 'r') as f:
        ranges_input = f.read().strip()
    ranges = []
    for range_str in ranges_input.split(','):
        range_str = range_str.strip()
        if range_str:
            start, end = map(int, range_str.split('-'))
            ranges.append((start, end))
    total_sum = 0
    
    for start, end in ranges:
        for num in range(start, end + 1):
            if is_invalid_id(num):
                total_sum += num
    
    return total_sum


if __name__ == "__main__":
    result = solve()
    print(f"Sum of all invalid IDs: {result}")
