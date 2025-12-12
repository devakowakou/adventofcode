#!/usr/bin/env python3
"""
solution.py - Day 12 solver (Advent of Code 2025)
Uses Dancing Links (Algorithm X) to decide whether each region can be exactly filled.

Usage:
    python3 solution.py

Input: input.txt in the same folder (format described by the puzzle).
Output: prints the number of regions that can fit all presents and per-region result.

Notes:
- TIMEOUT_PER_REGION controls how many seconds we allow DLX to try per region.
- This script finds existence only (stops when first solution is found).
"""

import re
import time
import sys
from collections import defaultdict
from multiprocessing import Process, Queue

# --------- Configuration ----------
TIMEOUT_PER_REGION = 8.0  # seconds per region (adjust if you want longer)
# ---------------------------------

# --------------------------
# Parsing functions
# --------------------------
def parse_input(path='input.txt'):
    lines = open(path, 'r', encoding='utf-8').read().splitlines()
    shapes = {}
    i = 0
    n = len(lines)

    # parse shapes
    while i < n:
        line = lines[i].strip()
        if line == '':
            i += 1
            continue
        m = re.match(r'^(\d+):\s*$', line)
        if not m:
            break
        idx = int(m.group(1))
        i += 1
        rows = []
        while i < n and lines[i].strip() != '':
            rows.append(lines[i].rstrip('\n'))
            i += 1
        shapes[idx] = [r.rstrip() for r in rows if r.strip() != '']
    # parse regions
    regions = []
    while i < n:
        line = lines[i].strip()
        i += 1
        if not line:
            continue
        m = re.match(r'^(\d+)x(\d+):\s*(.*)$', line)
        if not m:
            continue
        w = int(m.group(1)); h = int(m.group(2))
        counts = [int(x) for x in m.group(3).split() if x != '']
        regions.append((w, h, counts))
    return shapes, regions

# --------------------------
# Geometry helpers
# --------------------------
def shape_to_cells(rows):
    cells = []
    for r, row in enumerate(rows):
        for c, ch in enumerate(row):
            if ch == '#':
                cells.append((r, c))
    return cells

def normalize(cells):
    if not cells:
        return tuple()
    minr = min(r for r,c in cells)
    minc = min(c for r,c in cells)
    return tuple(sorted(((r - minr, c - minc) for r,c in cells)))

def rotate(cells):
    # (r,c) -> (c, -r)
    rotated = [(c, -r) for r,c in cells]
    return normalize(rotated)

def flip(cells):
    flipped = [(r, -c) for r,c in cells]
    return normalize(flipped)

def all_orientations(cells):
    s = set()
    cur = normalize(cells)
    for _ in range(4):
        cur = rotate(cur)
        s.add(cur)
        s.add(flip(cur))
    # return canonical sorted list (tuples of (r,c))
    return sorted(s)

def placement_mask(cells, w, h, top, left):
    mask = 0
    for r,c in cells:
        rr = top + r; cc = left + c
        if rr < 0 or rr >= h or cc < 0 or cc >= w:
            return None
        idx = rr * w + cc
        mask |= (1 << idx)
    return mask

def all_placements_for_orientation(ori, w, h):
    maxr = max(r for r,c in ori)
    maxc = max(c for r,c in ori)
    placements = []
    for top in range(0, h - maxr):
        for left in range(0, w - maxc):
            pm = placement_mask(ori, w, h, top, left)
            if pm is not None:
                placements.append(pm)
    return placements

# --------------------------
# Dancing Links (DLX) minimal implementation
# We use sparse representation: columns are integers 0..m-1
# Rows are lists of column indices that the row covers.
# We'll implement a classic DLX with arrays (pointer-like) for speed.
# We stop at first solution found.
# --------------------------

class DLX:
    def __init__(self, n_cols, rows):
        """
        n_cols: number of columns
        rows: list of lists (columns covered by each row)
        """
        self.n_cols = n_cols
        self.rows = rows
        # Build column -> rows index mapping (for heuristics)
        self.col_rows = [[] for _ in range(n_cols)]
        for r_idx, row in enumerate(rows):
            for c in row:
                self.col_rows[c].append(r_idx)
        # active sets
        self.col_active = [True] * n_cols
        self.row_active = [True] * len(rows)
        self.solution = []
        self.found = False

    def choose_column(self):
        # heuristic: choose active column with minimal remaining rows (MRV)
        best = -1
        best_count = 10**9
        for c in range(self.n_cols):
            if not self.col_active[c]:
                continue
            # count active rows that cover c
            cnt = 0
            for r in self.col_rows[c]:
                if self.row_active[r]:
                    # also ensure all columns in that row are active?
                    cnt += 1
            if cnt < best_count:
                best_count = cnt
                best = c
                if cnt <= 1:
                    break
        return best

    def cover(self, c):
        # deactivate column c and all rows intersecting it
        self.col_active[c] = False
        impacted_rows = []
        for r in self.col_rows[c]:
            if not self.row_active[r]:
                continue
            # deactivate row r
            self.row_active[r] = False
            impacted_rows.append(r)
        return impacted_rows

    def uncover_rows(self, rows_list):
        # re-activate given rows
        for r in rows_list:
            self.row_active[r] = True

    def uncover(self, c, rows_list):
        # reactivate column and rows
        self.col_active[c] = True
        self.uncover_rows(rows_list)

    def search(self, depth=0, max_nodes=10_000_000):
        # If all columns inactive -> solution found
        if all(not a for a in self.col_active):
            self.found = True
            return True
        c = self.choose_column()
        if c == -1:
            # no column available but not all inactive => fail
            return False
        # if no rows cover c -> dead end
        rows_covering = [r for r in self.col_rows[c] if self.row_active[r]]
        if not rows_covering:
            return False

        # Try each row that covers c
        for r in rows_covering:
            # select row r: deactivate all columns this row covers and rows intersecting them
            covered_cols = self.rows[r]
            # Save impacted rows per column
            impacted_per_col = {}
            # For each column in the row, cover it
            for col in covered_cols:
                impacted = self.cover(col)
                impacted_per_col[col] = impacted
            self.solution.append(r)
            # Recurse
            if self.search(depth+1):
                return True
            # backtrack
            self.solution.pop()
            # uncover columns in reverse order
            for col in reversed(covered_cols):
                self.uncover(col, impacted_per_col[col])
        return False

