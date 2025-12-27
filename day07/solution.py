from typing import List, Tuple, Dict, Set
from dataclasses import dataclass
import sys
from collections import defaultdict

@dataclass(frozen=True)
class Position:
    """Représente une position dans la grille."""
    row: int
    col: int

class TachyonSimulator:
    """Simulateur de propagation de tachyon dans une variété quantique."""
    
    def __init__(self, grid: List[str]):
        """Initialise le simulateur avec une grille donnée."""
        self.grid = grid
        self.rows = len(grid)
        self.cols = len(grid[0]) if self.rows > 0 else 0
        self.start_pos = self._find_start()
        
    def _find_start(self) -> Position:
        """Trouve la position de départ 'S' dans la grille.
        
        Returns:
            Position: La position (ligne, colonne) de 'S'
            
        Raises:
            ValueError: Si 'S' n'est pas trouvé dans la grille
        """
        for row_idx, row in enumerate(self.grid):
            if 'S' in row:
                return Position(row_idx, row.index('S'))
        raise ValueError("Position de départ 'S' non trouvée dans la grille")
    
    def is_valid_position(self, pos: Position) -> bool:
        """Vérifie si une position est valide dans la grille."""
        return (0 <= pos.row < self.rows and 
                0 <= pos.col < self.cols)
    
    def count_beam_splits(self) -> int:
        """Compte le nombre total de divisions de faisceau (Partie 1).
        
        Returns:
            int: Nombre total de divisions de faisceau
        """
        if not self.start_pos:
            return 0
            
        beams = [Position(self.start_pos.row + 1, self.start_pos.col)]
        processed = set()
        split_count = 0
        
        while beams:
            new_beams = []
            
            for pos in beams:
                if not self.is_valid_position(pos) or pos in processed:
                    continue
                    
                processed.add(pos)
                char = self.grid[pos.row][pos.col]
                
                if char == '^':
                    # Division du faisceau
                    split_count += 1
                    left = Position(pos.row + 1, pos.col - 1)
                    right = Position(pos.row + 1, pos.col + 1)
                    
                    if self.is_valid_position(left):
                        new_beams.append(left)
                    if self.is_valid_position(right):
                        new_beams.append(right)
                else:
                    # Déplacement vers le bas
                    new_beams.append(Position(pos.row + 1, pos.col))
            
            beams = new_beams
        
        return split_count
    
    def count_timelines(self) -> int:
        """Compte le nombre total d'univers parallèles (Partie 2).
        
        Returns:
            int: Nombre total de chronologies uniques
        """
        if not self.start_pos:
            return 0
            
        # Dictionnaire des chemins: (row, col) -> nombre de chemins
        paths = defaultdict(int)
        start = Position(self.start_pos.row + 1, self.start_pos.col)
        paths[start] = 1
        
        for current_row in range(self.start_pos.row + 1, self.rows + 1):
            new_paths = defaultdict(int)
            
            for pos, count in paths.items():
                if pos.row != current_row:
                    continue
                    
                # Vérifie si on sort des limites
                if not (0 <= pos.col < self.cols) or pos.row >= self.rows:
                    new_paths[pos] += count
                    continue
                
                char = self.grid[pos.row][pos.col]
                
                if char == '^':
                    # Division quantique
                    left = Position(pos.row + 1, pos.col - 1)
                    right = Position(pos.row + 1, pos.col + 1)
                    new_paths[left] += count
                    new_paths[right] += count
                else:
                    # Déplacement vers le bas
                    new_paths[Position(pos.row + 1, pos.col)] += count
            
            paths = new_paths
        
        # Compte tous les chemins qui sortent de la grille
        return sum(
            count 
            for pos, count in paths.items() 
            if pos.row >= self.rows or not (0 <= pos.col < self.cols)
        )

def main() -> None:
    """Fonction principale."""
    if len(sys.argv) != 2:
        print(f"Utilisation: {sys.argv[0]} <fichier_entrée>", file=sys.stderr)
        sys.exit(1)
        
    filename = sys.argv[1]
    
    try:
        # Lecture du fichier d'entrée
        with open(filename, 'r') as f:
            grid = [line.strip() for line in f if line.strip()]
            
        if not grid:
            print("Erreur: La grille est vide.", file=sys.stderr)
            sys.exit(1)
            
        # Création du simulateur
        simulator = TachyonSimulator(grid)
        
        # Partie 1: Nombre de divisions de faisceau
        split_count = simulator.count_beam_splits()
        print(f"Partie 1 - Nombre de divisions de faisceau: {split_count}")
        
        # Partie 2: Nombre total de chronologies uniques
        timeline_count = simulator.count_timelines()
        print(f"Partie 2 - Nombre total de chronologies: {timeline_count}")
        
    except FileNotFoundError:
        print(f"Erreur: Le fichier {filename} est introuvable.", file=sys.stderr)
        sys.exit(1)
    except ValueError as e:
        print(f"Erreur: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Erreur inattendue: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()