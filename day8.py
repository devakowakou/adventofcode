import heapq
from collections import defaultdict


def parse_input(filename):
    """Parse the junction box coordinates from the input file."""
    boxes = []
    with open(filename, 'r') as f:
        for line in f:
            line = line.strip()
            if line:
                x, y, z = map(int, line.split(','))
                boxes.append((x, y, z))
    return boxes


def distance(box1, box2):
    """Calculate the Euclidean distance between two junction boxes."""
    x1, y1, z1 = box1
    x2, y2, z2 = box2
    return ((x2 - x1)**2 + (y2 - y1)**2 + (z2 - z1)**2) ** 0.5


class UnionFind:
    """Union-Find data structure to track connected circuits."""
    
    def __init__(self, n):
        self.parent = list(range(n))
        self.rank = [0] * n
        self.size = [1] * n
    
    def find(self, x):
        """Find the root of the set containing x with path compression."""
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]
    
    def union(self, x, y):
        """Union the sets containing x and y."""
        root_x = self.find(x)
        root_y = self.find(y)
        
        if root_x == root_y:
            return False  # Already in the same set
        
        # Union by rank
        if self.rank[root_x] < self.rank[root_y]:
            self.parent[root_x] = root_y
            self.size[root_y] += self.size[root_x]
        elif self.rank[root_x] > self.rank[root_y]:
            self.parent[root_y] = root_x
            self.size[root_x] += self.size[root_y]
        else:
            self.parent[root_y] = root_x
            self.size[root_x] += self.size[root_y]
            self.rank[root_x] += 1
        
        return True  # Successfully merged
    
    def get_circuit_sizes(self):
        """Get the sizes of all circuits."""
        circuits = defaultdict(int)
        for i in range(len(self.parent)):
            root = self.find(i)
            circuits[root] = self.size[root]
        return list(circuits.values())


def solve_part1(filename, num_connections):
    """
    Solve the junction box problem Part 1.
    Connect the num_connections shortest pairs and return the product
    of the three largest circuit sizes.
    """
    boxes = parse_input(filename)
    n = len(boxes)
    
    print(f"Total junction boxes: {n}")
    
    # Create a min-heap of all pairwise distances
    print("Computing all pairwise distances...")
    distances = []
    for i in range(n):
        for j in range(i + 1, n):
            dist = distance(boxes[i], boxes[j])
            heapq.heappush(distances, (dist, i, j))
    
    print(f"Total possible connections: {len(distances)}")
    
    # Initialize Union-Find
    uf = UnionFind(n)
    
    # Connect the shortest num_connections pairs
    connections_made = 0
    for _ in range(num_connections):
        if not distances:
            break
        
        dist, i, j = heapq.heappop(distances)
        if uf.union(i, j):
            connections_made += 1
    
    print(f"Connections made: {connections_made}")
    
    # Get circuit sizes
    circuit_sizes = uf.get_circuit_sizes()
    circuit_sizes.sort(reverse=True)
    
    print(f"Number of circuits: {len(circuit_sizes)}")
    print(f"Three largest circuits: {circuit_sizes[:3]}")
    
    # Multiply the three largest
    result = circuit_sizes[0] * circuit_sizes[1] * circuit_sizes[2]
    return result


def solve_part2(filename):
    """
    Solve the junction box problem Part 2.
    Connect junction boxes until they're all in one circuit.
    Return the product of X coordinates of the last two boxes connected.
    """
    boxes = parse_input(filename)
    n = len(boxes)
    
    print(f"\nPart 2:")
    print(f"Total junction boxes: {n}")
    
    # Create a min-heap of all pairwise distances
    print("Computing all pairwise distances...")
    distances = []
    for i in range(n):
        for j in range(i + 1, n):
            dist = distance(boxes[i], boxes[j])
            heapq.heappush(distances, (dist, i, j))
    
    # Initialize Union-Find
    uf = UnionFind(n)
    
    # Connect pairs until all are in one circuit
    connections_made = 0
    last_connection = None
    
    while len(uf.get_circuit_sizes()) > 1:
        if not distances:
            break
        
        dist, i, j = heapq.heappop(distances)
        if uf.union(i, j):
            connections_made += 1
            last_connection = (i, j)
    
    print(f"Total connections made: {connections_made}")
    print(f"Number of circuits: {len(uf.get_circuit_sizes())}")
    
    if last_connection:
        i, j = last_connection
        x1, y1, z1 = boxes[i]
        x2, y2, z2 = boxes[j]
        print(f"Last connection: box {i} at ({x1},{y1},{z1}) and box {j} at ({x2},{y2},{z2})")
        result = x1 * x2
        print(f"X coordinates: {x1} * {x2} = {result}")
        return result
    
    return None


def main():
    # Part 1
    print("Part 1:")
    result1 = solve_part1('input_day8.txt', 1000)
    print(f"\nPart 1 Answer: {result1}")
    
    # Part 2
    result2 = solve_part2('input_day8.txt')
    print(f"\nPart 2 Answer: {result2}")


if __name__ == "__main__":
    main()
