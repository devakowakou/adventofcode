def solve():
    with open('input.txt', 'r') as f:
        rotations = [line.strip() for line in f.readlines()]
    position = 50
    zero_count = 0
    print(f"Position de départ: {position}")
    print("-" * 50)
    for i, rotation in enumerate(rotations, 1):
        direction = rotation[0]
        distance = int(rotation[1:])
        old_position = position
        if direction == 'L':
            position = (position - distance) % 100
        else:
            position = (position + distance) % 100
        print(f"#{i:3d} | {rotation:5s} | {old_position:2d} → {position:2d}", end="")
        if position == 0:
            zero_count += 1
            print(" ✓ ZERO!")
        else:
            print()
    
    print("-" * 50)
    return zero_count

if __name__ == "__main__":
    password = solve()
    print(f"The password is: {password}")
