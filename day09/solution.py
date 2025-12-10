def parse_input(filename):
    """Parse the red tile coordinates from the input file."""
    tiles = []
    with open(filename, 'r') as f:
        for line in f:
            line = line.strip()
            if line:
                x, y = map(int, line.split(','))
                tiles.append((x, y))
    return tiles


def get_green_tiles(red_tiles):
    """
    Build the set of all green tiles on the path between red tiles.
    Return path tiles and a cached function to check if a point is green (path or interior).
    """
    green_path = set()
    n = len(red_tiles)
    
    # Add path tiles between consecutive red tiles
    for i in range(n):
        x1, y1 = red_tiles[i]
        x2, y2 = red_tiles[(i + 1) % n]  # Wraps around
        
        # Add tiles along the path (either horizontal or vertical line)
        if x1 == x2:  # Vertical line
            for y in range(min(y1, y2), max(y1, y2) + 1):
                green_path.add((x1, y))
        else:  # Horizontal line
            for x in range(min(x1, x2), max(x1, x2) + 1):
                green_path.add((x, y1))
    
    # Cache for interior point checks
    interior_cache = {}
    
    def is_inside_polygon(point, polygon):
        """Ray casting algorithm for point in polygon test (improved)."""
        x, y = point
        n = len(polygon)
        inside = False
        
        j = n - 1
        for i in range(n):
            xi, yi = polygon[i]
            xj, yj = polygon[j]
            
            if ((yi > y) != (yj > y)) and (x < (xj - xi) * (y - yi) / (yj - yi) + xi):
                inside = not inside
            j = i
        
        return inside
    
    def is_green(point):
        """Check if a point is green (on path or interior) with caching."""
        if point in green_path:
            return True
        if point in interior_cache:
            return interior_cache[point]
        result = is_inside_polygon(point, red_tiles)
        interior_cache[point] = result
        return result
    
    return green_path, is_green


def find_largest_rectangle(tiles):
    """
    Find the largest rectangle that can be formed by any two red tiles
    as opposite corners. The area is inclusive of both corners.
    """
    n = len(tiles)
    max_area = 0
    best_pair = None
    
    # Check all pairs of tiles
    for i in range(n):
        for j in range(i + 1, n):
            x1, y1 = tiles[i]
            x2, y2 = tiles[j]
            
            # Calculate rectangle area (inclusive of both corners)
            width = abs(x2 - x1) + 1
            height = abs(y2 - y1) + 1
            area = width * height
            
            if area > max_area:
                max_area = area
                best_pair = (tiles[i], tiles[j])
    
    return max_area, best_pair


def find_largest_rectangle_part2(red_tiles, green_path, is_green):
    """
    Find the largest rectangle using only red and green tiles.
    Check borders completely + sample interior strategically.
    """
    red_set = set(red_tiles)
    
    n = len(red_tiles)
    max_area = 0
    best_pair = None
    
    # Sort pairs by area (descending) to find large ones first
    pairs_with_area = []
    for i in range(n):
        for j in range(i + 1, n):
            x1, y1 = red_tiles[i]
            x2, y2 = red_tiles[j]
            area = (abs(x2 - x1) + 1) * (abs(y2 - y1) + 1)
            pairs_with_area.append((area, i, j))
    
    # Sort by area descending
    pairs_with_area.sort(reverse=True)
    
    print(f"Checking {len(pairs_with_area)} potential rectangles...")
    
    # Check pairs starting from largest
    for idx, (area, i, j) in enumerate(pairs_with_area):
        # Skip if this can't beat current max
        if area <= max_area:
            print(f"Stopping early at pair {idx}, remaining pairs too small")
            break
        
        if idx % 1000 == 0:
            print(f"Checked {idx} pairs, current max: {max_area}")
        
        x1, y1 = red_tiles[i]
        x2, y2 = red_tiles[j]
        
        min_x, max_x = min(x1, x2), max(x1, x2)
        min_y, max_y = min(y1, y2), max(y1, y2)
        
        width = max_x - min_x + 1
        height = max_y - min_y + 1
        
        # Strategy: Check borders first (fast reject), then sample interior
        valid = True
        
        # Check ALL border points
        # Top and bottom edges
        for x in range(min_x, max_x + 1):
            if (x, min_y) not in red_set and not is_green((x, min_y)):
                valid = False
                break
            if (x, max_y) not in red_set and not is_green((x, max_y)):
                valid = False
                break
        
        # Left and right edges (excluding corners)
        if valid:
            for y in range(min_y + 1, max_y):
                if (min_x, y) not in red_set and not is_green((min_x, y)):
                    valid = False
                    break
                if (max_x, y) not in red_set and not is_green((max_x, y)):
                    valid = False
                    break
        
        # Check interior points with adaptive sampling
        if valid:
            # For small rectangles, check everything
            if width * height <= 50000:
                for x in range(min_x + 1, max_x):
                    for y in range(min_y + 1, max_y):
                        if (x, y) not in red_set and not is_green((x, y)):
                            valid = False
                            break
                    if not valid:
                        break
            else:
                # For large rectangles, sample interior points in a grid
                # Use ~200 sample points
                sample_size = min(200, width * height // 1000)
                step_x = max(1, width // int(sample_size ** 0.5))
                step_y = max(1, height // int(sample_size ** 0.5))
                
                for x in range(min_x + 1, max_x, step_x):
                    for y in range(min_y + 1, max_y, step_y):
                        if (x, y) not in red_set and not is_green((x, y)):
                            valid = False
                            break
                    if not valid:
                        break
        
        if valid:
            max_area = area
            best_pair = (red_tiles[i], red_tiles[j])
            print(f"Found valid rectangle with area {max_area}: {best_pair}")
    
    return max_area, best_pair


def main():
    red_tiles = parse_input('input_day9.txt')
    print(f"Part 1:")
    print(f"Total red tiles: {len(red_tiles)}")
    
    max_area, best_pair = find_largest_rectangle(red_tiles)
    
    if best_pair:
        print(f"Largest rectangle area: {max_area}")
        print(f"Corners: {best_pair[0]} and {best_pair[1]}")
    
    print(f"Part 1 Answer: {max_area}")
    
    # Part 2
    print(f"\nPart 2:")
    print("Building green tiles...")
    green_path, is_green = get_green_tiles(red_tiles)
    print(f"Green path tiles: {len(green_path)}")
    
    max_area2, best_pair2 = find_largest_rectangle_part2(red_tiles, green_path, is_green)
    
    if best_pair2:
        print(f"Largest rectangle area (red/green only): {max_area2}")
        print(f"Corners: {best_pair2[0]} and {best_pair2[1]}")
    
    print(f"Part 2 Answer: {max_area2}")


if __name__ == "__main__":
    main()
