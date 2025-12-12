#!/usr/bin/env python3
"""
Advent of Code 2025 - Day 12
Optimized solver using bitmasks + backtracking with pruning.

Usage:
    python3 solution.py
Reads 'input.txt' in the current folder (format described in the puzzle).
"""

from functools import lru_cache
from collections import defaultdict, Counter
import sys

# -------------------------
# Parsing utilities
# -------------------------
def read_input(filename='input.txt'):
    raw = open(filename, 'r', encoding='utf-8').read().strip().splitlines()
    # split into shapes block and regions block
    shapes = {}
    i = 0
    n = len(raw)
    # parse shapes: lines like "0:" then shape rows until blank
    while i < n:
        line = raw[i].strip()
        if line == '':
            i += 1
            continue
        if ':' in line and line.endswith(':') and line.split(':')[0].isdigit():
            idx = int(line.split(':')[0])
            i += 1
            rows = []
            while i < n and raw[i].strip() != '':
                rows.append(raw[i].rstrip('\n'))
                i += 1
            # normalize rows (they may include '.' and '#')
            # remove any leading/trailing spaces
            rows = [r.strip() for r in rows if r.strip() != '']
            shapes[idx] = rows
            continue
        # otherwise break: regions start now
        break

    # parse remaining lines as regions
    regions = []
    # find first region line index
    # continue from current i
    while i < n:
        line = raw[i].strip()
        if line == '':
            i += 1
            continue
        # lines like "12x5: 1 0 1 0 2 2"
        if ':' in line:
            left, right = line.split(':', 1)
            dims = left.strip()
            if 'x' not in dims:
                i += 1
                continue
            w, h = [int(x) for x in dims.split('x')]
            counts = [int(x) for x in right.strip().split()]
            regions.append((w, h, counts))
        i += 1

    return shapes, regions

# -------------------------
# Geometry helpers
# -------------------------
def shape_to_cells(shape_rows):
    """Convert shape display (list of strings) to set of (r,c) cells where char == '#'."""
    cells = []
    for r, row in enumerate(shape_rows):
        for c, ch in enumerate(row):
            if ch == '#':
                cells.append((r, c))
    return cells

def normalize_cells(cells):
    """Translate so min r,min c becomes (0,0) and return tuple sorted."""
    if not cells:
        return tuple()
    minr = min(r for r,c in cells)
    minc = min(c for r,c in cells)
    norm = tuple(sorted(((r - minr, c - minc) for r,c in cells)))
    return norm

def rotate_cells(cells):
    """Rotate 90 degrees clockwise around origin on grid: (r,c) -> (c, -r) then normalize."""
    # For integer grid it's simpler to map (r,c) -> (c, -r), but we'll then translate to positives.
    rotated = [ (c, -r) for r,c in cells ]
    return normalize_cells(rotated)

def flip_cells(cells):
    """Flip horizontally: (r,c) -> (r, -c) then normalize."""
    flipped = [ (r, -c) for r,c in cells ]
    return normalize_cells(flipped)

def all_orientations(cells):
    """Return set of all unique orientations (rotations + flips) as normalized tuples."""
    ori = set()
    cur = normalize_cells(cells)
    for _ in range(4):
        cur = rotate_cells(cur)
        ori.add(cur)
        ori.add(flip_cells(cur))
    # normalize each orientation to positive coordinates starting at 0
    return sorted(ori)

# -------------------------
# Bitmask board helpers
# -------------------------
def placement_bitmask(cells, w, h, top, left):
    """
    Given normalized cells (list of (r,c)), board width w and height h,
    and top,left placement, return integer bitmask with bits set for occupied cells.
    Bit indexing: row-major: bit index = r * w + c
    """
    mask = 0
    for r, c in cells:
        rr = top + r
        cc = left + c
        if rr < 0 or rr >= h or cc < 0 or cc >= w:
            return None
        idx = rr * w + cc
        mask |= (1 << idx)
    return mask

# -------------------------
# Precompute placements per shape per region
# -------------------------
def compute_placements_for_shape_in_region(shape_cells, w, h):
    """
    For a normalized shape (tuple of (r,c)), compute all placements bitmasks on a w x h board.
    Returns list of bitmasks.
    """
    placements = []
    # compute shape bounds
    maxr = max(r for r,c in shape_cells)
    maxc = max(c for r,c in shape_cells)
    for top in range(0, h - maxr):
        for left in range(0, w - maxc):
            mask = placement_bitmask(shape_cells, w, h, top, left)
            if mask is not None:
                placements.append(mask)
    return placements

