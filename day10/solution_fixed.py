import re
from pulp import LpProblem, LpVariable, LpMinimize, lpSum, LpInteger, PULP_CBC_CMD
# Parsing
# -------------------------------
def parse_machine(line):
    """Parse une ligne de spécification de machine."""
    # Extract indicator lights pattern
    lights_match = re.search(r'\[([.#]+)\]', line)
    target = [1 if c == '#' else 0 for c in lights_match.group(1)] if lights_match else []

    # Extract button configurations
    buttons = []
    button_matches = re.findall(r'\(([0-9,]+)\)', line)
    for match in button_matches:
        indices = [int(x) for x in match.split(',')]
        buttons.append(indices)

    # Extract joltage requirements
    joltage_match = re.search(r'\{([0-9,]+)\}', line)
    joltages = [int(x) for x in joltage_match.group(1).split(',')] if joltage_match else []

    return target, buttons, joltages

# -------------------------------
# Part 1: Lights (bruteforce)
# -------------------------------
def solve_lights_bruteforce(target, buttons):
    n_lights = len(target)
    n_buttons = len(buttons)
    min_presses = float('inf')

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

# -------------------------------
# Part 2: Joltage (ILP)
# -------------------------------
def solve_joltage_ilp(joltages, buttons):
    n_buttons = len(buttons)
    n_counters = len(joltages)

    # Définir le problème
    prob = LpProblem("MinButtonPresses", LpMinimize)
    x = [LpVariable(f"x{i}", lowBound=0, cat=LpInteger) for i in range(n_buttons)]

    # Fonction objectif
    prob += lpSum(x)

    # Contraintes
    for counter_idx in range(n_counters):
        prob += lpSum(x[btn_idx] for btn_idx, btn in enumerate(buttons) if counter_idx in btn) == joltages[counter_idx]

    # Résolution
    solver = PULP_CBC_CMD(msg=0)
    status = prob.solve(solver)

    if prob.status != 1:
        return None

    return sum(int(x[i].value()) for i in range(n_buttons))

# -------------------------------
# Main
# -------------------------------
def main():
    # Test examples
    examples = [
        "[.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}",
        "[...#.] (0,2,3,4) (2,3) (0,4) (0,1,2) (1,2,3,4) {7,5,12,7,2}",
        "[.###.#] (0,1,2,3,4) (0,3,4) (0,1,2,4,5) (1,2) {10,11,11,5,10,5}"
    ]

    print("=== Tests Part 1 (lights) ===")
    total_test = 0
    for i, example in enumerate(examples, 1):
        target, buttons, _ = parse_machine(example)
        result = solve_lights_bruteforce(target, buttons)
        print(f"Example {i} -> {result}")
        total_test += result
    print(f"Total expected 7, got: {total_test}\n")

    print("=== Tests Part 2 (joltage) ===")
    total_test_p2 = 0
    for i, example in enumerate(examples, 1):
        _, buttons, joltages = parse_machine(example)
        result = solve_joltage_ilp(joltages, buttons)
        print(f"Example {i} -> {result}")
        total_test_p2 += result if result is not None else 0
    print(f"Total expected 33, got: {total_test_p2}\n")

    # Solve real input
    try:
        with open('input_day10.txt', 'r') as f:
            lines = [line.strip() for line in f if line.strip()]

        # Part 1
        total_presses_p1 = 0
        machines_solved_p1 = 0
        for i, line in enumerate(lines, 1):
            target, buttons, _ = parse_machine(line)
            result = solve_lights_bruteforce(target, buttons)
            if result is not None:
                total_presses_p1 += result
                machines_solved_p1 += 1
        print(f"Part1: solved {machines_solved_p1} machines, total presses = {total_presses_p1}")

        # Part 2
        total_presses_p2 = 0
        machines_solved_p2 = 0
        for i, line in enumerate(lines, 1):
            _, buttons, joltages = parse_machine(line)
            result = solve_joltage_ilp(joltages, buttons)
            if result is not None:
                total_presses_p2 += result
                machines_solved_p2 += 1
            else:
                print(f"Part2: Machine {i} has no solution!")
        print(f"Part2: solved {machines_solved_p2} machines, total presses = {total_presses_p2}")

    except FileNotFoundError:
        print("input_day10.txt not found. Please download your puzzle input.")

if __name__ == "__main__":
    main()
