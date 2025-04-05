class Puzzle:
    def __init__(self, grid):
        self.grid = grid
        self.width = len(grid[0])
        self.height = len(grid)
        self.zero = self.find_zero()

    def find_zero(self):
        for i in range(self.height):
            for j in range(self.width):
                if self.grid[i][j] == 0:
                    return i, j
        return None

    def move_left(self):
        i, j = self.zero
        if j > 0:
            self.grid[i][j], self.grid[i][j-1] = self.grid[i][j-1], self.grid[i][j]
            self.zero = (i, j-1)
            return 'L'
        return None

    def move_right(self):
        i, j = self.zero
        if j < self.width-1:
            self.grid[i][j], self.grid[i][j+1] = self.grid[i][j+1], self.grid[i][j]
            self.zero = (i, j+1)
            return 'R'
        return None

    def move_up(self):
        i, j = self.zero
        if i > 0:
            self.grid[i][j], self.grid[i-1][j] = self.grid[i-1][j], self.grid[i][j]
            self.zero = (i-1, j)
            return 'U'
        return None

    def move_down(self):
        i, j = self.zero
        if i < self.height - 1:
            self.grid[i][j], self.grid[i+1][j] = self.grid[i+1][j], self.grid[i][j]
            self.zero = (i+1, j)
            return 'D'
        return None

    def move(self, move):
        match move:
            case "L":
                return self.move_left()
            case "R":
                return self.move_right()
            case "U":
                return self.move_up()
            case "D":
                return self.move_down()
        return None

    def is_solved(self):
        expected = list(range(1, self.height * self.width)) + [0]
        flat_grid = [num for row in self.grid for num in row]
        return flat_grid == expected

    def print_grid(self):
        for row in self.grid:
            print(" ".join(map(str, row)))
        print()

    def get_goal(self):
        return list(range(1, self.height * self.width)) + [0]