# -------------------------
# Region solver
# -------------------------
def can_fill_region(w, h, shape_orientations, counts, timeout=None):
    """
    shape_orientations: dict shape_idx -> list of orientation-tuples (each orientation: tuple of (r,c))
    counts: list of counts per shape_idx (length equals number of shape indices)
    Returns True if region can be filled, False otherwise.
    """
    # total area check
    total_cells_needed = 0
    area_per_shape = {}
    for idx, oris in shape_orientations.items():
        if not oris:
            return False
        # area is number of cells in any orientation (all same)
        area_per_shape[idx] = len(oris[0])
    for idx, cnt in enumerate(counts):
        total_cells_needed += cnt * area_per_shape[idx]
    if total_cells_needed > w * h:
        return False

    # Precompute placements lists for each shape index (for the region)
    placements_per_shape = {}
    for idx, oris in shape_orientations.items():
        placements = []
        # for each orientation, compute placements
        for ori in oris:
            placements.extend(compute_placements_for_shape_in_region(ori, w, h))
        # deduplicate
        placements = sorted(set(placements))
        placements_per_shape[idx] = placements

        if counts[idx] > 0 and len(placements) == 0:
            # a required shape has no possible placement -> impossible
            return False

    # Expand multiset of required shapes into list of shape indices to place
    # but we will keep grouped by shape index and choose placements accordingly.
    # Build a list of "instances" with reference to shape idx, but ordering matters: choose shapes
    # with fewer placements first => reduce branching
    instances = []
    for idx, cnt in enumerate(counts):
        for _ in range(cnt):
            instances.append(idx)
    # order instances by placements-per-shape (ascending)
    instances.sort(key=lambda si: len(placements_per_shape[si]))

    # quick heuristic: if any instance has zero placements -> impossible
    for si in instances:
        if len(placements_per_shape[si]) == 0:
            return False

    # Precompute total area remaining after k placements for pruning
    # We'll also use a simple memoization by (pos, occupied_mask) but occupied_mask could be large.
    # To decrease memo size, we memo only by (pos, lowbits) where lowbits is truncated mask of first L bits.
    # However for simplicity and because Python ints are hashable, we'll memo full masks but with a cap on memo size.

    target_area = w * h

    sys.setrecursionlimit(10000)
    memo = set()
    placements_lists = placements_per_shape

    # compute union of all placements for quick impossible-check? skip

    # ordering of instances done; we try backtracking
    # to help pruning, we compute remaining area requirement at each pos
    remaining_area_from_pos = [0] * (len(instances) + 1)
    for i in range(len(instances)-1, -1, -1):
        remaining_area_from_pos[i] = remaining_area_from_pos[i+1] + area_per_shape[instances[i]]

    # recursion
    def backtrack(pos, occupied):
        # pos: next instance index to place
        if pos == len(instances):
            # all placed
            return True
        # pruning: if free cells (target_area - bits set in occupied) < remaining required area => impossible
        free_cells = target_area - occupied.bit_count()
        if free_cells < remaining_area_from_pos[pos]:
            return False

        key = (pos, occupied)
        if key in memo:
            return False

        si = instances[pos]
        for pmask in placements_lists[si]:
            # if placement overlaps, skip
            if (pmask & occupied) != 0:
                continue
            # place
            if backtrack(pos+1, occupied | pmask):
                return True

        memo.add(key)
        return False

    return backtrack(0, 0)

# -------------------------
# Main solver
# -------------------------
def solve_all(shapes_raw, regions):
    # Precompute normalized orientations for all shapes
    # shapes_raw: dict idx -> list of strings
    shape_orientations = {}
    for idx, rows in shapes_raw.items():
        cells = shape_to_cells(rows)
        # normalize and compute all orientations
        all_ori = all_orientations(cells)
        # store as list of list-of-(r,c)
        shape_orientations[idx] = [tuple(ori) for ori in all_ori]

    count_good = 0
    results = []
    for (w, h, counts) in regions:
        # counts is array with length maybe less than shapes count; ensure length matches number of shapes
        # The puzzle uses shape indices starting at 0 and contiguous.
        # Ensure counts length matches max shape index + 1:
        max_shape = max(shape_orientations.keys())
        # pad counts if needed
        if len(counts) <= max_shape:
            counts = counts + [0] * (max_shape + 1 - len(counts))
        # build per-region shape_orientations subset (only those present)
        per_region_oris = {idx: shape_orientations[idx] for idx in range(max_shape+1)}
        ok = can_fill_region(w, h, per_region_oris, counts)
        results.append(ok)
        if ok:
            count_good += 1
    return count_good, results

# -------------------------
# Entrypoint
# -------------------------
def main():
    shapes, regions = read_input('input.txt')
    good, results = solve_all(shapes, regions)
    print("Regions that can fit all presents:", good)

if __name__ == "__main__":
    main()