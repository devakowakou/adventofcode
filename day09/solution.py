from typing import List, Tuple, Set, Dict, Optional
from dataclasses import dataclass
import sys
from functools import lru_cache

@dataclass(frozen=True, order=True)
class Point:
    """Représente un point 2D avec des coordonnées entières."""
    x: int
    y: int

class RectangleFinder:
    """Classe pour trouver le plus grand rectangle dans une grille de points."""
    
    def __init__(self, red_tiles: List[Tuple[int, int]]):
        """Initialise le finder avec les tuiles rouges.
        
        Args:
            red_tiles: Liste des coordonnées (x, y) des tuiles rouges
        """
        self.red_tiles = [Point(x, y) for x, y in red_tiles]
        self.red_set = set(self.red_tiles)
        self.green_path: Set[Point] = set()
        self._build_green_path()
        self._interior_cache: Dict[Point, bool] = {}
    
    def _build_green_path(self) -> None:
        """Construit le chemin vert entre les tuiles rouges consécutives."""
        n = len(self.red_tiles)
        for i in range(n):
            p1 = self.red_tiles[i]
            p2 = self.red_tiles[(i + 1) % n]  # Connexion circulaire
            
            # Ajout des points entre p1 et p2 (inclus)
            if p1.x == p2.x:  # Ligne verticale
                y_min, y_max = sorted((p1.y, p2.y))
                for y in range(y_min, y_max + 1):
                    self.green_path.add(Point(p1.x, y))
            else:  # Ligne horizontale
                x_min, x_max = sorted((p1.x, p2.x))
                for x in range(x_min, x_max + 1):
                    self.green_path.add(Point(x, p1.y))
    
    @lru_cache(maxsize=None)
    def _is_inside_polygon(self, point: Point) -> bool:
        """Vérifie si un point est à l'intérieur du polygone formé par les tuiles rouges.
        
        Utilise l'algorithme du ray casting.
        """
        x, y = point.x, point.y
        n = len(self.red_tiles)
        inside = False
        
        j = n - 1
        for i in range(n):
            xi, yi = self.red_tiles[i].x, self.red_tiles[i].y
            xj, yj = self.red_tiles[j].x, self.red_tiles[j].y
            
            if ((yi > y) != (yj > y)) and (x < (xj - xi) * (y - yi) / (yj - yi) + xi):
                inside = not inside
            j = i
        
        return inside
    
    def is_green(self, point: Point) -> bool:
        """Vérifie si un point est vert (sur le chemin ou à l'intérieur)."""
        if point in self.green_path:
            return True
        if point in self._interior_cache:
            return self._interior_cache[point]
        
        result = self._is_inside_polygon(point)
        self._interior_cache[point] = result
        return result
    
    def find_largest_rectangle(self) -> Tuple[int, Optional[Tuple[Point, Point]]]:
        """Trouve le plus grand rectangle formé par deux tuiles rouges.
        
        Returns:
            Un tuple (aire, ((x1, y1), (x2, y2))) représentant l'aire et les coins du rectangle,
            ou (0, None) si aucun rectangle valide n'est trouvé.
        """
        n = len(self.red_tiles)
        max_area = 0
        best_pair = None
        
        # Génère toutes les paires de points
        for i in range(n):
            p1 = self.red_tiles[i]
            for j in range(i + 1, n):
                p2 = self.red_tiles[j]
                
                # Calcule les coins du rectangle
                min_x = min(p1.x, p2.x)
                max_x = max(p1.x, p2.x)
                min_y = min(p1.y, p2.y)
                max_y = max(p1.y, p2.y)
                
                # Calcule l'aire
                width = max_x - min_x + 1
                height = max_y - min_y + 1
                area = width * height
                
                # Passe à la suite si l'aire est trop petite
                if area <= max_area:
                    continue
                
                # Vérifie les bords du rectangle
                if not self._is_rectangle_valid(min_x, max_x, min_y, max_y):
                    continue
                
                # Met à jour le meilleur rectangle trouvé
                max_area = area
                best_pair = (p1, p2)
        
        return max_area, best_pair
    
    def _is_rectangle_valid(self, min_x: int, max_x: int, min_y: int, max_y: int) -> bool:
        """Vérifie si tous les points du rectangle sont valides (rouges ou verts)."""
        # Vérifie les bords supérieur et inférieur
        for x in range(min_x, max_x + 1):
            p1 = Point(x, min_y)
            p2 = Point(x, max_y)
            if p1 not in self.red_set and not self.is_green(p1):
                return False
            if p2 not in self.red_set and not self.is_green(p2):
                return False
        
        # Vérifie les bords gauche et droit (sans les coins déjà vérifiés)
        for y in range(min_y + 1, max_y):
            p1 = Point(min_x, y)
            p2 = Point(max_x, y)
            if p1 not in self.red_set and not self.is_green(p1):
                return False
            if p2 not in self.red_set and not self.is_green(p2):
                return False
        
        # Pour les grands rectangles, on échantillonne l'intérieur
        width = max_x - min_x + 1
        height = max_y - min_y + 1
        
        if width * height > 10000:  # Seuil pour l'échantillonnage
            step = max(1, int((width * height) ** 0.25))
            for x in range(min_x + 1, max_x, step):
                for y in range(min_y + 1, max_y, step):
                    p = Point(x, y)
                    if p not in self.red_set and not self.is_green(p):
                        return False
        
        return True

def parse_input(filename: str) -> List[Tuple[int, int]]:
    """Lit le fichier d'entrée et retourne les coordonnées des tuiles rouges.
    
    Args:
        filename: Chemin vers le fichier d'entrée
        
    Returns:
        Liste des coordonnées (x, y) des tuiles rouges
    """
    try:
        with open(filename, 'r') as f:
            return [tuple(map(int, line.strip().split(','))) 
                   for line in f if line.strip()]
    except FileNotFoundError:
        print(f"Erreur: Le fichier {filename} est introuvable.", file=sys.stderr)
        sys.exit(1)
    except ValueError as e:
        print(f"Erreur de format dans le fichier {filename}: {e}", file=sys.stderr)
        sys.exit(1)

def main() -> None:
    """Fonction principale."""
    if len(sys.argv) != 2:
        print(f"Utilisation: {sys.argv[0]} <fichier_entrée>", file=sys.stderr)
        sys.exit(1)
    
    filename = sys.argv[1]
    
    try:
        # Lecture des données d'entrée
        red_tiles = parse_input(filename)
        print(f"Nombre de tuiles rouges: {len(red_tiles)}")
        
        if len(red_tiles) < 3:
            print("Erreur: Au moins 3 tuiles rouges sont nécessaires pour former un polygone.", 
                  file=sys.stderr)
            sys.exit(1)
        
        # Création du finder et recherche du plus grand rectangle
        finder = RectangleFinder(red_tiles)
        max_area, best_pair = finder.find_largest_rectangle()
        
        # Affichage des résultats
        if best_pair:
            p1, p2 = best_pair
            print(f"\nPlus grand rectangle trouvé:")
            print(f"  Coin 1: ({p1.x}, {p1.y})")
            print(f"  Coin 2: ({p2.x}, {p2.y})")
            print(f"  Aire: {max_area}")
        else:
            print("\nAucun rectangle valide n'a été trouvé.")
            
    except Exception as e:
        print(f"Erreur: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()