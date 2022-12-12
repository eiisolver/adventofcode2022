import heapq

class Node(object):
    def __init__(self, id, value, height):
        self.id = id
        self.value = value
        self.height = height
        self.neighbours = set()

    def add(self, n):
        self.neighbours.add(n)

    def can_go_to(self, n2):
        return n2.elevation() <= self.elevation() + 1

    def elevation(self):
        if self.height == 'S':
            return ord('a')
        elif self.height == 'E':
            return ord('z')
        else:
            return ord(self.height)

def dijkstra(graph, start_node):
    distance = len(graph) * [1e9]
    distance[start_node] = 0
    queue = [(0, start_node)]
    while len(queue) > 0:
        curr_dist, v = heapq.heappop(queue)
        if curr_dist > distance[v]:
            continue
        for n2 in graph[v].neighbours:
            w = n2.id
            dist_v = curr_dist + n2.value
            if dist_v < distance[w]:
                distance[w] = dist_v
                heapq.heappush(queue, (dist_v, w))
    return distance

def get_node_id(col, row, w, h):
    if 0 <= col < w and 0 <= row < h:
        return row * w + col
    return -1

data = open('12_input.txt', 'r').read().splitlines()

# Create nodes
graph = []
w = len(data[0])
h = len(data)
end = None
for row in range(h):
    for col in range(w):
        id = get_node_id(col, row, w, h)
        n = Node(id, 1, data[row][col])
        graph.append(n)
        if n.height == 'E':
            end = id

# Create edges
for row in range(h):
    for col in range(w):
        id = get_node_id(col, row, w, h)
        n = graph[id]
        for dx, dy in [ (0, 1), (1, 0), (0, -1), (-1, 0)]:
            id2 = get_node_id(col + dx, row + dy, w, h)
            if id2 >= 0:
                n2 = graph[id2]
                if n.can_go_to(n2):
                    n.add(n2)
print("Part 1:", min(dijkstra(graph, n.id)[end] for n in graph if n.height == "S"))
print("Part 2:", min(dijkstra(graph, n.id)[end] for n in graph if n.height in ("a", "S")))
