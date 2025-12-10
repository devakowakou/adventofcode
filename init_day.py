#!/usr/bin/env python3
"""
Script d'initialisation pour un nouveau jour d'Advent of Code
Usage: python init_day.py [jour]
Exemple: python init_day.py 11
"""
import sys
import os
from pathlib import Path

SOLUTION_TEMPLATE = '''#!/usr/bin/env python3
"""
Advent of Code 2025 - Day {day}
"""

def parse_input(filename='input.txt'):
    """Parse le fichier d'entrée"""
    with open(filename, 'r') as f:
        lines = f.read().strip().split('\\n')
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
    print(f"Part 1: {{result1}}")
    
    # Partie 2
    result2 = part2(data)
    print(f"Part 2: {{result2}}")


if __name__ == "__main__":
    main()
'''

def init_day(day_num):
    """Initialise le dossier et les fichiers pour un jour donné"""
    day_folder = Path(f"day{day_num:02d}")
    
    # Vérifier si le dossier existe déjà
    if day_folder.exists():
        response = input(f"⚠️  Le dossier {day_folder} existe déjà. Écraser? (o/N): ")
        if response.lower() != 'o':
            print("❌ Opération annulée")
            return False
    
    # Créer le dossier
    day_folder.mkdir(exist_ok=True)
    print(f"✅ Dossier créé: {day_folder}/")
    
    # Créer solution.py
    solution_file = day_folder / "solution.py"
    if not solution_file.exists() or input(f"Écraser {solution_file}? (o/N): ").lower() == 'o':
        with open(solution_file, 'w') as f:
            f.write(SOLUTION_TEMPLATE.format(day=day_num))
        # Rendre exécutable
        os.chmod(solution_file, 0o755)
        print(f"✅ Fichier créé: {solution_file}")
    
    # Créer input.txt vide
    input_file = day_folder / "input.txt"
    if not input_file.exists():
        input_file.touch()
        print(f"✅ Fichier créé: {input_file}")
    else:
        print(f"ℹ️  Fichier existant conservé: {input_file}")
    
    # Créer README.md
    readme_file = day_folder / "README.md"
    if not readme_file.exists():
        with open(readme_file, 'w') as f:
            f.write(f"# Day {day_num}\n\n")
            f.write(f"[Problème sur adventofcode.com](https://adventofcode.com/2025/day/{day_num})\n\n")
            f.write("## Partie 1\n\n")
            f.write("TODO: Description\n\n")
            f.write("## Partie 2\n\n")
            f.write("TODO: Description\n")
        print(f"✅ Fichier créé: {readme_file}")
    
    print(f"\n🎄 Jour {day_num} initialisé avec succès!")
    print(f"\nProchaines étapes:")
    print(f"1. Copier votre input dans: {input_file}")
    print(f"2. Éditer la solution dans: {solution_file}")
    print(f"3. Lancer avec: python run.py {day_num}")
    
    return True


def main():
    if len(sys.argv) != 2:
        print("Usage: python init_day.py [jour]")
        print("Exemple: python init_day.py 11")
        return
    
    try:
        day = int(sys.argv[1])
        if day < 1 or day > 25:
            print("❌ Le jour doit être entre 1 et 25")
            return
        init_day(day)
    except ValueError:
        print("❌ Le jour doit être un nombre")


if __name__ == "__main__":
    main()
