import random
import heapq
from collections import deque


def get_neighbors(pos, n):
    """Return 4-direction neighbors within grid bounds."""
    r, c = pos
    for dr, dc in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
        nr, nc = r + dr, c + dc
        if 0 <= nr < n and 0 <= nc < n:
            yield (nr, nc)


def get_neighbors_cost(pos, n):
    """Return neighbors and movement cost (8-direction with diagonals)."""
    r, c = pos
    for dr, dc in [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1)]:
        nr, nc = r + dr, c + dc
        if 0 <= nr < n and 0 <= nc < n:
            cost = 1 if dr == 0 or dc == 0 else (2**0.5)
            yield (nr, nc), cost


def get_heuristic(a, b, method):
    """Compute heuristic distance between a and b using the specified method."""
    dx = abs(a[0] - b[0])
    dy = abs(a[1] - b[1])
    if method == 'Euclidean':
        return (dx*dx + dy*dy) ** 0.5
    elif method == 'Manhattan':
        return dx + dy
    elif method == 'Chebyshev':
        return max(dx, dy)
    elif method == 'Octile':
        f = 2**0.5 - 1
        return f * min(dx, dy) + abs(dx - dy)
    elif method == 'Tie-breaking':
        return (dx + dy) * (1 + 1e-3)
    elif method == 'Angle Euclidean':
        return (dx*dx + dy*dy) ** 0.5 * (1 + 1e-3)
    return 0


def bfs(grid, start, goal):
    """Breadth-First Search on a binary grid."""
    n = len(grid)
    visited = {start}
    parent = {start: None}
    queue = deque([start])
    while queue:
        u = queue.popleft()
        if u == goal:
            break
        for v in get_neighbors(u, n):
            if v not in visited and grid[v[0]][v[1]] == 0:
                visited.add(v)
                parent[v] = u
                queue.append(v)
    else:
        return []
    path = []
    node = goal
    while node is not None:
        path.append(node)
        node = parent[node]
    return path[::-1]


def dfs(grid, start, goal):
    """Depth-First Search on a binary grid."""
    n = len(grid)
    visited = set()
    parent = {start: None}
    stack = [start]
    while stack:
        u = stack.pop()
        if u in visited:
            continue
        visited.add(u)
        if u == goal:
            break
        for v in get_neighbors(u, n):
            if v not in visited and grid[v[0]][v[1]] == 0:
                parent[v] = u
                stack.append(v)
    else:
        return []
    path = []
    node = goal
    while node is not None:
        path.append(node)
        node = parent[node]
    return path[::-1]


def dijkstra(grid, start, goal):
    """Dijkstra's algorithm on a weighted grid."""
    n = len(grid)
    dist = {start: 0}
    parent = {}
    visited = set()
    heap = [(0, start)]
    while heap:
        d, u = heapq.heappop(heap)
        if u in visited:
            continue
        visited.add(u)
        if u == goal:
            break
        for v, cost in get_neighbors_cost(u, n):
            if grid[v[0]][v[1]] == 1:
                continue
            nd = d + cost
            if v not in dist or nd < dist[v]:
                dist[v] = nd
                parent[v] = u
                heapq.heappush(heap, (nd, v))
    if goal not in parent and start != goal:
        return []
    path = []
    node = goal
    while node != start:
        path.append(node)
        node = parent[node]
    path.append(start)
    return path[::-1]


def astar(grid, start, goal, heuristic):
    """A* search on a weighted grid with a chosen heuristic."""
    n = len(grid)
    g_score = {start: 0}
    f_score = {start: get_heuristic(start, goal, heuristic)}
    open_set = [(f_score[start], start)]
    came_from = {}
    closed = set()
    while open_set:
        _, current = heapq.heappop(open_set)
        if current == goal:
            break
        if current in closed:
            continue
        closed.add(current)
        for v, cost in get_neighbors_cost(current, n):
            if grid[v[0]][v[1]] == 1:
                continue
            tentative_g = g_score[current] + cost
            if v in g_score and tentative_g >= g_score[v]:
                continue
            came_from[v] = current
            g_score[v] = tentative_g
            f_score[v] = tentative_g + get_heuristic(v, goal, heuristic)
            heapq.heappush(open_set, (f_score[v], v))
    if goal not in came_from and start != goal:
        return []
    path = []
    node = goal
    while node != start:
        path.append(node)
        node = came_from[node]
    path.append(start)
    return path[::-1]


