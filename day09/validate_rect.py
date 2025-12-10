# day9_validate_rect.py
import sys
from pathlib import Path

def load_points(path):
    pts = [tuple(map(int, l.split(','))) for l in Path(path).read_text().splitlines() if l.strip()]
    return pts

def edges_from_points(pts):
    edges = []
    n = len(pts)
    for i in range(n):
        x1,y1 = pts[i]; x2,y2 = pts[(i+1)%n]
        edges.append((x1,y1,x2,y2))
    return edges

def point_on_edge(x,y,edges):
    # check if integer tile center (x,y) lies on any edge segment (boundary)
    # A tile is "on edge" if its center equals a point on a horizontal/vertical edge
    for x1,y1,x2,y2 in edges:
        if x1 == x2:
            if x == x1 and min(y1,y2) <= y <= max(y1,y2):
                return True
        elif y1 == y2:
            if y == y1 and min(x1,x2) <= x <= max(x1,x2):
                return True
    return False

def point_in_polygon_evenodd(x, y, edges):
    # test center (x, y) with scanline cast at y+0.1 to avoid integer-edge issues
    scan_y = y + 0.1
    cnt = 0
    for x1,y1,x2,y2 in edges:
        # ignore horizontal edges in the intersection test
        if (y1 > scan_y) != (y2 > scan_y):
            # compute intersection x coordinate
            xi = x1 + (scan_y - y1) * (x2 - x1) / (y2 - y1)
            if xi > x:
                cnt += 1
    return (cnt % 2) == 1

def is_allowed_tile(x, y, red_set, edges):
    # allowed if red OR on boundary OR inside polygon (green)
    if (x,y) in red_set:
        return True
    if point_on_edge(x, y, edges):
        return True
    if point_in_polygon_evenodd(x, y, edges):
        return True
    return False

def main():
    if len(sys.argv) < 6:
        print("Usage: python3 day9_validate_rect.py input_day9.txt xmin ymin xmax ymax")
        return
    infile = sys.argv[1]
    xmin = int(sys.argv[2]); ymin = int(sys.argv[3]); xmax = int(sys.argv[4]); ymax = int(sys.argv[5])

    pts = load_points(infile)
    edges = edges_from_points(pts)
    red_set = set(pts)

    # check corners are red
    corners = [(xmin,ymin),(xmin,ymax),(xmax,ymin),(xmax,ymax)]
    corners_ok = all(c in red_set for c in [(xmin,ymin),(xmax,ymax)])
    print("Top-left", (xmin,ymax),"is red?", (xmin,ymax) in red_set)
    print("Bottom-right", (xmax,ymin),"is red?", (xmax,ymin) in red_set)
    print("Specified corners red (opposite):", (xmin,ymin) in red_set, (xmax,ymax) in red_set)
    if not ((xmin,ymin) in red_set and (xmax,ymax) in red_set):
        print("ERROR: Opposite corners are not both red -> invalid rectangle.")
        return

    # Validate every tile inside inclusive rectangle
    print("Validating interior tiles (this may take a bit for large rect)...")
    bad = None
    count = 0
    for y in range(ymin, ymax+1):
        for x in range(xmin, xmax+1):
            count += 1
            if not is_allowed_tile(x, y, red_set, edges):
                bad = (x,y)
                break
        if bad:
            break

    if bad:
        print("FOUND invalid tile inside rectangle at:", bad, "which is neither red nor green.")
    else:
        print("All", count, "tiles inside rectangle are allowed (red or green).")
        area = (xmax - xmin + 1) * (ymax - ymin + 1)
        print("Area:", area)

if __name__ == '__main__':
    main()
