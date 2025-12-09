def parse_manifold(filename):
    """Parse the manifold diagram and return the grid."""
    with open(filename, 'r') as f:
        grid = [line.rstrip('\n') for line in f.readlines()]
    return grid


def find_start(grid):
    """Find the starting position S."""
    for row_idx, row in enumerate(grid):
        for col_idx, char in enumerate(row):
            if char == 'S':
                return (row_idx, col_idx)
    return None


def simulate_beam(grid, start_row, start_col):
    """
    Simulate tachyon beam propagation.
    Returns the total number of splits.
    """
    rows = len(grid)
    cols = len(grid[0]) if rows > 0 else 0
    
    # Track active beams: list of (row, col) positions
    beams = [(start_row + 1, start_col)]  # Start one row below S
    split_count = 0
    
    # Track which positions have been processed to avoid infinite loops
    processed = set()
    
    while beams:
        new_beams = []
        
        for row, col in beams:
            # Skip if out of bounds
            if row < 0 or row >= rows or col < 0 or col >= cols:
                continue
            
            # Skip if already processed this position
            if (row, col) in processed:
                continue
            
            processed.add((row, col))
            
            # Check current position
            char = grid[row][col]
            
            if char == '^':
                # Hit a splitter - split into left and right
                split_count += 1
                
                # Add beams going down from left and right
                if col - 1 >= 0:
                    new_beams.append((row + 1, col - 1))
                if col + 1 < cols:
                    new_beams.append((row + 1, col + 1))
            else:
                # Empty space - continue downward
                new_beams.append((row + 1, col))
        
        beams = new_beams
    
    return split_count


def count_timelines(grid, start_row, start_col):
    """
    Count unique timelines in quantum tachyon splitting.
    Track the number of different paths (timelines) that reach each position.
    """
    rows = len(grid)
    cols = len(grid[0]) if rows > 0 else 0
    
    # Use dynamic programming: count paths to each position
    # paths[(row, col)] = number of distinct timelines to reach this position
    paths = {}
    paths[(start_row + 1, start_col)] = 1
    
    # Process row by row from top to bottom
    for current_row in range(start_row + 1, rows + 1):
        new_paths = {}
        
        for (row, col), count in list(paths.items()):
            if row != current_row:
                continue
            
            # If we've exited the bottom, count this as a final timeline
            if row >= rows:
                new_paths[(row, col)] = new_paths.get((row, col), 0) + count
                continue
            
            # Check if out of bounds horizontally - these also exit
            if col < 0 or col >= cols:
                new_paths[(row, col)] = new_paths.get((row, col), 0) + count
                continue
            
            char = grid[row][col]
            
            if char == '^':
                # Quantum split: particle takes both left and right paths
                # Each path inherits the count of timelines
                new_paths[(row + 1, col - 1)] = new_paths.get((row + 1, col - 1), 0) + count
                new_paths[(row + 1, col + 1)] = new_paths.get((row + 1, col + 1), 0) + count
            else:
                # Empty space: continue downward
                new_paths[(row + 1, col)] = new_paths.get((row + 1, col), 0) + count
        
        paths = new_paths
    
    # Sum all timelines that exited (bottom, left, or right edges)
    return sum(count for (row, col), count in paths.items() if row >= rows or col < 0 or col >= cols)


def main():
    # Parse the manifold
    grid = parse_manifold('input_day7.txt')
    
    # Find starting position
    start = find_start(grid)
    if not start:
        print("Error: Could not find starting position S")
        return
    
    start_row, start_col = start
    print(f"Starting position: row {start_row}, col {start_col}")
    
    # Part 1: Simulate beam propagation
    split_count = simulate_beam(grid, start_row, start_col)
    print(f"\nPart 1 - Total number of beam splits: {split_count}")
    
    # Part 2: Count unique timelines
    timeline_count = count_timelines(grid, start_row, start_col)
    print(f"Part 2 - Total number of unique timelines: {timeline_count}")


if __name__ == "__main__":
    main()
