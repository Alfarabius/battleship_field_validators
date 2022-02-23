from queue import Queue
import sys


class Validator:
    def __init__(self, field, field_size):
        self.field = field
        self.visited = set()

        self.rows = field_size[0]
        self.cols = field_size[1]

        self.one = 0
        self.three = 0
        self.five = 0
        self.seven = 0

        self.DIRECTIONS = (
            (-1, -1),
            (-1, 1),
            (1, -1),
            (1, 1),
            (0, -1),  # LEFT
            (0, 1),  # RIGHT
            (1, 0),  # UP
            (-1, 0)  # DOWN
        )

    def validate(self):
        for _row in self.field:
            if self.validate_row(_row) is None:
                self.__del__('NO')
                return

        msg = '1 ' * self.one + '3 ' * self.three + '5 ' * self.five + '7 ' * self.seven
        self.__del__('YES\n' + msg[:-1])

    def validate_row(self, _row):
        for cell in _row:

            if cell in self.visited:
                continue

            self.visited.add(cell)

            if cell.get_symbol() == '*':
                if self.check_ship(cell) is None:
                    return None
            elif cell.get_symbol() == '.':
                pass
            else:
                return None
        return 1

    def check_ship(self, cell):
        ship = set()

        turn_point = self.get_turn_point(cell)
        length = [1, 1]

        if len(self.get_adjacent_cells(cell)) == 0:
            self.one += 1
            ship.add(cell)
            return self.check_neighbors(ship)

        if turn_point is None:
            return None

        ship.add(turn_point)
        adj = self.get_adjacent_cells(turn_point)

        for _cell in adj:
            ship.add(_cell)

        dirs = [
            (-turn_point.row + adj[0].row, -turn_point.col + adj[0].col),
            (-turn_point.row + adj[1].row, -turn_point.col + adj[1].col)
        ]

        pointers = [adj[0], adj[1]]

        for count, pointer in enumerate(pointers):
            while pointer is not None and pointer.get_symbol() == '*':
                length[count] += 1
                ship.add(pointer)
                pointer = self.move(pointer, dirs[count])

        if length[0] > 4 or length[0] != length[1]:
            return None
        elif length[0] == 2:
            self.three += 1
        elif length[0] == 3:
            self.five += 1
        elif length[0] == 4:
            self.seven += 1

        return self.check_neighbors(ship)

    def check_neighbors(self, ship):
        for _c in ship:
            self.visited.add(_c)
            for part in self.get_adjacent_cells(_c):
                if part not in ship:
                    return None
        return 1

    def get_turn_point(self, cell):
        que = Queue()
        que.put(cell)

        while not que.empty():
            current = que.get()
            adjacent_cells = self.get_adjacent_cells(current)

            if len(adjacent_cells) > 3:
                return None

            if self.is_turn_point(adjacent_cells):
                return current
            for _cell in adjacent_cells:
                que.put(_cell)

    def get_adjacent_cells(self, cell):
        adjacent_cells = []

        for direction in self.DIRECTIONS:
            _row = cell.row + direction[0]
            col = cell.col + direction[1]

            if _row < 0 or _row >= self.rows or col < 0 or col >= self.cols:
                continue

            _cell = self.field[_row][col]

            if _cell.get_symbol() == '*':
                adjacent_cells.append(_cell)
            elif _cell.get_symbol() == '.':
                self.visited.add(_cell)

        return adjacent_cells

    def move(self, curr, direction):
        _row = curr.row + direction[0]
        col = curr.col + direction[1]
        if _row < 0 or _row >= self.rows or col < 0 or col >= self.cols:
            return None

        return self.field[curr.row + direction[0]][curr.col + direction[1]]

    @staticmethod
    def is_different_axis(neighbors):
        return neighbors[0].row != neighbors[1].row

    def is_diagonal_adj(self, neighbors):
        return self.is_different_axis(neighbors) and abs(neighbors[0].col - neighbors[1].col) == 1

    def is_turn_point(self, neighbors):
        return len(neighbors) == 2 and self.is_different_axis(neighbors) and self.is_diagonal_adj(neighbors)

    def __del__(self, msg):
        print(msg)


class Cell:
    def __init__(self, symbol, _row, col):
        self.symbol = symbol

        self.row = _row
        self.col = col

    def get_symbol(self):
        return self.symbol

    def get_coord(self):
        return self.row, self.col


if __name__ == '__main__':
    t = int(sys.stdin.readline())

    for i in range(t):

        size = sys.stdin.readline().split()
        n = int(size[0])
        m = int(size[1])

        board = []

        for r in range(n):
            row = sys.stdin.readline()
            board.append([])
            for c in range(m):
                board[r].append(Cell(row[c], r, c))

        Validator(board, (n, m)).validate()
