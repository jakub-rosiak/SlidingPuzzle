from Puzzle import Puzzle
from algorithms import bfs, dfs, reconstruct_solution
import sys

sys.setrecursionlimit(1000000)

grids = list()

grids.append([
    [1, 2, 3],
    [4, 5, 6],
    [7, 0, 8]
])

grids.append([
    [1, 2, 3],
    [4, 5, 0],
    [7, 8, 6]
])

grids.append([
    [1, 3, 0],
    [4, 2, 5],
    [7, 8, 6]
])

grids.append([
    [1, 3, 5],
    [4, 0, 8],
    [7, 2, 6]
])

grids.append([
    [8, 6, 7],
    [2, 5, 4],
    [3, 0, 1]
])

grids.append([
    [8, 6, 7],
    [2, 5, 4],
    [0, 3, 1]
])

goal = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 0]
]


for index, grid in enumerate(grids):
    print(f"Solving for grid {index + 1} with BFS")
    puzzle = Puzzle(grid)

    solution = bfs(puzzle, ["L","R","U","D"])

    print(solution)

for index, grid in enumerate(grids):
    print(f"Solving for grid {index + 1} with DFS")
    puzzle = Puzzle(grid)

    visited = set()
    parent_map = {}
    solution = dfs(puzzle, ["L","R","U","D"], visited, parent_map, 0, 100)
    if solution is not None:
        reconstructed = reconstruct_solution(puzzle, goal, parent_map)
        print("".join(reconstructed))
    else:
        print("No solution found")