def add_loops(grid, n, loops):
    """Randomly remove walls between corridors to create loops in the maze."""
    # consider only interior walls
    walls = [(r, c) for r in range(1, n-1) for c in range(1, n-1) if grid[r][c] == 1]
    random.shuffle(walls)
    removed = 0
    for r, c in walls:
        if removed >= loops:
            break
        # if vertical wall between two open cells
        if grid[r-1][c] == 0 and grid[r+1][c] == 0:
            grid[r][c] = 0
            removed += 1
        # if horizontal wall between two open cells
        elif grid[r][c-1] == 0 and grid[r][c+1] == 0:
            grid[r][c] = 0
            removed += 1
    return grid


def add_targeted_loops(grid, start, end, loops=1):
    """Add loops specifically along the unique start-end path to create alternative routes."""
    # find the unique path using BFS
    path = bfs(grid, start, end)
    n = len(grid)
    candidates = []
    # look for wall cells adjacent to two distant nodes on the path
    for idx, (r, c) in enumerate(path):
        for dr, dc in [(1,0),(-1,0),(0,1),(0,-1)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < n and 0 <= nc < n and grid[nr][nc] == 1:
                # collect path neighbors of this wall
                neigh = []
                for dr2, dc2 in [(1,0),(-1,0),(0,1),(0,-1)]:
                    ar, ac = nr + dr2, nc + dc2
                    if (ar, ac) in path:
                        neigh.append(path.index((ar, ac)))
                if len(neigh) >= 2 and abs(neigh[0] - neigh[1]) > 1:
                    candidates.append((nr, nc))
    random.shuffle(candidates)
    for r, c in candidates[:loops]:
        grid[r][c] = 0
    return grid


def maze_recursive_backtracking(n):
    """Recursive backtracking maze generation."""
    grid = [[1] * n for _ in range(n)]
    def carve(r, c):
        dirs = [(2, 0), (-2, 0), (0, 2), (0, -2)]
        random.shuffle(dirs)
        for dr, dc in dirs:
            nr, nc = r + dr, c + dc
            if 0 <= nr < n and 0 <= nc < n and grid[nr][nc] == 1:
                grid[r + dr//2][c + dc//2] = 0
                grid[nr][nc] = 0
                carve(nr, nc)
    # start at (1,1) or (0,0) if small
    sr = 1 if n > 2 else 0
    sc = 1 if n > 2 else 0
    grid[sr][sc] = 0
    carve(sr, sc)
    return grid


def maze_prim(n):
    """Prim's algorithm maze generation."""
    grid = [[1] * n for _ in range(n)]
    sr, sc = random.randrange(1, n, 2), random.randrange(1, n, 2)
    grid[sr][sc] = 0
    walls = []
    for dr, dc in [(2, 0), (-2, 0), (0, 2), (0, -2)]:
        nr, nc = sr + dr, sc + dc
        if 0 <= nr < n and 0 <= nc < n:
            walls.append((nr, nc, (sr, sc)))
    while walls:
        idx = random.randrange(len(walls))
        r, c, (pr, pc) = walls.pop(idx)
        if grid[r][c] == 1 and grid[pr][pc] == 0:
            grid[(r+pr)//2][(c+pc)//2] = 0
            grid[r][c] = 0
            for dr, dc in [(2, 0), (-2, 0), (0, 2), (0, -2)]:
                nr, nc = r + dr, c + dc
                if 0 <= nr < n and 0 <= nc < n and grid[nr][nc] == 1:
                    walls.append((nr, nc, (r, c)))
    return grid


def maze_kruskal(n):
    """Kruskal's algorithm maze generation."""
    parent = {}
    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x
    def union(a, b):
        parent[find(a)] = find(b)
    cells = [(r, c) for r in range(1, n, 2) for c in range(1, n, 2)]
    for cell in cells:
        parent[cell] = cell
    edges = []
    for r, c in cells:
        if r + 2 < n:
            edges.append(((r, c), (r+2, c)))
        if c + 2 < n:
            edges.append(((r, c), (r, c+2)))
    random.shuffle(edges)
    grid = [[1] * n for _ in range(n)]
    for r, c in cells:
        grid[r][c] = 0
    for a, b in edges:
        if find(a) != find(b):
            union(a, b)
            ar, ac = a
            br, bc = b
            grid[(ar+br)//2][(ac+bc)//2] = 0
    return grid


def maze_eller(n):
    """Eller's algorithm maze generation, row-by-row perfect maze."""
    # initialize grid full of walls
    grid = [[1] * n for _ in range(n)]
    # early exit for small grids
    if n < 3:
        return [[0] * n for _ in range(n)]
    # cell positions are odd indices
    cell_rows = [i for i in range(n) if i % 2 == 1]
    cell_cols = [i for i in range(n) if i % 2 == 1]
    sets = {}
    next_set_id = 1
    # process each cell row
    for row_idx, y in enumerate(cell_rows):
        # open cells and assign sets
        for x in cell_cols:
            grid[y][x] = 0
            if (y, x) not in sets:
                sets[(y, x)] = next_set_id
                next_set_id += 1
        is_last = (row_idx == len(cell_rows) - 1)
        # join horizontally
        for i in range(len(cell_cols) - 1):
            x = cell_cols[i]
            x2 = cell_cols[i+1]
            if sets[(y, x)] != sets[(y, x2)]:
                if is_last or random.choice([True, False]):
                    # carve horizontal wall
                    grid[y][x+1] = 0
                    old_id = sets[(y, x2)]
                    new_id = sets[(y, x)]
                    # merge sets in this row
                    for xc in cell_cols:
                        if sets.get((y, xc)) == old_id:
                            sets[(y, xc)] = new_id
        # carve down vertically except last row
        if not is_last:
            next_y = cell_rows[row_idx + 1]
            # group by set id
            groups = {}
            for x in cell_cols:
                sid = sets[(y, x)]
                groups.setdefault(sid, []).append(x)
            new_sets = {}
            # carve vertical connections
            for sid, xs in groups.items():
                # choose at least one cell per group
                choices = [x for x in xs if random.choice([True, False])]
                if not choices:
                    choices = [random.choice(xs)]
                for x in choices:
                    # carve vertical wall
                    grid[y+1][x] = 0
                    # open cell below
                    grid[next_y][x] = 0
                    new_sets[(next_y, x)] = sid
            # assign new sets for next row cells
            for x in cell_cols:
                key = (next_y, x)
                if key not in new_sets:
                    new_sets[key] = next_set_id
                    next_set_id += 1
                    grid[next_y][x] = 0
            # update sets mapping to only next row
            sets = new_sets
    return grid


# Mapping of maze generation algorithms to their functions
MAZE_GENERATORS = {
    'Recursive Backtracking': maze_recursive_backtracking,
    'Prim': maze_prim,
    'Kruskal': maze_kruskal,
    'Eller': maze_eller
}


def generate_maze(n, algorithm='Recursive Backtracking', variant=None):
    """
    Generate a maze of size n x n.
    algorithm: one of ['Recursive Backtracking','Prim','Kruskal','Eller'].
    variant: optional variant name (stub for now).
    Returns a 2D grid with 0=open paths, 1=walls.
    """
    # select generator function
    try:
        gen_func = MAZE_GENERATORS[algorithm]
    except KeyError:
        raise ValueError(f'Unknown algorithm: {algorithm}')
    # generate perfect maze
    grid = gen_func(n)
    # add loops to create extra paths
    grid = add_loops(grid, n, loops=n)
    return grid
