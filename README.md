# Advent of Code 2025 Solutions

Solutions pour les défis Advent of Code 2025.

## 🎄 Progression

| Jour | Partie 1 | Partie 2 | Description |
|------|----------|----------|-------------|
| [Jour 1](day01/) | ⭐ 1145 | ⭐ 6561 | Secret Entrance - Rotation de cadran |
| [Jour 2](day02/) | ⭐ 26255179562 | ⭐ 31680313976 | Gift Shop - IDs de produits invalides |
| [Jour 3](day03/) | ⭐ | ⭐ | Résultat dans result.txt |
| [Jour 4](day04/) | ⭐ 1518 | ⭐ 8665 | Printing Department - Rouleaux de papier accessibles |
| [Jour 5](day05/) | ⭐ 679 | ⭐ 358155203664116 | Cafeteria - Gestion d'inventaire d'ingrédients |
| [Jour 6](day06/) | ⭐ | ⭐ | |
| [Jour 7](day07/) | ⭐ | ⭐ | |
| [Jour 8](day08/) | ⭐ | ⭐ | |
| [Jour 9](day09/) | ⭐ | ⭐ | |
| [Jour 10](day10/) | ⭐ | ⭐ | |

**Total: 10 étoiles ⭐**

## 📋 Description des défis

### Jour 1: Secret Entrance
Simulation d'un cadran de coffre-fort avec rotations circulaires (0-99).
- **Partie 1**: Compter combien de fois le cadran pointe sur 0 après chaque rotation
- **Partie 2**: Compter tous les passages par 0, y compris pendant les rotations

### Jour 2: Gift Shop
Identification d'IDs de produits invalides basés sur des motifs répétés.
- **Partie 1**: IDs avec un motif répété exactement 2 fois (ex: 6464, 123123)
- **Partie 2**: IDs avec un motif répété au moins 2 fois (ex: 111, 12341234)

### Jour 3: Lobby
Résultat stocké dans `aoc_day3_result.txt`

### Jour 4: Printing Department
Analyse d'une grille de rouleaux de papier pour optimiser le travail des chariots élévateurs.
- **Partie 1**: Compter les rouleaux accessibles (moins de 4 rouleaux adjacents)
- **Partie 2**: Supprimer itérativement tous les rouleaux accessibles

### Jour 5: Cafeteria
Système de gestion d'inventaire pour identifier les ingrédients frais.
- **Partie 1**: Vérifier quels IDs disponibles sont dans les plages fraîches
- **Partie 2**: Compter tous les IDs dans les plages fraîches (avec fusion des plages qui se chevauchent)

## 🚀 Utilisation

```bash
# Exécuter une solution spécifique
python run.py 1
python run.py 2
python run.py 4
python run.py 5

# Ou directement dans le dossier du jour
cd day01 && python solution.py
cd day02 && python solution.py
```

## 📁 Structure des fichiers

```
adventofcode/
├── run.py              # Script de lancement global
├── README.md           # Ce fichier
├── requirements.txt    # Dépendances Python
├── utils/              # Utilitaires communs
│   └── main.py
├── day01/              # Jour 1
│   ├── solution.py     # Solution du jour
│   └── input.txt       # Input du jour
├── day02/              # Jour 2
│   ├── solution.py
│   └── input.txt
├── day03/              # Jour 3
│   ├── solution.py
│   ├── result.txt      # Résultat stocké
│   ├── lobby.py        # Fichiers additionnels
│   └── lob.py
└── dayXX/              # Structure pour chaque jour
    ├── solution.py     # Solution principale
    ├── input.txt       # Input du défi
    └── *.py            # Fichiers additionnels si nécessaire
```

## 🛠️ Technologies

- Python 3
- Algorithmes: grilles 2D, fusion d'intervalles, simulation, détection de motifs

---

*Prêt pour le jour 6! 🎅*
