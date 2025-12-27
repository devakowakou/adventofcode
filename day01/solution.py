def parse_rotation(line: str) -> tuple[str, int]:
    """Parse une ligne de rotation comme 'L68' ou 'R48'.
    
    Args:
        line: Chaîne au format '[LR]\\d+'
    
    Returns:
        Un tuple (direction, distance)
    
    Raises:
        ValueError: Si le format est incorrect
    """
    if not line or line[0] not in 'LR':
        raise ValueError(f"Direction invalide dans: {line}")
    
    try:
        return line[0], int(line[1:])
    except ValueError as e:
        raise ValueError(f"Distance invalide dans: {line}") from e


def rotate_dial(current_pos: int, direction: str, distance: int) -> int:
    """Fait tourner le cadran et retourne la nouvelle position.
    
    Args:
        current_pos: Position actuelle (0-99)
        direction: 'L' pour gauche, 'R' pour droite
        distance: Nombre de crans à tourner
        
    Returns:
        Nouvelle position (0-99)
    """
    rotation = -distance if direction == 'L' else distance
    return (current_pos + rotation) % 100


def count_zeros_during_rotation(start_pos: int, direction: str, distance: int) -> int:
    """Compte combien de fois le cadran passe par 0 pendant la rotation.
    
    Args:
        start_pos: Position de départ (0-99)
        direction: 'L' ou 'R'
        distance: Nombre de crans à tourner
        
    Returns:
        Nombre de passages par 0 pendant la rotation
    """
    if direction == 'L':
        # Pour une rotation à gauche, on décrémente
        start = (start_pos - 1) % 100
        end = (start_pos - distance) % 100
        # Si on fait le tour complet, on ajoute 1
        return (start // 100 - end // 100) % 100
    else:
        # Pour une rotation à droite, on incrémente
        start = (start_pos + 1) % 100
        end = (start_pos + distance) % 100
        return (end // 100 - start // 100) % 100


def solve_part1(rotations: list[tuple[str, int]]) -> int:
    """Résout la partie 1: compte les zéros après chaque rotation complète.
    
    Args:
        rotations: Liste de tuples (direction, distance)
        
    Returns:
        Nombre de fois où on est sur 0 après une rotation
    """
    position = 50
    return sum(1 for direction, distance in rotations 
              if (position := rotate_dial(position, direction, distance)) == 0)


def solve_part2(rotations: list[tuple[str, int]]) -> int:
    """Résout la partie 2: compte tous les passages par 0.
    
    Args:
        rotations: Liste de tuples (direction, distance)
        
    Returns:
        Nombre total de passages par 0
    """
    position = 50
    zero_count = 0
    
    for direction, distance in rotations:
        zero_count += count_zeros_during_rotation(position, direction, distance)
        position = rotate_dial(position, direction, distance)
    
    return zero_count


def main():
    try:
        # Lecture du fichier d'entrée
        with open('input.txt', 'r') as f:
            lines = [line.strip() for line in f if line.strip()]
        
        # Parsing des rotations
        rotations = [parse_rotation(line) for line in lines]
        
        # Partie 1
        result_part1 = solve_part1(rotations)
        print(f"Partie 1 - Mot de passe (zéros après rotation): {result_part1}")
        
        # Partie 2
        result_part2 = solve_part2(rotations)
        print(f"Partie 2 - Mot de passe (zéros pendant rotation): {result_part2}")
        
    except FileNotFoundError:
        print("Erreur: Fichier d'entrée non trouvé.")
    except ValueError as e:
        print(f"Erreur de format: {e}")
    except Exception as e:
        print(f"Erreur inattendue: {e}")


if __name__ == "__main__":
    main()
