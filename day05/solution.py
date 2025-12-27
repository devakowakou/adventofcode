from typing import List, Tuple
from dataclasses import dataclass
import sys

@dataclass(frozen=True)
class Range:
    """Représente une plage de numéros d'ingrédients frais."""
    start: int
    end: int

    def __lt__(self, other: 'Range') -> bool:
        """Permet de trier les plages par ordre croissant."""
        return (self.start, self.end) < (other.start, other.end)

    def contains(self, value: int) -> bool:
        """Vérifie si une valeur est dans la plage."""
        return self.start <= value <= self.end

    def overlaps(self, other: 'Range') -> bool:
        """Vérifie si cette plage chevauche une autre plage."""
        return (self.start <= other.end + 1 and 
                other.start <= self.end + 1)

    def merge(self, other: 'Range') -> 'Range':
        """Fusionne cette plage avec une autre plage qui la chevauche."""
        return Range(
            min(self.start, other.start),
            max(self.end, other.end)
        )

def parse_input(filename: str) -> Tuple[List[Range], List[int]]:
    """Parse le fichier d'entrée en plages et identifiants d'ingrédients.
    
    Args:
        filename: Chemin vers le fichier d'entrée
        
    Returns:
        Tuple contenant:
        - Liste des plages d'ingrédients frais
        - Liste des identifiants d'ingrédients à vérifier
    """
    try:
        with open(filename, 'r') as f:
            lines = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print(f"Erreur: Le fichier {filename} est introuvable.", file=sys.stderr)
        sys.exit(1)

    try:
        # Séparation des plages et des IDs
        separator = lines.index('')
        range_lines = lines[:separator]
        id_lines = lines[separator + 1:]
        
        # Parsing des plages
        ranges = []
        for line in range_lines:
            start, end = map(int, line.split('-', 1))
            ranges.append(Range(start, end))
            
        # Parsing des IDs
        ingredient_ids = [int(id_str) for id_str in id_lines]
        
        return ranges, ingredient_ids
        
    except (ValueError, IndexError) as e:
        print(f"Erreur de format dans le fichier {filename}: {e}", file=sys.stderr)
        sys.exit(1)

def merge_ranges(ranges: List[Range]) -> List[Range]:
    """Fusionne les plages qui se chevauchent ou se touchent.
    
    Args:
        ranges: Liste de plages à fusionner
        
    Returns:
        Liste des plages fusionnées
    """
    if not ranges:
        return []
        
    # Tri des plages par ordre croissant
    sorted_ranges = sorted(ranges)
    merged = [sorted_ranges[0]]
    
    for current in sorted_ranges[1:]:
        last = merged[-1]
        if last.overlaps(current):
            merged[-1] = last.merge(current)
        else:
            merged.append(current)
    
    return merged

def count_fresh_ingredients(ranges: List[Range], ingredient_ids: List[int]) -> int:
    """Compte le nombre d'ingrédients frais.
    
    Args:
        ranges: Plages d'ingrédients frais
        ingredient_ids: Liste des identifiants à vérifier
        
    Returns:
        Nombre d'ingrédients frais
    """
    # Optimisation: création d'un set pour des recherches rapides
    fresh_ranges = merge_ranges(ranges)
    
    def is_fresh(ingredient_id: int) -> bool:
        """Vérifie si un ingrédient est frais."""
        # Recherche binaire serait plus efficace pour beaucoup de plages
        return any(r.contains(ingredient_id) for r in fresh_ranges)
    
    return sum(1 for ingredient_id in ingredient_ids if is_fresh(ingredient_id))

def count_total_fresh_ids(ranges: List[Range]) -> int:
    """Compte le nombre total d'IDs d'ingrédients frais uniques.
    
    Args:
        ranges: Plages d'ingrédients frais
        
    Returns:
        Nombre total d'IDs uniques dans les plages
    """
    return sum(r.end - r.start + 1 for r in merge_ranges(ranges))

def main() -> None:
    """Fonction principale."""
    if len(sys.argv) != 2:
        print(f"Utilisation: {sys.argv[0]} <fichier_entree>", file=sys.stderr)
        sys.exit(1)
        
    filename = sys.argv[1]
    
    try:
        # Lecture et analyse de l'entrée
        ranges, ingredient_ids = parse_input(filename)
        
        print(f"Plages d'ingrédients frais: {len(ranges)}")
        print(f"Nombre d'ingrédients à vérifier: {len(ingredient_ids)}")
        
        # Partie 1: Nombre d'ingrédients frais
        fresh_count = count_fresh_ingredients(ranges, ingredient_ids)
        print(f"\nPartie 1 - Ingrédients frais: {fresh_count}")
        
        # Partie 2: Nombre total d'IDs frais uniques
        total_fresh = count_total_fresh_ids(ranges)
        print(f"Partie 2 - Total des IDs frais uniques: {total_fresh}")
        
    except Exception as e:
        print(f"Erreur: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()