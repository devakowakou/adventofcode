from typing import List, DefaultDict, Optional
from dataclasses import dataclass
from collections import defaultdict
import heapq
import sys

@dataclass(frozen=True, order=True)
class JunctionBox:
    """Représente une boîte de jonction avec des coordonnées 3D."""
    x: int
    y: int
    z: int

class UnionFind:
    """Structure de données Union-Find pour gérer les circuits connectés.
    
    Cette structure permet de regrouper efficacement des éléments en ensembles
    disjoints et de déterminer rapidement si deux éléments sont dans le même ensemble.
    """
    
    def __init__(self, size: int) -> None:
        """Initialise la structure avec un nombre donné d'éléments.
        
        Args:
            size: Nombre initial d'éléments (de 0 à size-1)
        """
        self.parent: List[int] = list(range(size))
        self.rank: List[int] = [0] * size
        self.size: List[int] = [1] * size
    
    def find(self, x: int) -> int:
        """Trouve le représentant de l'ensemble contenant x avec compression de chemin.
        
        Args:
            x: L'élément dont on cherche le représentant
            
        Returns:
            Le représentant de l'ensemble contenant x
        """
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])  # Compression de chemin
        return self.parent[x]
    
    def union(self, x: int, y: int) -> bool:
        """Fusionne les ensembles contenant x et y.
        
        Args:
            x: Premier élément
            y: Deuxième élément
            
        Returns:
            True si les ensembles ont été fusionnés, False si x et y étaient déjà dans le même ensemble
        """
        root_x = self.find(x)
        root_y = self.find(y)
        
        if root_x == root_y:
            return False  # Déjà dans le même ensemble
        
        # Union par rang
        if self.rank[root_x] < self.rank[root_y]:
            self.parent[root_x] = root_y
            self.size[root_y] += self.size[root_x]
        elif self.rank[root_x] > self.rank[root_y]:
            self.parent[root_y] = root_x
            self.size[root_x] += self.size[root_y]
        else:
            self.parent[root_y] = root_x
            self.size[root_x] += self.size[root_y]
            self.rank[root_x] += 1
        
        return True
    
    def get_circuit_sizes(self) -> List[int]:
        """Retourne la taille de chaque circuit.
        
        Returns:
            Une liste des tailles des circuits, triée par ordre décroissant
        """
        circuits: DefaultDict[int, int] = defaultdict(int)
        for i in range(len(self.parent)):
            root = self.find(i)
            circuits[root] = self.size[root]
        return sorted(circuits.values(), reverse=True)

def parse_input(filename: str) -> List[JunctionBox]:
    """Lit le fichier d'entrée et retourne la liste des boîtes de jonction.
    
    Args:
        filename: Chemin vers le fichier d'entrée
        
    Returns:
        Liste des boîtes de jonction lues depuis le fichier
    """
    boxes: List[JunctionBox] = []
    try:
        with open(filename, 'r') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    x, y, z = map(int, line.split(','))
                    boxes.append(JunctionBox(x, y, z))
                except ValueError as e:
                    print(f"Erreur de format dans la ligne: {line} - {e}", file=sys.stderr)
    except FileNotFoundError:
        print(f"Erreur: Le fichier {filename} est introuvable.", file=sys.stderr)
        sys.exit(1)
    
    return boxes

def solve_part1(filename: str, num_connections: int) -> int:
    """Résout la première partie du problème des boîtes de jonction.
    
    Connecte les 'num_connections' paires les plus proches et retourne
    le produit des tailles des trois plus grands circuits.
    
    Args:
        filename: Chemin vers le fichier d'entrée
        num_connections: Nombre de connexions à établir
        
    Returns:
        Le produit des tailles des trois plus grands circuits
    """
    boxes = parse_input(filename)
    n = len(boxes)
    
    if n < 3:
        print("Erreur: Au moins 3 boîtes sont nécessaires.", file=sys.stderr)
        sys.exit(1)
    
    # Création d'un tas des distances entre toutes les paires
    distances = []
    for i in range(n):
        for j in range(i + 1, n):
            dist = ((boxes[j].x - boxes[i].x)**2 + 
                   (boxes[j].y - boxes[i].y)**2 + 
                   (boxes[j].z - boxes[i].z)**2)
            heapq.heappush(distances, (dist, i, j))
    
    # Initialisation de la structure Union-Find
    uf = UnionFind(n)
    
    # Établissement des connexions
    connections_made = 0
    while connections_made < num_connections and distances:
        _, i, j = heapq.heappop(distances)
        if uf.union(i, j):
            connections_made += 1
    
    # Calcul du résultat
    circuit_sizes = uf.get_circuit_sizes()
    if len(circuit_sizes) < 3:
        print("Erreur: Moins de 3 circuits après connexion.", file=sys.stderr)
        return 0
    
    return circuit_sizes[0] * circuit_sizes[1] * circuit_sizes[2]

def solve_part2(filename: str) -> Optional[int]:
    """Résout la deuxième partie du problème des boîtes de jonction.
    
    Connecte les boîtes jusqu'à ce qu'elles forment un seul circuit.
    Retourne le produit des coordonnées X des deux dernières boîtes connectées.
    
    Args:
        filename: Chemin vers le fichier d'entrée
        
    Returns:
        Le produit des coordonnées X des deux dernières boîtes connectées, ou None si impossible
    """
    boxes = parse_input(filename)
    n = len(boxes)
    
    if n < 2:
        print("Erreur: Au moins 2 boîtes sont nécessaires.", file=sys.stderr)
        return None
    
    # Création d'un tas des distances entre toutes les paires
    distances = []
    for i in range(n):
        for j in range(i + 1, n):
            dist = ((boxes[j].x - boxes[i].x)**2 + 
                   (boxes[j].y - boxes[i].y)**2 + 
                   (boxes[j].z - boxes[i].z)**2)
            heapq.heappush(distances, (dist, i, j))
    
    # Initialisation de la structure Union-Find
    uf = UnionFind(n)
    last_connection: Optional[Tuple[int, int]] = None
    
    # Connexion jusqu'à ce qu'il n'y ait plus qu'un seul circuit
    while len(uf.get_circuit_sizes()) > 1 and distances:
        _, i, j = heapq.heappop(distances)
        if uf.union(i, j):
            last_connection = (i, j)
    
    if not last_connection:
        print("Aucune connexion n'a pu être établie.", file=sys.stderr)
        return None
    
    # Calcul du résultat
    i, j = last_connection
    return boxes[i].x * boxes[j].x

def main() -> None:
    """Fonction principale."""
    if len(sys.argv) != 2:
        print(f"Utilisation: {sys.argv[0]} <fichier_entrée>", file=sys.stderr)
        sys.exit(1)
    
    filename = sys.argv[1]
    
    # Partie 1
    print("=== Partie 1 ===")
    result1 = solve_part1(filename, 1000)
    print(f"Résultat Partie 1: {result1}")
    
    # Partie 2
    print("\n=== Partie 2 ===")
    result2 = solve_part2(filename)
    if result2 is not None:
        print(f"Résultat Partie 2: {result2}")

if __name__ == "__main__":
    main()