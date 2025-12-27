from typing import List, Tuple, Optional, Iterator
from dataclasses import dataclass
import sys

@dataclass
class MathProblem:
    """Représente un problème mathématique avec des nombres et une opération."""
    numbers: List[int]
    operation: str  # '+' ou '*'
    
    def solve(self) -> int:
        """Résout le problème mathématique.
        
        Returns:
            Le résultat de l'opération appliquée aux nombres.
            
        Raises:
            ValueError: Si l'opération n'est pas supportée.
        """
        if not self.numbers:
            return 0
            
        result = self.numbers[0]
        for num in self.numbers[1:]:
            if self.operation == '+':
                result += num
            elif self.operation == '*':
                result *= num
            else:
                raise ValueError(f"Opération non supportée: {self.operation}")
        return result

class WorksheetParser:
    """Classe pour parser les feuilles de calcul mathématiques."""
    
    def __init__(self, filename: str):
        """Initialise le parseur avec le fichier d'entrée.
        
        Args:
            filename: Chemin vers le fichier contenant la feuille de calcul.
        """
        self.filename = filename
        self.lines: List[str] = []
        self.max_width: int = 0
        
    def load_file(self) -> None:
        """Charge le fichier et prépare les données pour le traitement."""
        try:
            with open(self.filename, 'r') as f:
                self.lines = [line.rstrip('\n') for line in f if line.strip()]
                
            if not self.lines:
                raise ValueError("Le fichier est vide")
                
            self.max_width = max(len(line) for line in self.lines)
            
        except FileNotFoundError:
            print(f"Erreur: Le fichier {self.filename} est introuvable.", file=sys.stderr)
            sys.exit(1)
        except Exception as e:
            print(f"Erreur lors de la lecture du fichier: {e}", file=sys.stderr)
            sys.exit(1)
    
    def is_separator_column(self, col_idx: int, padded_lines: List[str]) -> bool:
        """Vérifie si une colonne est un séparateur.
        
        Une colonne est un séparateur si elle contient uniquement des espaces
        dans toutes les lignes de nombres et dans la ligne d'opération.
        """
        return all(
            line[col_idx] == ' ' if col_idx < len(line) else True
            for line in padded_lines
        )
    
    def parse_left_to_right(self) -> List[MathProblem]:
        """Parse la feuille de calcul de gauche à droite.
        
        Returns:
            Liste des problèmes mathématiques trouvés.
        """
        if not self.lines:
            self.load_file()
            
        operation_line = self.lines[-1]
        number_lines = self.lines[:-1]
        
        # Ajoute du padding si nécessaire
        padded_numbers = [line.ljust(self.max_width) for line in number_lines]
        padded_ops = operation_line.ljust(self.max_width)
        all_lines = padded_numbers + [padded_ops]
        
        problems = []
        current_numbers = []
        current_operation = None
        in_number = False
        
        for col_idx in range(self.max_width):
            # Vérifie si c'est une colonne séparatrice
            if self.is_separator_column(col_idx, all_lines):
                if current_numbers and current_operation:
                    problems.append(MathProblem(current_numbers, current_operation))
                    current_numbers = []
                    current_operation = None
                continue
                
            # Extrait les chiffres de la colonne
            digits = []
            for line in padded_numbers:
                if col_idx < len(line) and line[col_idx].isdigit():
                    digits.append(line[col_idx])
            
            if digits:
                number = int(''.join(digits))
                current_numbers.append(number)
                in_number = True
            elif in_number:
                # Fin d'un nombre
                in_number = False
                
            # Extrait l'opération
            if col_idx < len(padded_ops) and padded_ops[col_idx] in '+-*/':
                current_operation = padded_ops[col_idx]
                
        # Ajoute le dernier problème
        if current_numbers and current_operation:
            problems.append(MathProblem(current_numbers, current_operation))
            
        return problems
    
    def parse_right_to_left(self) -> List[MathProblem]:
        """Parse la feuille de calcul de droite à gauche.
        
        Returns:
            Liste des problèmes mathématiques trouvés.
        """
        if not self.lines:
            self.load_file()
            
        operation_line = self.lines[-1]
        number_lines = self.lines[:-1]
        
        # Ajoute du padding si nécessaire
        padded_numbers = [line.ljust(self.max_width) for line in number_lines]
        padded_ops = operation_line.ljust(self.max_width)
        all_lines = padded_numbers + [padded_ops]
        
        problems = []
        current_numbers = []
        current_operation = None
        
        # Parcours de droite à gauche
        for col_idx in range(self.max_width - 1, -1, -1):
            # Vérifie si c'est une colonne séparatrice
            if self.is_separator_column(col_idx, all_lines):
                if current_numbers and current_operation:
                    problems.append(MathProblem(current_numbers, current_operation))
                    current_numbers = []
                    current_operation = None
                continue
                
            # Extrait les chiffres de la colonne (du haut vers le bas)
            digits = []
            for line in padded_numbers:
                if col_idx < len(line) and line[col_idx].isdigit():
                    digits.append(line[col_idx])
            
            if digits:
                number = int(''.join(digits))
                current_numbers.append(number)
                
            # Extrait l'opération
            if col_idx < len(padded_ops) and padded_ops[col_idx] in '+-*/':
                current_operation = padded_ops[col_idx]
                
        # Ajoute le dernier problème
        if current_numbers and current_operation:
            problems.append(MathProblem(current_numbers, current_operation))
            
        return problems

def main() -> None:
    """Fonction principale."""
    if len(sys.argv) != 2:
        print(f"Utilisation: {sys.argv[0]} <fichier_entrée>", file=sys.stderr)
        sys.exit(1)
        
    filename = sys.argv[1]
    parser = WorksheetParser(filename)
    
    try:
        # Partie 1: Lecture de gauche à droite
        print("Partie 1: Lecture de gauche à droite")
        problems = parser.parse_left_to_right()
        print(f"  {len(problems)} problèmes trouvés")
        
        total = sum(problem.solve() for problem in problems)
        print(f"  Total: {total}\n")
        
        # Affiche les 3 premiers problèmes à titre d'exemple
        for i, problem in enumerate(problems[:3], 1):
            nums = " ".join(str(n) for n in problem.numbers)
            print(f"  Problème {i}: {nums} {problem.operation} = {problem.solve()}")
        
        # Partie 2: Lecture de droite à gauche
        print("\nPartie 2: Lecture de droite à gauche")
        problems_rtl = parser.parse_right_to_left()
        print(f"  {len(problems_rtl)} problèmes trouvés")
        
        total_rtl = sum(problem.solve() for problem in problems_rtl)
        print(f"  Total: {total_rtl}\n")
        
        # Affiche les 3 premiers problèmes à titre d'exemple
        for i, problem in enumerate(problems_rtl[:3], 1):
            nums = " ".join(str(n) for n in problem.numbers)
            print(f"  Problème {i}: {nums} {problem.operation} = {problem.solve()}")
            
    except Exception as e:
        print(f"Erreur: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()