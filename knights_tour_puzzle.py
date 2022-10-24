class Board:
    def __init__(self, board_x, board_y, space):
        self.board_x = board_x
        self.board_y = board_y
        self.space = space
        self.grid = [['_' * space for _ in range(board_x)] for _ in range(board_y)]
        self.possible_moves = [[2, 1], [2, -1], [1, 2], [-1, 2], [-2, 1], [-2, -1], [1, -2], [-1, -2]]
        self.history_moves = list()
        self.last_x = 0
        self.last_y = 0

    def set_position(self, pos_x, pos_y):
        self.grid[pos_y][pos_x] = ' ' * (self.space - 1) + 'X'

    def __str__(self):
        board = " " + "-" * (self.board_x * (self.space + 1) + 3) + "\n"
        for i in range(self.board_y):
            board += "{}| {} |".format(self.board_y - i, " ".join(self.grid[i])) + "\n"
        board += " " + "-" * (self.board_x * (self.space + 1) + 3) + "\n"
        nums = list()
        for i in range(1, self.board_x + 1):
            nums.append("{}{}".format(" " * self.space, i))
        board += "  {}".format("".join(nums))
        return board

    def set_move(self, pos_x, pos_y, counter):
        sum = 0
        for move in self.possible_moves:
            move_x, move_y = move
            if 0 <= pos_y + move_y < self.board_y and 0 <= pos_x + move_x < self.board_x:
                if counter == 1:
                    if not [pos_x + move_x, pos_y + move_y] in self.history_moves:
                        sum += 1
                else:
                    self.grid[pos_y + move_y][pos_x + move_x] = "{}{}".format(" " * (self.space - 1), self.set_move(pos_x + move_x, pos_y + move_y, counter + 1))
        return sum - 1

    def has_solution(self, pos_x, pos_y, count_move):
        if count_move == board_y * board_x:
            return True
        for move in self.possible_moves:
            move_x, move_y = move
            if 0 <= pos_y + move_y < self.board_y and 0 <= pos_x + move_x < self.board_x and self.grid[pos_y + move_y][pos_x + move_x].strip("_") == "":
                self.grid[pos_y + move_y][pos_x + move_x] = ' ' * (space - len(str(count_move))) + str(count_move)
                if self.has_solution(pos_x + move_x, pos_y + move_y, count_move + 1):
                    return True
                self.grid[pos_y + move_y][pos_x + move_x] = '_' * space
        return False

    def count_moves(self, pos_x, pos_y):
        sum = 0
        for move in self.possible_moves:
            move_x, move_y = move
            if 0 <= pos_y + move_y < self.board_y and 0 <= pos_x + move_x < self.board_x:
                if not [pos_x + move_x, pos_y + move_y] in self.history_moves:
                        sum += 1
        return sum

    def board_moves(self, pos_x, pos_y):
        self.history_moves.append([pos_x, pos_y])
        for i in range(board_y):
            for j in range(board_x):
                if [j, i] in self.history_moves:
                    self.grid[i][j] = ' ' * (space - 1) + "*"


def check_board_size():
    while True:
        board_size = input("Enter your board dimensions:").split()
        try:
            board_x = int(board_size[0])
            board_y = int(board_size[1])
            if len(board_size) != 2:
                raise ValueError
            elif not (board_x > 0 and board_y > 0):
                raise IndexError
        except (ValueError, IndexError):
            print("Invalid dimensions!")
            continue
        break
    return board_x, board_y


def check_start(board_x, board_y, counter):
    while True:
        if counter == 0:
            start = input("Enter the knight's starting position: ").split()
        else:
            start = input("Enter your next move: ").split()
        try:
            pos_x = int(start[0]) - 1
            pos_y = board_y - int(start[1])
            if [pos_x, pos_y] in board.history_moves:
                raise IndexError
            if counter != 0:
                if not [pos_x - board.last_x, pos_y - board.last_y] in board.possible_moves:
                    raise IndexError
            if len(start) != 2:
                raise ValueError
            elif not (0 <= pos_x < board_x and 0 <= pos_y < board_y):
                raise IndexError
        except(ValueError, IndexError):
            if counter == 0:
                print("Invalid dimensions!")
            else:
                print("Invalid move!", end = ' ')
            continue
        break
    board.last_x = pos_x
    board.last_y = pos_y
    return pos_x, pos_y

def solution():
    while True:
        sol = input("Do you want to try the puzzle? (y/n):")
        has_sol = board.has_solution(pos_x, pos_y, 1)
        if sol == "y":
            if not has_sol:
                print("No solution exists!")
                return False
            else:
                return True
        if sol == "n":
            if not has_sol:
                print("No solution exists!")
                return False
            else:
                print("Here's the solution!")
                print(board)
                return False
        else:
            print("Invalid input!")
            continue

def calc_space(board_x, board_y):
    return len(str(board_x * board_y))


board_x, board_y = check_board_size()
space = calc_space(board_x, board_y)
board = Board(board_x, board_y, space)
counter = 0
while True:
    pos_x, pos_y = check_start(board_x, board_y, counter)
    board.grid = [['_' * space for _ in range(board_x)] for _ in range(board_y)]
    board.grid[pos_y][pos_x] = ' ' * (space - 1) + "0"
    if counter == 0:
        if not solution():
            break
    board.grid = [['_' * space for _ in range(board_x)] for _ in range(board_y)]
    board.set_move(pos_x, pos_y, 0)
    board.board_moves(pos_x, pos_y)
    board.set_position(pos_x, pos_y)
    print(board)
    counter += 1
    if counter == board_x * board_y:
        print("What a great tour! Congratulations!")
        break
    elif counter != 0 and board.count_moves(pos_x, pos_y) == 0:
        print("No more possible moves!")
        print("Your knight visited {} squares!".format(counter))
        break




