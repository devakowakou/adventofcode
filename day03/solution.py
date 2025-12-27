from typing import List, Tuple

def is_invalid_id(num: int) -> bool:
    """Vérifie si un nombre est invalide (séquence répétée deux fois).
    
    Un nombre est invalide si :
    - Il a un nombre pair de chiffres
    - La première moitié est identique à la seconde
    - La première moitié ne commence pas par zéro
    
    Args:
        num: Le nombre à vérifier
        
    Returns:
        bool: True si le nombre est invalide, False sinon
    """
    num_str = str(num)
    if len(num_str) % 2 != 0:
        return False
        
    half = len(num_str) // 2
    first_half = num_str[:half]
    return first_half[0] != '0' and first_half == num_str[half:]


def parse_ranges(ranges_input: str) -> List[Tuple[int, int]]:
    """Parse les plages de nombres depuis une chaîne.
    
    Format attendu : "début-fin,début-fin,..."
    
    Args:
        ranges_input: Chaîne contenant les plages à parser
        
    Returns:
        Liste de tuples (début, fin) pour chaque plage
    """
    ranges = []
    for range_str in (r.strip() for r in ranges_input.split(',') if r.strip()):
        try:
            start, end = map(int, range_str.split('-', 1))
            if start > end:
                start, end = end, start
            ranges.append((start, end))
        except (ValueError, IndexError) as e:
            raise ValueError(f"Format de plage invalide: {range_str}") from e
    return ranges


def solve() -> int:
    """Résout le problème du jour 3.
    
    Returns:
        La somme des IDs invalides dans les plages spécifiées
        
    Raises:
        FileNotFoundError: Si le fichier input.txt n'existe pas
        ValueError: Si le format du fichier est incorrect
    """
    try:
        with open('input.txt', 'r') as f:
            ranges_input = f.read().strip()
            
        ranges = parse_ranges(ranges_input)
        if not ranges:
            print("Aucune plage valide trouvée.")
            return 0
            
        return sum(
            num
            for start, end in ranges
            for num in range(start, end + 1)
            if is_invalid_id(num)
        )
        
    except FileNotFoundError:
        raise FileNotFoundError("Erreur: Fichier 'input.txt' introuvable.")
    except Exception as e:
        raise ValueError(f"Erreur lors du traitement: {str(e)}") from e


if __name__ == "__main__":
    try:
        result = solve()
        print(f"Somme des IDs invalides: {result}")
    except (FileNotFoundError, ValueError) as e:
        print(f"Erreur: {str(e)}")
        exit(1)