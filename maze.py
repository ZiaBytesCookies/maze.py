import sys
import argparse
import random
import time
import logging
from collections import deque

# Wall directions bitmasks
N, S, E, W = 1, 2, 4, 8
DX = {E: 1, W: -1, N: 0, S: 0}
DY = {E: 0, W: 0, N: -1, S: 1}
OPPOSITE = {N: S, S: N, E: W, W: E}


def parse_args():
    parser = argparse.ArgumentParser(description="Maze generator and solver")
    parser.add_argument("--width", type=int, default=21, help="Maze width in cells")
    parser.add_argument("--height", type=int, default=11, help="Maze height in cells")
    parser.add_argument("--seed", type=int, help="Random seed")
    parser.add_argument("--solve", action="store_true", help="Solve the maze")
    parser.add_argument("--animate", action="store_true", help="Animate carving and solving")
    parser.add_argument("--export", type=str, help="Export maze to text file")
    parser.add_argument("--test", action="store_true", help="Run self-tests")
    return parser.parse_args()


def init_grid(width, height):
    grid = [[N | S | E | W for _ in range(width)] for _ in range(height)]
    return grid


def carve_maze(grid, x=0, y=0, animate=False):
    width = len(grid[0])
    height = len(grid)
    stack = [(x, y)]
    visited = {(x, y)}
    while stack:
        cx, cy = stack[-1]
        neighbors = []
        for direction in (N, S, E, W):
            nx, ny = cx + DX[direction], cy + DY[direction]
            if 0 <= nx < width and 0 <= ny < height and (nx, ny) not in visited:
                neighbors.append((direction, nx, ny))
        if neighbors:
            direction, nx, ny = random.choice(neighbors)
            grid[cy][cx] &= ~direction
            grid[ny][nx] &= ~OPPOSITE[direction]
            visited.add((nx, ny))
            stack.append((nx, ny))
            if animate:
                render_and_sleep(grid, None)
        else:
            stack.pop()


def solve_maze(grid, start=(0, 0), goal=None, animate=False):
    width, height = len(grid[0]), len(grid)
    if goal is None:
        goal = (width - 1, height - 1)
    queue = deque([start])
    came_from = {start: None}
    while queue:
        current = queue.popleft()
        if current == goal:
            break
        x, y = current
        for direction in (N, S, E, W):
            if not grid[y][x] & direction:
                nx, ny = x + DX[direction], y + DY[direction]
                if (0 <= nx < width and 0 <= ny < height and (nx, ny) not in came_from):
                    came_from[(nx, ny)] = current
                    queue.append((nx, ny))
        if animate:
            path_prog = reconstruct_path(came_from, current)
            render_and_sleep(grid, path_prog)
    return reconstruct_path(came_from, goal)


def reconstruct_path(came_from, goal):
    path, current = [], goal
    while current is not None:
        path.append(current)
        current = came_from.get(current)
    path.reverse()
    return path


def render(grid, path=None):
    width, height = len(grid[0]), len(grid)
    maze_rows, maze_cols = 2*height + 1, 2*width + 1
    maze = [['█'] * maze_cols for _ in range(maze_rows)]
    for y in range(height):
        for x in range(width):
            mx, my = 2*x + 1, 2*y + 1
            maze[my][mx] = ' '
            if not grid[y][x] & N:
                maze[my-1][mx] = ' '
            if not grid[y][x] & S:
                maze[my+1][mx] = ' '
            if not grid[y][x] & W:
                maze[my][mx-1] = ' '
            if not grid[y][x] & E:
                maze[my][mx+1] = ' '
    if path:
        for (x, y) in path:
            mx, my = 2*x + 1, 2*y + 1
            if (x, y) != path[0] and (x, y) != path[-1]:
                maze[my][mx] = '·'
        sx, sy = path[0]
        ex, ey = path[-1]
        maze[2*sy + 1][2*sx + 1] = 'S'
        maze[2*ey + 1][2*ex + 1] = 'E'
    else:
        maze[1][1] = 'S'
        maze[-2][-2] = 'E'
    return [''.join(row) for row in maze]


def render_and_sleep(grid, path=None):
    print("\033[H", end='')
    for row in render(grid, path):
        print(row)
    time.sleep(0.05)


def run_self_tests():
    for w, h in [(3, 3), (5, 5), (7, 7)]:
        grid = init_grid(w, h)
        carve_maze(grid)
        visited = set()
        def dfs(x, y):
            visited.add((x, y))
            for d in (N, S, E, W):
                if not grid[y][x] & d:
                    nx, ny = x + DX[d], y + DY[d]
                    if (nx, ny) not in visited:
                        dfs(nx, ny)
        dfs(0, 0)
        assert len(visited) == w*h, f"Disconnected maze {w}x{h}"
        path = solve_maze(grid)
        assert path[0] == (0, 0) and path[-1] == (w-1, h-1), f"No path for maze {w}x{h}"
    print("All self-tests passed!")


def main():
    args = parse_args()
    if args.seed is not None:
        random.seed(args.seed)
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    if args.test:
        run_self_tests()
        return
    grid = init_grid(args.width, args.height)
    t0 = time.perf_counter()
    carve_maze(grid, animate=args.animate)
    t1 = time.perf_counter()
    path = None
    if args.solve:
        path = solve_maze(grid, animate=args.animate)
    t2 = time.perf_counter()
    maze_lines = render(grid, path)
    for line in maze_lines:
        print(line)
    logging.info(f"Generated in {t1-t0:.3f}s; Solved in {t2-t1:.3f}s; Path length {len(path) if path else 0}")
    if args.export:
        with open(args.export, "w") as f:
            f.write("\n".join(maze_lines))

if __name__ == "__main__":
    main()
