"""
Advent of Code 2025 - Jour 12 : Emballage de cadeaux
Solution optimisée avec typage statique et documentation complète
"""

from functools import lru_cache
from typing import Dict, List, Set, Tuple, Optional
from collections import defaultdict
import sys

# Types personnalisés
Cell = Tuple[int, int]  # (ligne, colonne)
Orientation = Tuple[Cell, ...]
ShapeOrientations = Dict[int, List[Orientation]]
Placements = Dict[int, List[int]]  # Dictionnaire d'index de forme vers listes de masques de bits

def lire_entree(chemin_fichier: str = 'input.txt') -> Tuple[Dict[int, List[str]], List[Tuple[int, int, List[int]]]]:
    """Lit le fichier d'entrée et retourne les formes et régions.
    
    Args:
        chemin_fichier: Chemin vers le fichier d'entrée
        
    Returns:
        Un tuple contenant:
        - Un dictionnaire des formes (index -> lignes de la forme)
        - Une liste de régions (largeur, hauteur, comptage des formes)
        
    Lève:
        FileNotFoundError: Si le fichier n'existe pas
        ValueError: Si le format du fichier est invalide
    """
    try:
        with open(chemin_fichier, 'r', encoding='utf-8') as f:
            lignes = [ligne.strip() for ligne in f if ligne.strip()]

        formes = {}
        regions = []
        i = 0
        n = len(lignes)
        
        # Lire les formes
        while i < n and ':' in lignes[i] and lignes[i].split(':')[0].isdigit():
            idx = int(lignes[i].split(':')[0])
            i += 1
            formes_lignes = []
            while i < n and lignes[i] and not lignes[i].startswith(('0', '1', '2', '3', '4', '5', '6', '7', '8', '9')):
                if lignes[i].strip():
                    formes_lignes.append(lignes[i].strip())
                i += 1
            if formes_lignes:
                formes[idx] = formes_lignes
                
        # Lire les régions
        while i < n:
            if 'x' in lignes[i] and ':' in lignes[i]:
                dims, comptes_str = lignes[i].split(':', 1)
                largeur, hauteur = map(int, dims.split('x'))
                comptes = list(map(int, comptes_str.split()))
                regions.append((largeur, hauteur, comptes))
            i += 1
                
        return formes, regions
        
    except Exception as e:
        raise ValueError(f"Erreur lors de la lecture du fichier {chemin_fichier}: {e}")

def convertir_en_cellules(lignes_forme: List[str]) -> List[Cell]:
    """Convertit une forme en liste de cellules occupées.
    
    Args:
        lignes_forme: Liste de chaînes représentant la forme
        
    Returns:
        Liste des coordonnées (ligne, colonne) des cellules occupées (#)
    """
    return [(r, c) 
            for r, ligne in enumerate(lignes_forme) 
            for c, case in enumerate(ligne) 
            if case == '#']

def normaliser_cellules(cellules: List[Cell]) -> Orientation:
    """Normalise les coordonnées pour que la cellule la plus en haut à gauche soit à (0,0).
    
    Args:
        cellules: Liste des coordonnées des cellules
        
    Returns:
        Tuple des coordonnées normalisées, triées
    """
    if not cellules:
        return ()
    min_ligne = min(r for r, _ in cellules)
    min_col = min(c for _, c in cellules)
    return tuple(sorted((r - min_ligne, c - min_col) for r, c in cellules))

def pivoter_90(cellules: Orientation) -> Orientation:
    """Effectue une rotation de 90° dans le sens horaire.
    
    Args:
        cellules: Cellules à pivoter
        
    Returns:
        Nouvelles coordonnées après rotation
    """
    return normaliser_cellules([(c, -r) for r, c in cellules])

def retourner(cellules: Orientation) -> Orientation:
    """Retourne horizontalement la forme.
    
    Args:
        cellules: Cellules à retourner
        
    Returns:
        Nouvelles coordonnées après retournement
    """
    return normaliser_cellules([(r, -c) for r, c in cellules])

def generer_orientations(cellules: List[Cell]) -> Set[Orientation]:
    """Génère toutes les orientations uniques d'une forme.
    
    Args:
        cellules: Cellules de la forme d'origine
        
    Returns:
        Ensemble des orientations uniques (rotations et symétries)
    """
    orientations = set()
    courante = normaliser_cellules(cellules)
    
    for _ in range(4):
        courante = pivoter_90(courante)
        orientations.add(courante)
        orientations.add(retourner(courante))
        
    return orientations

