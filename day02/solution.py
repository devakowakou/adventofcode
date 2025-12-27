def is_repeated_twice(num_str: str) -> bool:
    """Vérifie si un nombre est composé d'une séquence répétée exactement deux fois.
    
    Args:
        num_str: Le nombre sous forme de chaîne de caractères
        
    Returns:
        bool: True si le nombre est une séquence répétée deux fois, False sinon
        
    Exemples:
        >>> is_repeated_twice("1212")
        True
        >>> is_repeated_twice("1234")
        False
    """
    return len(num_str) % 2 == 0 and num_str[:len(num_str)//2] == num_str[len(num_str)//2:]


def is_repeated_pattern(num_str: str) -> bool:
    """Vérifie si un nombre est composé d'une séquence répétée au moins deux fois.
    
    Args:
        num_str: Le nombre sous forme de chaîne de caractères
        
    Returns:
        bool: True si le nombre contient un motif répété, False sinon
        
    Exemples:
        >>> is_repeated_pattern("123123")
        True
        >>> is_repeated_pattern("12341234")
        True
        >>> is_repeated_pattern("12345")
        False
    """
    n = len(num_str)
    return any(
        num_str[:i] * (n // i) == num_str 
        for i in range(1, n // 2 + 1) 
        if n % i == 0 and n // i >= 2
    )


def parse_ranges(input_line: str) -> list[tuple[int, int]]:
    """Parse les plages séparées par des virgules.
    
    Args:
        input_line: Ligne d'entrée au format "début1-fin1,début2-fin2,..."
        
    Returns:
        Liste de tuples (début, fin) pour chaque plage
        
    Exemple:
        >>> parse_ranges("1-5,10-15")
        [(1, 5), (10, 15)]
    """
    try:
        return [
            tuple(map(int, part.split('-', 1)))
            for part in input_line.strip().strip(',').split(',')
            if part.strip()
        ]
    except (ValueError, AttributeError) as e:
        raise ValueError(f"Format de plage invalide dans: {input_line}") from e


def solve_part1(ranges: list[tuple[int, int]]) -> int:
    """Trouve la somme des IDs invalides (répétés exactement deux fois).
    
    Args:
        ranges: Liste de plages (début, fin) à vérifier
        
    Returns:
        La somme des nombres valides
    """
    return sum(
        num
        for start, end in ranges
        for num in range(start, end + 1)
        if is_repeated_twice(str(num))
    )


def solve_part2(ranges: list[tuple[int, int]]) -> int:
    """Trouve la somme des IDs invalides (motif répété au moins deux fois).
    
    Args:
        ranges: Liste de plages (début, fin) à vérifier
        
    Returns:
        La somme des nombres valides
    """
    return sum(
        num
        for start, end in ranges
        for num in range(start, end + 1)
        if is_repeated_pattern(str(num))
    )


def main():
    """Fonction principale qui lit l'entrée et affiche les résultats."""
    try:
        # Lecture du fichier d'entrée
        with open('input.txt', 'r') as f:
            input_line = f.read()
        
        # Analyse des plages
        ranges = parse_ranges(input_line)
        
        if not ranges:
            print("Aucune plage valide trouvée dans le fichier d'entrée.")
            return
            
        print(f"{len(ranges)} plages à vérifier")
        
        # Partie 1: Nombres répétés exactement deux fois
        result_part1 = solve_part1(ranges)
        print(f"Partie 1 - Somme des IDs invalides (répétés deux fois) : {result_part1}")
        
        # Partie 2: Motifs répétés au moins deux fois
        result_part2 = solve_part2(ranges)
        print(f"Partie 2 - Somme des IDs invalides (motif répété) : {result_part2}")
        
    except FileNotFoundError:
        print("Erreur: Fichier d'entrée non trouvé.")
    except ValueError as e:
        print(f"Erreur de format: {e}")
    except Exception as e:
        print(f"Erreur inattendue: {e}")


if __name__ == "__main__":
    main()
