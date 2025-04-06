import heapq
from collections import deque
from Puzzle import Puzzle

def bfs(puzzle, move_order):
    queue = deque([(puzzle, "")])

    visited = set()
    visited.add(tuple(map(tuple, puzzle.grid)))
    visited_count = 1
    checked_count = 1

    while queue:
        current_state, path = queue.popleft()

        if current_state.is_solved():
            return path, visited_count, checked_count

        for move in move_order:
            new_state = Puzzle([row[:] for row in current_state.grid])
            move_result = new_state.move(move)

            checked_count += 1

            if move_result is not None:
                if new_state.is_solved():
                    return path + move_result, visited_count + 1, checked_count

                state_tuple = tuple(map(tuple, new_state.grid))
                if state_tuple not in visited:
                    visited.add(state_tuple)
                    visited_count += 1
                    queue.append((new_state, path + move_result))

    return None, visited_count, checked_count


def dfs(puzzle, move_order, limit=20):
    visited = {}
    max_depth = [0]
    checked_count = [0]
    result, found = dfs_helper(puzzle, move_order, limit, visited, 0, "", max_depth, checked_count)
    return result, len(visited), max_depth[0], checked_count[0]

def dfs_helper(puzzle, move_order, limit, visited, depth, path, max_depth, checked_count):
    max_depth[0] = max(max_depth[0], depth)
    checked_count[0] += 1

    if puzzle.is_solved():
        return path, True

    if depth >= limit:
        return None, False

    current_state = tuple(map(tuple, puzzle.grid))
    if current_state in visited and visited[current_state] <= depth:
        return None, False

    visited[current_state] = depth

    for move in move_order:
        new_state = Puzzle([row[:] for row in puzzle.grid])
        move_result = new_state.move(move)

        if move_result is not None:
            new_state_tuple = tuple(map(tuple, new_state.grid))
            if new_state_tuple not in visited or visited[new_state_tuple] > depth + 1:
                result, found = dfs_helper(new_state, move_order, limit, visited, depth + 1, path + move_result,
                                           max_depth, checked_count)
                if found:
                    return result, True

    return None, False


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
            goal_positions[i + 1] = (i // puzzle.width, i % puzzle.width)
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

def astar(puzzle, move_order, heuristic_func):
    queue = [(0, 0, puzzle, "")]
    visited = set()
    g_scores = {tuple(map(tuple, puzzle.grid)): 0}
    counter = 0
    visited_count = 1
    checked_count = 1
    max_depth_reached = 0

    while queue:
        _, _, current_state, path = heapq.heappop(queue)
        current_tuple = tuple(map(tuple, current_state.grid))
        if current_tuple in visited:
            continue

        if current_state.is_solved():
            return path, visited_count, checked_count, max_depth_reached

        visited.add(current_tuple)

        for move in move_order:
            new_state = Puzzle([row[:] for row in current_state.grid])
            move_result = new_state.move(move)

            checked_count += 1

            if move_result is not None:
                new_tuple = tuple(map(tuple, new_state.grid))

                new_g_score = g_scores[current_tuple] + 1
                max_depth_reached = max(max_depth_reached, new_g_score)

                is_new_state = new_tuple not in g_scores and new_tuple not in visited
                if is_new_state or new_g_score < g_scores.get(new_tuple, float('inf')):
                    if is_new_state:
                        visited_count += 1

                    g_scores[new_tuple] = new_g_score
                    h_score = heuristic_func(new_state)
                    f_score = new_g_score + h_score

                    counter += 1
                    heapq.heappush(queue, (f_score, counter, new_state, path + move_result))

    return None, visited_count, checked_count, max_depth_reached