# aoc_day3.py
from pathlib import Path

def max_two_digit_from_line(s):
    max_seen = -1
    best = -1
    for i in range(len(s)-1, -1, -1):
        d = ord(s[i]) - 48
        if max_seen != -1:
            candidate = d*10 + max_seen
            if candidate > best:
                best = candidate
        if d > max_seen:
            max_seen = d
    return best if best >= 0 else 0

def main():
    p = Path("input.txt")  
    if not p.exists():
        print("input.txt introuvable dans le dossier courant.")
        return
    lines = [l.strip() for l in p.read_text(encoding='utf-8').splitlines() if l.strip()]
    per_line = []
    total = 0
    for line in lines:
        val = max_two_digit_from_line(line)
        per_line.append(val)
        total += val

    print("Banques (lignes) :", len(lines))
    print("Somme totale des meilleurs jolts :", total)

    out = Path("aoc_day3_result.txt")
    with out.open("w", encoding="utf-8") as f:
        f.write(f"total={total}\n")
        for i, v in enumerate(per_line, start=1):
            f.write(f"{i},{v}\n")
    print("Résultats détaillés sauvés dans aoc_day3_result.txt")

if __name__ == "__main__":
    main()
