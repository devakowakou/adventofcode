#!/usr/bin/env python3
"""
Script de lancement pour Advent of Code 2025
Usage: python run.py [jour]
"""
import sys
import os
import subprocess

def run_day(day_num):
    """Exécute la solution pour un jour donné"""
    day_folder = f"day{day_num:02d}"
    solution_path = os.path.join(day_folder, "solution.py")
    
    if not os.path.exists(solution_path):
        print(f"❌ Solution non trouvée pour le jour {day_num}")
        return False
    
    print(f"🎄 Exécution du jour {day_num}...")
    try:
        result = subprocess.run([sys.executable, solution_path], 
                              cwd=day_folder, 
                              capture_output=True, 
                              text=True)
        print(result.stdout)
        if result.stderr:
            print(f"Erreurs: {result.stderr}")
        return result.returncode == 0
    except Exception as e:
        print(f"❌ Erreur lors de l'exécution: {e}")
        return False

def main():
    if len(sys.argv) != 2:
        print("Usage: python run.py [jour]")
        print("Exemple: python run.py 1")
        return
    
    try:
        day = int(sys.argv[1])
        if day < 1 or day > 25:
            print("Le jour doit être entre 1 et 25")
            return
        run_day(day)
    except ValueError:
        print("Le jour doit être un nombre")

if __name__ == "__main__":
    main()