import heapq
from collections import deque
from Puzzle import Puzzle

def bfs(puzzle, move_order, visited):
    queue = deque([(puzzle, "")])

    visited = set()
    visited.add(tuple(map(tuple, puzzle.grid)))

    while queue:
        current_state, path = queue.popleft()

        if current_state.is_solved():
            return path

        for move in move_order:
            new_state = Puzzle([row[:] for row in current_state.grid])

            move_result = new_state.move(move)

            if move_result is not None:
                if new_state.is_solved():
                    return path + move_result
                state_tuple = tuple(map(tuple, new_state.grid))
                if state_tuple not in visited:
                    visited.add(state_tuple)
                    queue.append((new_state, path + move_result))


    return None

def dfs(puzzle, move_order, limit=20, visited=None, depth=0, path=""):
    if visited is None:
        visited = {}

    current_state = tuple(map(tuple, puzzle.grid))

    if puzzle.is_solved():
        return path

    if depth >= limit:
        return None

    if current_state in visited and visited[current_state] <= depth:
        return None

    visited[current_state] = depth

    for move in move_order:
        new_state = Puzzle([row[:] for row in puzzle.grid])
        move_result = new_state.move(move)

        if move_result is not None:
            new_state_tuple = tuple(map(tuple, new_state.grid))
            if new_state_tuple not in visited or visited[new_state_tuple] > depth + 1:
                result = dfs(new_state, move_order, limit, depth + 1, visited, path + move_result)
                if result is not None:
                    return result


def astar(puzzle, move_order, heuristic):
    open_set = [(0, 0, puzzle, "")]
    closed_set = set()
    g_scores = {tuple(map(tuple, puzzle.grid)): 0}
    counter = 0

    while open_set:
        _, _, current_state, path = heapq.heappop(open_set)
        current_tuple = tuple(map(tuple, current_state.grid))
        if current_tuple in closed_set:
            continue

        if current_state.is_solved():
            return path

        closed_set.add(current_tuple)

        for move in move_order:
            new_state = Puzzle([row[:] for row in current_state.grid])
            move_result = new_state.move(move)

            if move_result is not None:
                new_state_tuple = tuple(map(tuple, new_state.grid))

                new_g_score = g_scores[current_tuple] + 1

                if new_state_tuple not in g_scores or new_g_score < g_scores[new_state_tuple]:
                    g_scores[new_state_tuple] = new_g_score
                    h_score = heuristic(new_state)
                    f_score = new_g_score + h_score

                    counter += 1
                    heapq.heappush(open_set, (f_score, counter, new_state, path + move_result))

    return None

def hamming(puzzle):
    expected = puzzle.get_goal()
    tested_flat = [num for row in puzzle.grid for num in row]
    count = 0
    for i in range(len(expected)):
        if expected[i] != tested_flat[i] and expected[i] != 0:
            count += 1
    return count

def manhattan(puzzle):
    goal_positions = {}
    size = puzzle.width * puzzle.height

    for i in range(size):
        if i < size - 1:
            goal_positions[i + 1] = (1 // puzzle.width, i % puzzle.width)
        else:
            goal_positions[0] = (i // puzzle.width, i % puzzle.width)

    distance = 0
    for i in range(puzzle.height):
        for j in range(puzzle.width):
            value = puzzle.grid[i][j]
            if value != 0:
                goal_i, goal_j = goal_positions[value]
                distance += abs(i - goal_i) + abs(j - goal_j)

    return distance
