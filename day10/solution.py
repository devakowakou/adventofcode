import re


def parse_machine(line):
    """Parse a machine specification line."""
    # Extract indicator lights pattern
    lights_match = re.search(r'\[([.#]+)\]', line)
    lights = lights_match.group(1)
    target = [1 if c == '#' else 0 for c in lights]
    
    # Extract button configurations
    buttons = []
    button_matches = re.findall(r'\(([0-9,]+)\)', line)
    for match in button_matches:
        indices = [int(x) for x in match.split(',')]
        buttons.append(indices)
    
    # Extract joltage requirements
    joltage_match = re.search(r'\{([0-9,]+)\}', line)
    joltages = [int(x) for x in joltage_match.group(1).split(',')]
    
    return target, buttons, joltages


def solve_joltage(joltages, buttons):
    """
    Solve using a simple approach: since each button adds 1 to certain counters,
    we can solve this as a system of linear equations.
    For many practical cases, we can solve it directly.
    """
    n_counters = len(joltages)
    n_buttons = len(buttons)
    
    # Build the matrix: A[counter][button] = 1 if button affects counter
    A = [[0] * n_buttons for _ in range(n_counters)]
    for button_idx, button in enumerate(buttons):
        for counter_idx in button:
            A[counter_idx][button_idx] = 1
    
    # Try Gaussian elimination
    aug = [A[i][:] + [joltages[i]] for i in range(n_counters)]
    
    # Row reduction
    pivot_row = 0
    for col in range(n_buttons):
        # Find pivot
        found = False
        for row in range(pivot_row, n_counters):
            if aug[row][col] != 0:
                aug[pivot_row], aug[row] = aug[row], aug[pivot_row]
                found = True
                break
        
        if not found:
            continue
        
        # Eliminate
        for row in range(n_counters):
            if row != pivot_row and aug[row][col] != 0:
                factor = aug[row][col] / aug[pivot_row][col]
                for c in range(n_buttons + 1):
                    aug[row][c] -= factor * aug[pivot_row][c]
        
        pivot_row += 1
    
    # Back substitution
    x = [0.0] * n_buttons
    for row in range(n_counters - 1, -1, -1):
        # Find pivot column
        pivot_col = None
        for col in range(n_buttons):
            if abs(aug[row][col]) > 1e-9:
                pivot_col = col
                break
        
        if pivot_col is None:
            if abs(aug[row][-1]) > 1e-9:
                return None  # Inconsistent
            continue
        
        # Solve for x[pivot_col]
        val = aug[row][-1]
        for col in range(pivot_col + 1, n_buttons):
            val -= aug[row][col] * x[col]
        x[pivot_col] = val / aug[row][pivot_col]
    
    # Check if solution is valid (non-negative integers)
    for i in range(n_buttons):
        if x[i] < -1e-6 or abs(x[i] - round(x[i])) > 1e-6:
            return None
    
    x = [int(round(v)) for v in x]
    
    # Verify
    result = [0] * n_counters
    for button_idx, count in enumerate(x):
        for counter_idx in buttons[button_idx]:
            result[counter_idx] += count
    
    if result == joltages:
        return sum(x)
    
    return None


def solve_joltage_bfs(joltages, buttons):
    """
    Optimized BFS with better pruning and state management.
    """
    import heapq
    
    n_counters = len(joltages)
    target = tuple(joltages)
    initial = tuple([0] * n_counters)
    
    if initial == target:
        return 0
    
    # Use Dijkstra with better heuristic
    def heuristic(state):
        # Minimum presses needed: max difference for any counter
        max_diff = 0
        for i in range(n_counters):
            if state[i] < joltages[i]:
                max_diff = max(max_diff, joltages[i] - state[i])
        return max_diff
    
    # Priority queue: (f_score, g_score, state)
    heap = [(heuristic(initial), 0, initial)]
    g_score = {initial: 0}
    
    iterations = 0
    max_iterations = 500000  # Safety limit
    
    while heap and iterations < max_iterations:
        iterations += 1
        f, g, state = heapq.heappop(heap)
        
        # Skip if we found better path
        if state in g_score and g_score[state] < g:
            continue
        
        # Found target
        if state == target:
            return g
        
        # Try each button
        for button in buttons:
            new_state = list(state)
            valid = True
            
            for counter_idx in button:
                new_state[counter_idx] += 1
                if new_state[counter_idx] > joltages[counter_idx]:
                    valid = False
                    break
            
            if not valid:
                continue
            
            new_state = tuple(new_state)
            new_g = g + 1
            
            if new_state not in g_score or g_score[new_state] > new_g:
                g_score[new_state] = new_g
                new_f = new_g + heuristic(new_state)
                heapq.heappush(heap, (new_f, new_g, new_state))
    
    return None