def calculer_placements(
    forme: Orientation, 
    largeur: int, 
    hauteur: int
) -> List[int]:
    """Calcule tous les placements possibles d'une forme dans une région.
    
    Args:
        forme: Orientation de la forme
        largeur: Largeur de la région
        hauteur: Hauteur de la région
        
    Returns:
        Liste des masques de bits représentant les placements valides
    """
    if not forme:
        return []
        
    max_r = max(r for r, _ in forme)
    max_c = max(c for _, c in forme)
    placements = []
    
    for r in range(hauteur - max_r):
        for c in range(largeur - max_c):
            masque = 0
            valide = True
            
            for dr, dc in forme:
                nr, nc = r + dr, c + dc
                if nr < 0 or nr >= hauteur or nc < 0 or nc >= largeur:
                    valide = False
                    break
                masque |= 1 << (nr * largeur + nc)
                
            if valide:
                placements.append(masque)
                
    return placements

def resoudre_region(
    largeur: int,
    hauteur: int,
    formes_orientations: ShapeOrientations,
    comptes: List[int],
    timeout: Optional[float] = None
) -> bool:
    """Détermine si une région peut être remplie avec les formes données.
    
    Args:
        largeur: Largeur de la région
        hauteur: Hauteur de la région
        formes_orientations: Dictionnaire des orientations par forme
        comptes: Nombre de chaque forme à placer
        timeout: Temps maximum d'exécution (non implémenté)
        
    Returns:
        True si la région peut être remplie, False sinon
    """
    # Vérification de l'aire totale
    aire_totale = largeur * hauteur
    aire_formes = {
        idx: len(orientations[0]) 
        for idx, orientations in formes_orientations.items()
    }
    
    if sum(cnt * aire_formes[idx] for idx, cnt in enumerate(comptes)) != aire_totale:
        return False
        
    # Préparation des placements
    placements_par_forme: Placements = {}
    for idx, orientations in formes_orientations.items():
        if comptes[idx] == 0:
            continue
            
        placements = []
        for ori in orientations:
            placements.extend(calculer_placements(ori, largeur, hauteur))
            
        if not placements:
            return False
            
        placements_par_forme[idx] = list(set(placements))
    
    # Préparation des instances à placer
    instances = [
        idx 
        for idx, cnt in enumerate(comptes) 
        for _ in range(cnt)
    ]
    
    if not instances:
        return aire_totale == 0
        
    # Tri des instances par nombre de placements (moins de placements en premier)
    instances.sort(key=lambda i: len(placements_par_forme.get(i, [])))
    
    # Vérification rapide
    if any(not placements_par_forme.get(i) for i in instances):
        return False
    
    # Backtracking avec mémoïsation
    memo = set()
    
    def backtrack(pos: int, occupe: int) -> bool:
        if pos == len(instances):
            return True
            
        cle = (pos, occupe)
        if cle in memo:
            return False
            
        idx_forme = instances[pos]
        for placement in placements_par_forme.get(idx_forme, []):
            if (placement & occupe) == 0:
                if backtrack(pos + 1, occupe | placement):
                    return True
                    
        memo.add(cle)
        return False
    
    return backtrack(0, 0)

def resoudre_tout(
    formes_brutes: Dict[int, List[str]],
    regions: List[Tuple[int, int, List[int]]]
) -> Tuple[int, List[bool]]:
    """Résout le problème pour toutes les régions.
    
    Args:
        formes_brutes: Dictionnaire des formes brutes
        regions: Liste des régions à résoudre
        
    Returns:
        Un tuple (nombre de régions résolues, résultats par région)
    """
    # Précalcul des orientations pour chaque forme
    formes_orientations: ShapeOrientations = {}
    for idx, lignes in formes_brutes.items():
        cellules = convertir_en_cellules(lignes)
        orientations = generer_orientations(cellules)
        formes_orientations[idx] = list(orientations)
    
    # Résolution de chaque région
    resultats = []
    for largeur, hauteur, comptes in regions:
        # Ajustement de la taille des comptes
        max_idx = max(formes_orientations.keys()) if formes_orientations else 0
        comptes_etendus = comptes + [0] * (max(0, max_idx + 1 - len(comptes)))
        
        # Filtrage des formes présentes
        formes_presentes = {
            idx: oris 
            for idx, oris in formes_orientations.items() 
            if idx < len(comptes_etendus) and comptes_etendus[idx] > 0
        }
        
        # Résolution
        reussi = resoudre_region(
            largeur, 
            hauteur, 
            formes_presentes, 
            comptes_etendus
        )
        resultats.append(reussi)
    
    return sum(resultats), resultats

def main() -> None:
    """Fonction principale."""
    if len(sys.argv) != 2:
        print(f"Utilisation: {sys.argv[0]} <fichier_entrée>", file=sys.stderr)
        sys.exit(1)
    
    try:
        # Lecture de l'entrée
        formes, regions = lire_entree(sys.argv[1])
        
        # Résolution
        nb_reussis, _ = resoudre_tout(formes, regions)
        
        # Affichage du résultat
        print(f"Régions pouvant contenir tous les cadeaux: {nb_reussis}")
        
    except Exception as e:
        print(f"Erreur: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()