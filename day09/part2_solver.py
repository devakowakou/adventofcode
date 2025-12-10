# day9_part2_robust.py
# Robust part-two solver using canonical scanline intersections
import sys, math, bisect, time
from pathlib import Path
from collections import defaultdict

def load_points(path):
    return [tuple(map(int, l.split(','))) for l in Path(path).read_text().splitlines() if l.strip()]

def build_edges(points):
    n = len(points)
    return [(points[i][0], points[i][1], points[(i+1)%n][0], points[(i+1)%n][1]) for i in range(n)]

def scanline_intervals(edges, miny, maxy):
    row_interior = {}
    for y in range(miny, maxy+1):
        scan_y = y + 0.5
        xs = []
        for (x1,y1,x2,y2) in edges:
            # standard test: edge contributes if scan_y is strictly between the ys of its endpoints
            if (y1 > scan_y) != (y2 > scan_y):
                # avoid division by zero because we ensured (y1>scan_y)!=(y2>scan_y) so y2!=y1
                x = x1 + (scan_y - y1) * (x2 - x1) / (y2 - y1)
                xs.append(x)
            # horizontal edges will not satisfy the test and are ignored in intersections
        if not xs:
            continue
        xs.sort()
        ints = []
        # pair intersections: [xs[0], xs[1]), [xs[2], xs[3]), ...
        for i in range(0, len(xs)-1, 2):
            xl = xs[i]; xr = xs[i+1]
            # integer tile centers x such that xl < x+0.5 < xr  <=>  x in (xl-0.5, xr-0.5)
            left = math.ceil(xl - 0.5 + 1e-12)
            right = math.floor(xr - 0.5 - 1e-12)
            if left <= right:
                ints.append((left, right))
        if ints:
            row_interior[y] = ints
    return row_interior

def boundary_points(edges):
    row_boundary = defaultdict(list)
    for (x1,y1,x2,y2) in edges:
        if x1 == x2:
            x = x1
            ylo, yhi = (y1, y2) if y1 <= y2 else (y2, y1)
            for yy in range(ylo, yhi+1):
                row_boundary[yy].append(x)
        else:
            # horizontal edges — every integer x on the segment is boundary at that y
            y = y1
            xlo, xhi = (x1, x2) if x1 <= x2 else (x2, x1)
            for xx in range(xlo, xhi+1):
                row_boundary[y].append(xx)
    return row_boundary

def merge_intervals(ints):
    if not ints:
        return []
    ints.sort()
    merged = []
    c0,c1 = ints[0]
    for a,b in ints[1:]:
        if a <= c1 + 1:
            c1 = max(c1, b)
        else:
            merged.append((c0,c1)); c0,c1 = a,b
    merged.append((c0,c1))
    return merged

def build_allowed(row_interior, row_boundary, miny, maxy):
    row_allowed = {}
    for y in range(miny, maxy+1):
        ints = []
        if y in row_interior:
            ints.extend(row_interior[y])
        if y in row_boundary:
            for x in row_boundary[y]:
                ints.append((x,x))
        if not ints:
            continue
        row_allowed[y] = merge_intervals(ints)
    return row_allowed

def covered(intervals, a, b):
    i = bisect.bisect_right(intervals, (a, 10**30)) - 1
    if i >= 0:
        x0,x1 = intervals[i]
        if x0 <= a and x1 >= b:
            return True
    return False

def find_max(points, row_allowed):
    n = len(points)
    pairs = []
    for i in range(n):
        x1,y1 = points[i]
        for j in range(i+1, n):
            x2,y2 = points[j]
            if x1 == x2 or y1 == y2:
                continue
            xmin,xmax = sorted((x1,x2))
            ymin,ymax = sorted((y1,y2))
            area = (xmax - xmin + 1) * (ymax - ymin + 1)
            pairs.append((-area, xmin, xmax, ymin, ymax, (x1,y1),(x2,y2)))
    pairs.sort()
    best = 0; rect = None
    for negarea, xmin,xmax,ymin,ymax,p1,p2 in pairs:
        area = -negarea
        if area <= best: break
        ok = True
        for y in range(ymin, ymax+1):
            ints = row_allowed.get(y)
            if not ints or not covered(ints, xmin, xmax):
                ok = False; break
        if ok:
            best = area
            rect = (xmin,ymin,xmax,ymax,p1,p2)
            # can break since we go largest->smallest
            break
    return best, rect

def main():
    inpath = sys.argv[1] if len(sys.argv)>1 else 'input_day9.txt'
    pts = load_points(inpath)
    edges = build_edges(pts)
    miny = min(y for _,y in pts); maxy = max(y for _,y in pts)
    start = time.time()
    row_interior = scanline_intervals(edges, miny, maxy)
    row_boundary = boundary_points(edges)
    row_allowed = build_allowed(row_interior, row_boundary, miny, maxy)
    best, rect = find_max(pts, row_allowed)
    end = time.time()
    print("Best area:", best)
    print("Best rect:", rect)
    print("Time(s):", end - start)

if __name__ == '__main__':
    main()