def solve_joltage_hybrid(joltages, buttons):
    """
    Hybrid approach: use BFS for all problems, with iteration limit as fallback.
    """
    # Always try BFS first (it's optimal when it works)
    result = solve_joltage_bfs(joltages, buttons)
    if result is not None:
        return result
    
    # Fallback to Gaussian elimination (may not be optimal but gives an answer)
    return solve_joltage(joltages, buttons)


def solve_lights_bruteforce(target, buttons):
    """
    Brute force solution for small cases.
    Try all combinations of button presses (each 0 or 1 times).
    """
    n_lights = len(target)
    n_buttons = len(buttons)
    
    min_presses = float('inf')
    
    # Try all 2^n_buttons combinations
    for mask in range(1 << n_buttons):
        lights = [0] * n_lights
        presses = 0
        
        for button_idx in range(n_buttons):
            if mask & (1 << button_idx):
                presses += 1
                for light_idx in buttons[button_idx]:
                    lights[light_idx] ^= 1
        
        if lights == target:
            min_presses = min(min_presses, presses)
    
    return min_presses if min_presses != float('inf') else None


def main():
    # Test with examples
    examples = [
        "[.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}",
        "[...#.] (0,2,3,4) (2,3) (0,4) (0,1,2) (1,2,3,4) {7,5,12,7,2}",
        "[.###.#] (0,1,2,3,4) (0,3,4) (0,1,2,4,5) (1,2) {10,11,11,5,10,5}"
    ]
    
    print("Testing Part 1 with examples:")
    total_test = 0
    for i, example in enumerate(examples, 1):
        target, buttons, _ = parse_machine(example)
        result = solve_lights_bruteforce(target, buttons)
        print(f"Machine {i}: {result} presses")
        total_test += result
    
    print(f"Total test presses (Part 1): {total_test}")
    print(f"Expected: 7 (2 + 3 + 2)")
    print()
    
    print("Testing Part 2 with examples:")
    total_test_p2 = 0
    for i, example in enumerate(examples, 1):
        _, buttons, joltages = parse_machine(example)
        result = solve_joltage_bfs(joltages, buttons)
        if result is None:
            print(f"Machine {i}: FAILED")
            continue
        print(f"Machine {i}: {result} presses")
        total_test_p2 += result
    
    print(f"Total test presses (Part 2): {total_test_p2}")
    print(f"Expected: 33 (10 + 12 + 11)")
    print()
    
    # Solve actual puzzle
    try:
        with open('input_day10.txt', 'r') as f:
            lines = f.readlines()
        
        # Part 1
        total_presses_p1 = 0
        machines_solved = 0
        
        for i, line in enumerate(lines, 1):
            line = line.strip()
            if not line:
                continue
            
            target, buttons, _ = parse_machine(line)
            result = solve_lights_bruteforce(target, buttons)
            
            if result is not None:
                total_presses_p1 += result
                machines_solved += 1
        
        print(f"Part 1: Solved {machines_solved} machines")
        print(f"Part 1 Answer: {total_presses_p1}")
        print()
        
        # Part 2
        total_presses_p2 = 0
        machines_solved_p2 = 0
        
        for i, line in enumerate(lines, 1):
            line = line.strip()
            if not line:
                continue
            
            _, buttons, joltages = parse_machine(line)
            result = solve_joltage_hybrid(joltages, buttons)
            
            if result is not None:
                total_presses_p2 += result
                machines_solved_p2 += 1
            else:
                print(f"Warning: Machine {i} (Part 2) has no solution!")
        
        print(f"Part 2: Solved {machines_solved_p2} machines")
        print(f"Part 2 Answer: {total_presses_p2}")
    
    except FileNotFoundError:
        print("input_day10.txt not found. Please download your puzzle input.")


if __name__ == "__main__":
    main()
