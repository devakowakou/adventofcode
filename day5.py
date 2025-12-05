def parse_input(filename):
    """
    Parse the input file into fresh ranges and available ingredient IDs.
    Returns: (list of tuples for ranges, list of ingredient IDs)
    """
    with open(filename, 'r') as f:
        lines = [line.strip() for line in f.readlines()]
    
    # Find the blank line that separates ranges from IDs
    blank_line_idx = lines.index('')
    
    # Parse ranges
    ranges = []
    for line in lines[:blank_line_idx]:
        if line:
            start, end = line.split('-')
            ranges.append((int(start), int(end)))
    
    # Parse available ingredient IDs
    ingredient_ids = []
    for line in lines[blank_line_idx + 1:]:
        if line:
            ingredient_ids.append(int(line))
    
    return ranges, ingredient_ids


def is_fresh(ingredient_id, ranges):
    """
    Check if an ingredient ID is fresh (falls within any range).
    """
    for start, end in ranges:
        if start <= ingredient_id <= end:
            return True
    return False


def solve_part1(ranges, ingredient_ids):
    """
    Count how many of the available ingredient IDs are fresh.
    """
    fresh_count = 0
    
    for ingredient_id in ingredient_ids:
        if is_fresh(ingredient_id, ranges):
            fresh_count += 1
    
    return fresh_count


def merge_ranges(ranges):
    """
    Merge overlapping ranges and return a list of non-overlapping ranges.
    """
    if not ranges:
        return []
    
    # Sort ranges by start position
    sorted_ranges = sorted(ranges)
    merged = [sorted_ranges[0]]
    
    for current_start, current_end in sorted_ranges[1:]:
        last_start, last_end = merged[-1]
        
        # Check if current range overlaps with the last merged range
        # Ranges overlap if current_start <= last_end + 1
        if current_start <= last_end + 1:
            # Merge by extending the end if necessary
            merged[-1] = (last_start, max(last_end, current_end))
        else:
            # No overlap, add as new range
            merged.append((current_start, current_end))
    
    return merged


def solve_part2(ranges):
    """
    Count total unique ingredient IDs considered fresh by the ranges.
    """
    # Merge overlapping ranges first
    merged = merge_ranges(ranges)
    
    # Count total IDs in all merged ranges
    total_count = 0
    for start, end in merged:
        total_count += (end - start + 1)
    
    return total_count


def main():
    # Parse input
    ranges, ingredient_ids = parse_input('input_day5.txt')
    
    print(f"Found {len(ranges)} fresh ingredient ranges")
    print(f"Found {len(ingredient_ids)} available ingredient IDs to check")
    
    # Part 1: Count fresh ingredients
    result_part1 = solve_part1(ranges, ingredient_ids)
    print(f"\nPart 1 - Number of fresh ingredient IDs: {result_part1}")
    
    # Part 2: Count all unique IDs in fresh ranges
    result_part2 = solve_part2(ranges)
    print(f"Part 2 - Total ingredient IDs considered fresh: {result_part2}")


if __name__ == "__main__":
    main()
