def parse_manifold(text):
    """Parse the manifold diagram from text."""
    return text.strip().split('\n')


def find_start(grid):
    """Find the starting position S."""
    for row_idx, row in enumerate(grid):
        for col_idx, char in enumerate(row):
            if char == 'S':
                return (row_idx, col_idx)
    return None


def count_timelines(grid, start_row, start_col):
    """
    Count unique timelines in quantum tachyon splitting.
    Track the number of different ways to reach each final exit point.
    """
    rows = len(grid)
    cols = len(grid[0]) if rows > 0 else 0
    
    # Use dynamic programming: count paths to each position
    # paths[(row, col)] = number of distinct paths to reach this position
    paths = {}
    paths[(start_row + 1, start_col)] = 1
    
    # Process row by row
    for current_row in range(start_row + 1, rows + 1):
        new_paths = {}
        
        for (row, col), count in list(paths.items()):
            if row != current_row:
                continue
            
            # If we're at the exit row, this is a final position
            if row >= rows:
                new_paths[(row, col)] = new_paths.get((row, col), 0) + count
                continue
            
            # Check if out of bounds horizontally - these also count as exits
            if col < 0 or col >= cols:
                new_paths[(row, col)] = new_paths.get((row, col), 0) + count
                continue
            
            char = grid[row][col]
            
            if char == '^':
                # Split: go left and right
                new_paths[(row + 1, col - 1)] = new_paths.get((row + 1, col - 1), 0) + count
                new_paths[(row + 1, col + 1)] = new_paths.get((row + 1, col + 1), 0) + count
            else:
                # Continue down
                new_paths[(row + 1, col)] = new_paths.get((row + 1, col), 0) + count
        
        paths = new_paths
    
    # Sum all paths that reached the exit (any edge)
    return sum(count for (row, col), count in paths.items() if row >= rows or col < 0 or col >= cols)


# Test with the example
example = """.......S.......
...............
.......^.......
...............
......^.^......
...............
.....^.^.^.....
...............
....^.^...^....
...............
...^.^...^.^...
...............
..^...^.....^..
...............
.^.^.^.^.^...^.
..............."""

grid = parse_manifold(example)
start = find_start(grid)
if start:
    result = count_timelines(grid, start[0], start[1])
    print(f"Example result: {result} (expected 40)")
