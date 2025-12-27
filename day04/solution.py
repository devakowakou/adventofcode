from typing import List
from dataclasses import dataclass

@dataclass(frozen=True)
class Position:
    """Représente une position dans la grille."""
    row: int
    col: int

    def __add__(self, other: 'Position') -> 'Position':
        return Position(self.row + other.row, self.col + other.col)

# Directions: N, NE, E, SE, S, SW, W, NW
DIRECTIONS = [
    Position(-1, 0), Position(-1, 1), Position(0, 1), Position(1, 1),
    Position(1, 0), Position(1, -1), Position(0, -1), Position(-1, -1)
]

class PaperRollGrid:
    """Classe pour gérer la grille de rouleaux de papier."""
    
    def __init__(self, grid: List[str]):
        self.grid = [list(row) for row in grid]
        self.rows = len(grid)
        self.cols = len(grid[0]) if self.rows > 0 else 0
    
    def is_valid_position(self, pos: Position) -> bool:
        """Vérifie si une position est valide dans la grille."""
        return 0 <= pos.row < self.rows and 0 <= pos.col < self.cols
    
    def get_adjacent_rolls_count(self, pos: Position) -> int:
        """Compte les rouleaux adjacents à une position."""
        return sum(
            1 for direction in DIRECTIONS
            if self.is_valid_position(new_pos := pos + direction) and
            self.grid[new_pos.row][new_pos.col] == '@'
        )
    
    def find_accessible_rolls(self) -> List[Position]:
        """Trouve tous les rouleaux accessibles (moins de 4 rouleaux adjacents)."""
        return [
            Position(row, col)
            for row in range(self.rows)
            for col in range(self.cols)
            if self.grid[row][col] == '@' and 
            self.get_adjacent_rolls_count(Position(row, col)) < 4
        ]
    
    def remove_rolls(self, positions: List[Position]) -> None:
        """Supprime les rouleaux aux positions données."""
        for pos in positions:
            self.grid[pos.row][pos.col] = '.'
    
    def count_rolls(self) -> int:
        """Compte le nombre total de rouleaux restants."""
        return sum(row.count('@') for row in self.grid)

def solve_part1(grid: List[str]) -> int:
    """Résout la partie 1: compte les rouleaux accessibles par chariot élévateur."""
    return len(PaperRollGrid(grid).find_accessible_rolls())

def solve_part2(grid: List[str]) -> int:
    """Résout la partie 2: compte le nombre total de rouleaux qui peuvent être enlevés."""
    paper_grid = PaperRollGrid(grid)
    total_removed = 0
    
    while True:
        accessible = paper_grid.find_accessible_rolls()
        if not accessible:
            break
        paper_grid.remove_rolls(accessible)
        total_removed += len(accessible)
    
    return total_removed

def main() -> None:
    """Fonction principale."""
    try:
        with open('input.txt', 'r') as f:
            grid = [line.strip() for line in f if line.strip()]
        
        if not grid:
            print("Erreur: La grille est vide.")
            return
        
        # Partie 1
        result_part1 = solve_part1(grid)
        print(f"Partie 1 - Rouleaux accessibles par chariot: {result_part1}")
        
        # Partie 2
        result_part2 = solve_part2(grid)
        print(f"Partie 2 - Total des rouleaux enlevables: {result_part2}")
        
    except FileNotFoundError:
        print("Erreur: Fichier 'input.txt' introuvable.")
    except Exception as e:
        print(f"Erreur lors du traitement: {str(e)}")

if __name__ == "__main__":
    main()