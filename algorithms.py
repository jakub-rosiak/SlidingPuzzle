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

def dfs(puzzle, move_order, limit=20, depth=0, visited=None, path=""):
    if visited is None:
        visited = {}

    print(type(visited))
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
                result = dfs(new_state, move_order, limit, depth + 1, visited, path + move_result)
                if result is not None:
                    return result
