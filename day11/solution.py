#!/usr/bin/env python3
"""
Advent of Code 2025 - Day 11
"""

def parse_input(filename='input.txt'):
    """Parse le fichier d'entrée"""
    with open(filename, 'r') as f:
        lines = f.read().strip().split('\n')
    return lines


def part1(data):
    """Résout la partie 1"""
    # TODO: Implémenter la solution
    return 0


def part2(data):
    """Résout la partie 2"""
    # TODO: Implémenter la solution
    return 0


def main():
    # Lecture des données
    data = parse_input()
    
    # Partie 1
    result1 = part1(data)
    print(f"Part 1: {result1}")
    
    # Partie 2
    result2 = part2(data)
    print(f"Part 2: {result2}")


if __name__ == "__main__":
    main()
