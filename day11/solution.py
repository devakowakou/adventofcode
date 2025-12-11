"""
Advent of Code 2025 - Day 11 : Reactor
Solution optimisée et entièrement documentée
"""

from functools import lru_cache


# ------------------------------------------------------------
# Parsing du fichier input.txt
# ------------------------------------------------------------
def parse_input(filename):
    graph = {}

    with open(filename) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue

            node, outs = line.split(":")
            node = node.strip()
            outputs = outs.strip().split()

            graph[node] = outputs

    return graph


# ------------------------------------------------------------
# PART 1 : Nombre total de chemins de 'you' vers 'out'
# DFS + MEMO pour éviter l'explosion combinatoire.
# ------------------------------------------------------------
@lru_cache(None)
def count_paths_part1(node):
    """
    Retourne le nombre total de chemins allant de 'node' jusqu'à 'out'.
    - Mémoïsation sur le node (fonction des sorties seulement)
    """
    if node == "out":
        return 1

    if node not in GRAPH:
        return 0

    return sum(count_paths_part1(nxt) for nxt in GRAPH[node])


# ------------------------------------------------------------
# PART 2 : Nombre de chemins de 'svr' vers 'out'
# qui passent OBLIGATOIREMENT par 'dac' ET 'fft'
#
# État du DFS = (node, seen_dac, seen_fft)
# Mémoïsation pour exploser aucune fois inutilement.
# ------------------------------------------------------------
@lru_cache(None)
def count_paths_part2(node, seen_dac, seen_fft):
    """
    seen_dac, seen_fft : bool -> indiquent si les nœuds 'dac' et 'fft'
    ont été visités sur le chemin actuel.
    """
    seen_dac = seen_dac or (node == "dac")
    seen_fft = seen_fft or (node == "fft")

    # Si on atteint 'out', c'est un chemin valide
    # UNIQUEMENT si les deux noeuds ont été visités.
    if node == "out":
        return 1 if (seen_dac and seen_fft) else 0

    # Dead end
    if node not in GRAPH:
        return 0

    # DFS
    total = 0
    for nxt in GRAPH[node]:
        total += count_paths_part2(nxt, seen_dac, seen_fft)

    return total


# ------------------------------------------------------------
# MAIN
# ------------------------------------------------------------
def main():
    global GRAPH
    GRAPH = parse_input("input.txt")

    # ------- PART 1 -------
    part1_result = count_paths_part1("you")
    print("Part 1:", part1_result)

    # ------- PART 2 -------
    part2_result = count_paths_part2("svr", False, False)
    print("Part 2:", part2_result)


if __name__ == "__main__":
    main()
