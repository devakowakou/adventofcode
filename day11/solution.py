"""
Advent of Code 2025 - Jour 11 : Réacteur
Solution optimisée avec typage statique et documentation complète
"""

from functools import lru_cache
from typing import Dict, List, Set, Tuple
import sys
from collections import defaultdict

# Type pour le graphe de connexions
Graph = Dict[str, List[str]]

def parse_input(filename: str) -> Graph:
    """Parse le fichier d'entrée et construit le graphe des connexions.
    
    Args:
        filename: Chemin vers le fichier d'entrée
        
    Returns:
        Un dictionnaire représentant le graphe des connexions
        
    Raises:
        FileNotFoundError: Si le fichier n'existe pas
        ValueError: Si le format du fichier est invalide
    """
    graph: Graph = defaultdict(list)
    
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            for line_num, line in enumerate(f, 1):
                line = line.strip()
                if not line:
                    continue
                    
                try:
                    node, outs = line.split(':', 1)
                    node = node.strip()
                    outputs = [out.strip() for out in outs.split() if out.strip()]
                    
                    if not node:
                        raise ValueError(f"Ligne {line_num}: Nom de nœud vide")
                        
                    graph[node].extend(outputs)
                    
                    # Vérification des références circulaires
                    for out in outputs:
                        if out == node:
                            print(f"Attention: Référence circulaire détectée pour le nœud {node}", 
                                  file=sys.stderr)
                            
                except ValueError as e:
                    print(f"Erreur de format à la ligne {line_num}: {e}", file=sys.stderr)
                    continue
                    
    except FileNotFoundError:
        print(f"Erreur: Le fichier {filename} est introuvable.", file=sys.stderr)
        raise
    
    return dict(graph)

class PathCounter:
    """Classe pour compter les chemins dans le graphe avec différentes contraintes."""
    
    def __init__(self, graph: Graph):
        """Initialise le compteur de chemins avec le graphe donné.
        
        Args:
            graph: Le graphe des connexions entre les nœuds
        """
        self.graph = graph
        self._validate_graph()
        
    def _validate_graph(self) -> None:
        """Vérifie que le graphe est valide (pas de nœuds non déclarés)."""
        all_nodes = set(self.graph.keys())
        for node, neighbors in self.graph.items():
            for neighbor in neighbors:
                if neighbor not in all_nodes and neighbor != "out":
                    print(f"Attention: Le nœud {neighbor} est référencé mais non déclaré", 
                          file=sys.stderr)
    
    @lru_cache(maxsize=None)
    def count_paths_to_out(self, node: str) -> int:
        """Compte le nombre de chemins d'un nœud à 'out'.
        
        Args:
            node: Le nœud de départ
            
        Returns:
            Le nombre de chemins possibles jusqu'à 'out'
        """
        if node == "out":
            return 1
        if node not in self.graph:
            return 0
        return sum(self.count_paths_to_out(neighbor) for neighbor in self.graph[node])
    
    @lru_cache(maxsize=None)
    def count_paths_through_nodes(
        self, 
        node: str, 
        required_nodes: Tuple[str, ...], 
        visited_nodes: Tuple[str, ...] = ()
    ) -> int:
        """Compte les chemins qui passent par tous les nœuds requis.
        
        Args:
            node: Le nœud actuel
            required_nodes: Les nœuds qui doivent être visités
            visited_nodes: Les nœuds déjà visités dans le chemin actuel
            
        Returns:
            Le nombre de chemins valides
        """
        # Mise à jour des nœuds visités
        current_visited = (*visited_nodes, node)
        
        # Vérification si tous les nœuds requis ont été visités
        remaining_required = set(required_nodes) - set(current_visited)
        
        # Si on est à la sortie, on vérifie si on a visité tous les nœuds requis
        if node == "out":
            return 1 if not remaining_required else 0
            
        # Si le nœud n'existe pas, c'est une impasse
        if node not in self.graph:
            return 0
            
        # Si on a déjà visité ce nœud, on évite les cycles
        if node in visited_nodes:
            return 0
            
        # Exploration récursive des voisins
        total = 0
        for neighbor in self.graph[node]:
            total += self.count_paths_through_nodes(
                neighbor, 
                required_nodes, 
                current_visited
            )
            
        return total

def main() -> None:
    """Fonction principale."""
    if len(sys.argv) != 2:
        print(f"Utilisation: {sys.argv[0]} <fichier_entrée>", file=sys.stderr)
        sys.exit(1)
        
    filename = sys.argv[1]
    
    try:
        # Chargement du graphe
        graph = parse_input(filename)
        
        # Vérification des nœuds nécessaires
        required_nodes = {"you", "svr", "dac", "fft", "out"}
        missing_nodes = required_nodes - set(graph.keys()) - {"out"}
        if missing_nodes:
            print(f"Attention: Nœuds manquants dans le graphe: {', '.join(missing_nodes)}", 
                  file=sys.stderr)
        
        # Initialisation du compteur de chemins
        path_counter = PathCounter(graph)
        
        # Partie 1: Chemins de 'you' à 'out'
        part1_result = path_counter.count_paths_to_out("you")
        print(f"Partie 1: {part1_result} chemins de 'you' à 'out'")
        
        # Partie 2: Chemins de 'svr' à 'out' passant par 'dac' et 'fft'
        part2_result = path_counter.count_paths_through_nodes("svr", ("dac", "fft"))
        print(f"Partie 2: {part2_result} chemins de 'svr' à 'out' passant par 'dac' et 'fft'")
        
    except Exception as e:
        print(f"Erreur: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()