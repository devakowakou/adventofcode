"""
Advent of Code 2025 - Jour 10 : Machines à Cadeaux
Solution optimisée avec typage statique et documentation complète
"""

import re
from typing import List, Tuple, Optional, Dict, Set
from pulp import LpProblem, LpVariable, LpMinimize, lpSum, LpInteger, PULP_CBC_CMD

# Types personnalisés
ConfigurationLumineuse = List[int]  # 0 pour éteint, 1 pour allumé
Bouton = List[int]  # Liste des indices des lumières contrôlées
Joltages = List[int]  # Exigences de joltage pour chaque compteur

def analyser_machine(ligne: str) -> Tuple[ConfigurationLumineuse, List[Bouton], Joltages]:
    """Analyse une ligne de spécification de machine.
    
    Args:
        ligne: Chaîne de caractères au format "[##...] (0,1) (2,3) {1,2,3}"
        
    Returns:
        Un tuple contenant:
        - La configuration lumineuse cible
        - La liste des boutons et les lumières qu'ils contrôlent
        - Les exigences de joltage
        
    Exemple:
        >>> analyser_machine("[.##.] (0,1) (1,2) {1,2}")
        ([0, 1, 1, 0], [[0, 1], [1, 2]], [1, 2])
    """
    # Extraire le motif des lumières
    motif_lumineux = re.search(r'\[([.#]+)\]', ligne)
    cible = [1 if c == '#' else 0 for c in motif_lumineux.group(1)] if motif_lumineux else []

    # Extraire les configurations des boutons
    boutons = []
    for match in re.finditer(r'\(([0-9,]+)\)', ligne):
        indices = [int(x) for x in match.group(1).split(',')]
        boutons.append(indices)

    # Extraire les exigences de joltage
    joltage_match = re.search(r'\{([0-9,]+)\}', ligne)
    joltages = [int(x) for x in joltage_match.group(1).split(',')] if joltage_match else []

    return cible, boutons, joltages

def resoudre_lumieres_brute_force(
    cible: ConfigurationLumineuse, 
    boutons: List[Bouton]
) -> Optional[int]:
    """Résout la partie 1 en testant toutes les combinaisons possibles.
    
    Args:
        cible: Configuration lumineuse souhaitée
        boutons: Liste des boutons et des lumières qu'ils contrôlent
        
    Returns:
        Le nombre minimum de pressions nécessaires, ou None si impossible
    """
    nb_lumieres = len(cible)
    nb_boutons = len(boutons)
    min_pressions = float('inf')

    # Essayer toutes les combinaisons possibles de boutons
    for masque in range(1 << nb_boutons):
        etat = [0] * nb_lumieres
        pressions = 0
        
        # Appliquer les boutons sélectionnés
        for i_bouton in range(nb_boutons):
            if masque & (1 << i_bouton):
                pressions += 1
                for lumiere in boutons[i_bouton]:
                    if 0 <= lumiere < nb_lumieres:
                        etat[lumiere] ^= 1
        
        # Vérifier si on a atteint la cible
        if etat == cible:
            min_pressions = min(min_pressions, pressions)

    return int(min_pressions) if min_pressions != float('inf') else None

def resoudre_joltage_ilp(
    joltages: Joltages, 
    boutons: List[Bouton], 
    timeout: int = 30
) -> Optional[int]:
    """Résout la partie 2 en utilisant la programmation linéaire en nombres entiers.
    
    Args:
        joltages: Exigences de joltage pour chaque compteur
        boutons: Liste des boutons et des compteurs qu'ils affectent
        timeout: Délai maximum en secondes pour la résolution
        
    Returns:
        Le nombre minimum de pressions nécessaires, ou None si impossible
    """
    nb_boutons = len(boutons)
    nb_compteurs = len(joltages)

    # Créer le problème d'optimisation
    probleme = LpProblem("Minimiser_Pressions", LpMinimize)
    
    # Variables de décision : nombre de fois qu'on appuie sur chaque bouton
    pressions = [LpVariable(f"x{i}", lowBound=0, cat=LpInteger) 
                for i in range(nb_boutons)]

    # Fonction objectif : minimiser le nombre total de pressions
    probleme += lpSum(pressions)

    # Contraintes : pour chaque compteur, la somme des pressions des boutons
    # qui l'affectent doit être égale à son joltage cible
    for i_compteur in range(nb_compteurs):
        if i_compteur < len(joltages):
            boutons_affectes = [
                pressions[i_bouton] 
                for i_bouton, bouton in enumerate(boutons) 
                if i_compteur in bouton
            ]
            if boutons_affectes:
                probleme += lpSum(boutons_affectes) == joltages[i_compteur]

    # Résoudre avec un timeout pour éviter les boucles infinies
    solveur = PULP_CBC_CMD(msg=0, timeLimit=timeout)
    statut = probleme.solve(solveur)

    if statut != 1:  # 1 = Optimal
        return None

    return int(sum(var.value() for var in pressions))

def main() -> None:
    """Fonction principale."""
    import sys
    from pathlib import Path

    # Vérifier les arguments en ligne de commande
    if len(sys.argv) != 2:
        print(f"Utilisation: {sys.argv[0]} <fichier_entree>", file=sys.stderr)
        sys.exit(1)

    fichier_entree = Path(sys.argv[1])
    if not fichier_entree.exists():
        print(f"Erreur: Le fichier {fichier_entree} n'existe pas.", file=sys.stderr)
        sys.exit(1)

    try:
        # Lire les lignes du fichier d'entrée
        with open(fichier_entree, 'r', encoding='utf-8') as f:
            lignes = [ligne.strip() for ligne in f if ligne.strip()]

        # Partie 1: Résoudre pour les lumières
        total_pressions_p1 = 0
        machines_resolues_p1 = 0

        for i, ligne in enumerate(lignes, 1):
            cible, boutons, _ = analyser_machine(ligne)
            resultat = resoudre_lumieres_brute_force(cible, boutons)
            
            if resultat is not None:
                total_pressions_p1 += resultat
                machines_resolues_p1 += 1
            else:
                print(f"Attention: Machine {i} n'a pas de solution pour la partie 1")

        print(f"Partie 1: {machines_resolues_p1} machines résolues, total des pressions = {total_pressions_p1}")

        # Partie 2: Résoudre pour les joltages
        total_pressions_p2 = 0
        machines_resolues_p2 = 0

        for i, ligne in enumerate(lignes, 1):
            _, boutons, joltages = analyser_machine(ligne)
            resultat = resoudre_joltage_ilp(joltages, boutons)
            
            if resultat is not None:
                total_pressions_p2 += resultat
                machines_resolues_p2 += 1
            else:
                print(f"Attention: Machine {i} n'a pas de solution pour la partie 2")

        print(f"Partie 2: {machines_resolues_p2} machines résolues, total des pressions = {total_pressions_p2}")

    except Exception as e:
        print(f"Erreur lors du traitement: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()