def count_adjacent_rolls(grid, row, col):
    """Count how many adjacent positions contain paper rolls."""
    rows = len(grid)
    cols = len(grid[0])
    
    # 8 directions: N, NE, E, SE, S, SW, W, NW
    directions = [
        (-1, 0), (-1, 1), (0, 1), (1, 1),
        (1, 0), (1, -1), (0, -1), (-1, -1)
    ]
    
    adjacent_count = 0
    for dr, dc in directions:
        new_row = row + dr
        new_col = col + dc
        
        # Check if position is within bounds
        if 0 <= new_row < rows and 0 <= new_col < cols:
            if grid[new_row][new_col] == '@':
                adjacent_count += 1
    
    return adjacent_count


def find_accessible_rolls(grid):
    """Find all rolls that can be accessed (have fewer than 4 adjacent rolls)."""
    rows = len(grid)
    cols = len(grid[0])
    accessible = []
    
    for row in range(rows):
        for col in range(cols):
            # Only check positions with paper rolls
            if grid[row][col] == '@':
                if count_adjacent_rolls(grid, row, col) < 4:
                    accessible.append((row, col))
    
    return accessible


def count_accessible_rolls(grid):
    """Count paper rolls that can be accessed by forklifts (Part 1)."""
    return len(find_accessible_rolls(grid))


def remove_all_accessible_rolls(grid):
    """
    Iteratively remove accessible rolls until none remain (Part 2).
    Returns the total number of rolls removed.
    """
    # Convert to list of lists for mutability
    grid = [list(row) for row in grid]
    total_removed = 0
    
    while True:
        # Find all accessible rolls
        accessible = find_accessible_rolls(grid)
        
        if not accessible:
            break
        
        # Remove all accessible rolls
        for row, col in accessible:
            grid[row][col] = '.'
        
        total_removed += len(accessible)
    
    return total_removed


def main():
    # Read the input file
    with open('input.txt', 'r') as f:
        grid = [line.strip() for line in f.readlines()]
    
    # Part 1: Count accessible rolls
    result_part1 = count_accessible_rolls(grid)
    print(f"Part 1 - Number of rolls accessible by forklift: {result_part1}")
    
    # Part 2: Total rolls that can be removed
    result_part2 = remove_all_accessible_rolls(grid)
    print(f"Part 2 - Total rolls that can be removed: {result_part2}")


if __name__ == "__main__":
    main()
