import sys
import time

from Puzzle import Puzzle
import algorithms as a


def validate_options(options):
    return set(options) == {"L", "R", "U", "D"} and len(options) == 4

def main():
    algorithm = sys.argv[1]
    options = sys.argv[2]
    input_file = sys.argv[3]
    output_file = sys.argv[4]
    statisitcs_file = sys.argv[5]

    if algorithm != "bfs" and algorithm != "dfs" and algorithm != "astr":
        raise Exception("Invalid algorithm")

    if (algorithm == "bfs" or algorithm == "dfs") and not validate_options(options):
        raise Exception("Invalid algorithm options")

    if algorithm == "astr" and options not in ["manh", "hamm"]:
        raise Exception("Invalid algorithm options")

    puzzle_numbers = []
    with open(input_file, "r") as file:
        next(file)
        for line in file:
            row = list(map(int, line.split()))
            puzzle_numbers.append(row)

    puzzle = Puzzle(puzzle_numbers)
    puzzle.print_grid()

    max_depth = None
    if algorithm == "bfs":
        time_start = time.perf_counter()
        solution, visited, checked_count = a.bfs(puzzle, options)
        max_depth = len(solution)
        time_end = time.perf_counter()
    elif algorithm == "dfs":
        time_start = time.perf_counter()
        solution, visited, max_depth, checked_count = a.dfs(puzzle, options)
        time_end = time.perf_counter()
    elif algorithm == "astr":
        if options == "manh":
            time_start = time.perf_counter()
            solution, visited, checked_count, max_depth = a.astar(puzzle, "LDUR", a.manhattan)
            time_end = time.perf_counter()
        elif options == "hamm":
            time_start = time.perf_counter()
            solution, visited, checked_count, max_depth = a.astar(puzzle, "LDUR", a.hamming)
            time_end = time.perf_counter()

    with open(output_file, "w") as file:
        if solution is None:
            file.write("-1")
        else:
            file.write(str(len(solution)) + "\n" + str(solution))

    with open(statisitcs_file, "w") as file:
        file.write(str(len(solution)) + "\n")

        # Write solution path
        file.write(str(visited) + "\n")

        # Write number of visited states
        file.write(str(checked_count) + '\n')

        # Write max depth if available, otherwise n/d
        if max_depth is not None:
            file.write(str(max_depth) + '\n')
        else:
            file.write('n/d\n')

        # Write execution time in milliseconds
        file.write(str(round((time_end - time_start) * 1000, 3)) + '\n')

    print(solution)

if __name__ == '__main__':
    main()