# --------------------------
# Convert region -> exact cover rows
# Columns scheme:
#   0..(w*h-1): board cells (row-major)
#   w*h .. w*h + total_instances -1 : one column per instance (to enforce counts)
# Rows:
#   for each instance id and for each placement of the corresponding shape: row = [cell_cols..., instance_col]
# --------------------------
def build_exact_cover_for_region(w, h, shape_oris, counts):
    """
    shape_oris: dict idx -> list of orientation tuples (r,c)
    counts: list of counts per shape idx
    Returns: n_cols, rows_list
    """
    max_shape = max(shape_oris.keys())
    # pad counts
    if len(counts) <= max_shape:
        counts = counts + [0] * (max_shape + 1 - len(counts))
    # compute areas and quick check
    area_per_shape = {idx: len(shape_oris[idx][0]) for idx in shape_oris}
    total_cells_needed = sum(counts[idx] * area_per_shape.get(idx, 0) for idx in range(max_shape+1))
    if total_cells_needed > w * h:
        return None, None  # impossible

    # compute placements per shape
    placements_per_shape = {}
    for idx, oris in shape_oris.items():
        placements = set()
        for ori in oris:
            pls = all_placements_for_orientation(ori, w, h)
            for pm in pls:
                placements.add(pm)
        placements_per_shape[idx] = sorted(placements)
        if counts[idx] > 0 and len(placements_per_shape[idx]) == 0:
            return None, None  # impossible

    # Build columns: board cells first
    cell_cols = w * h
    # Build instance columns: create a unique column for each required piece instance
    instance_cols = []
    instance_index = 0
    instance_map = []  # list of (shape_idx)
    for idx, cnt in enumerate(counts):
        for k in range(cnt):
            instance_map.append(idx)
            instance_index += 1
    total_cols = cell_cols + len(instance_map)
    # Now build rows
    rows = []
    # For each instance (with id j and shape idx s) add rows for each placement of shape s
    for inst_id, sidx in enumerate(instance_map):
        inst_col = cell_cols + inst_id
        for pm in placements_per_shape[sidx]:
            # convert pm bitmask into list of cell columns covered
            cells_covered = []
            bitmask = pm
            idxbit = 0
            while bitmask:
                if bitmask & 1:
                    cells_covered.append(idxbit)
                bitmask >>= 1; idxbit += 1
            row = cells_covered + [inst_col]
            rows.append(row)
    if len(rows) == 0:
        return None, None
    return total_cols, rows

# --------------------------
# Worker wrapper (timeout-friendly)
# --------------------------
def region_worker(idx, w, h, counts, shape_oris, q):
    """Worker invoked in separate process."""
    try:
        ncols, rows = build_exact_cover_for_region(w, h, shape_oris, counts)
        if ncols is None:
            q.put((idx, False))
            return
        dlx = DLX(ncols, rows)
        ok = dlx.search()
        q.put((idx, bool(ok)))
    except Exception as e:
        q.put((idx, None))

# --------------------------
# Main entrypoint
# --------------------------
def main():
    shapes_raw, regions = parse_input('input.txt')
    # precompute orientations
    shape_oris = {}
    for idx, rows in shapes_raw.items():
        cells = shape_to_cells(rows)
        shape_oris[idx] = all_orientations(cells)

    print(f"Shapes loaded: {len(shape_oris)}; Regions to test: {len(regions)}")
    total_ok = 0
    results = []
    for rid, (w, h, counts) in enumerate(regions):
        # pad counts to max shape index
        max_shape = max(shape_oris.keys())
        if len(counts) <= max_shape:
            counts = counts + [0] * (max_shape + 1 - len(counts))
        q = Queue()
        p = Process(target=region_worker, args=(rid, w, h, counts, shape_oris, q))
        start = time.time()
        p.start()
        p.join(TIMEOUT_PER_REGION)
        if p.is_alive():
            p.terminate()
            p.join()
            print(f"Region {rid} ({w}x{h}) -> TIMEOUT after {TIMEOUT_PER_REGION}s")
            results.append(None)
        else:
            if not q.empty():
                _rid, ok = q.get()
                print(f"Region {rid} ({w}x{h}) -> {ok} (time {time.time()-start:.2f}s)")
                results.append(ok)
                if ok:
                    total_ok += 1
            else:
                print(f"Region {rid} ({w}x{h}) -> ERROR (no result)")
                results.append(None)

    print(f"\nTotal regions that can fit: {total_ok} (timeouts marked as None)")

if __name__ == '__main__':
    main()
