from collections import deque
from Puzzle import Puzzle
import heapq

def bfs(puzzle, move_order):
    queue = deque([(puzzle, "")])

    visited = set()
    visited.add(tuple(map(tuple, puzzle.grid)))

    while queue:
        current_state, path = queue.popleft()

        if current_state.is_solved():
            return path

        for move in move_order:
            new_state = Puzzle([row[:] for row in current_state.grid])

            move_result = None
            match move:
                case "L":
                    move_result = new_state.move_left()
                case "R":
                    move_result = new_state.move_right()
                case "U":
                    move_result = new_state.move_up()
                case "D":
                    move_result = new_state.move_down()

            if move_result is not None:
                if new_state.is_solved():
                    return path + move_result
                state_tuple = tuple(map(tuple, new_state.grid))
                if state_tuple not in visited:
                    visited.add(state_tuple)
                    queue.append((new_state, path + move_result))


    return None

def dfs(puzzle, move_order, visited=None, parent_map=None, depth=0, limit=20):
    if visited is None:
        visited = {}

    if parent_map is None:
        parent_map = {}

    if puzzle.is_solved():
        return [puzzle]

    if depth >= limit:
        return None

    current_state = tuple(map(tuple, puzzle.grid))

    if current_state in visited and visited[current_state] <= depth:
        return None

    visited[current_state] = depth

    for move in move_order:
        new_state = Puzzle([row[:] for row in puzzle.grid])
        move_result = None
        match move:
            case "L":
                move_result = new_state.move_left()
            case "R":
                move_result = new_state.move_right()
            case "U":
                move_result = new_state.move_up()
            case "D":
                move_result = new_state.move_down()

        if move_result is not None:
            new_state_tuple = tuple(map(tuple, new_state.grid))
            if new_state_tuple not in visited or visited[new_state_tuple] > depth + 1:
                parent_map[new_state_tuple] = (current_state, move)
                result = dfs(new_state, move_order, visited, parent_map, depth + 1, limit)
                if result is not None:
                    return [puzzle] + result
    return None

def reconstruct_solution(puzzle, goal, parent_map):
    solution = []
    state = tuple(map(tuple, goal))

    while state != tuple(map(tuple, puzzle.grid)):
        parent_state, move = parent_map[state]
        solution.append(move)
        state = parent_state

    solution.reverse()
    return solution
