import copy
import random
import sys


class Arc:
    def __init__(self, i, j):
        self.i = i
        self.j = j


class Board:
    def __init__(self, board):
        self.board = board
        self.domain = {}

    def give_domain(self):
        for r in range(9):
            for c in range(9):
                if self.board[r][c] == '.':
                    self.domain[(r, c)] = [x for x in range(1, 10)]
                else:
                    self.domain[(r, c)] = []
                    self.domain[(r, c)].append(self.board[r][c])


def board_to_string(board):
    s = ""
    for row_index in range(9):
        if row_index % 3 == 0 and row_index > 0:
            s += "- - - - - - - - - - - \n"
        for col_index in range(9):
            if col_index % 3 == 2 and col_index != 8:
                s += str(board[row_index][col_index]) + " | "
            elif col_index == 8:
                s += str(board[row_index][col_index]) + "\n"
            else:
                s += str(board[row_index][col_index]) + " "
    return s


def completed(b):
    current = b.board
    count_empty = 0
    for i in range(9):
        for j in range(9):
            if current[i][j] == '.':
                count_empty += 1
    return count_empty == 0


def add_arc(r, c):
    arc_list = []
    for r_index in range(9):
        if r_index != r:
            arc_list.append(Arc((r, c), (r_index, c)))

    for c_index in range(9):
        if c_index != c:
            arc_list.append(Arc((r, c), (r, c_index)))

    top_left_square_r = int(r / 3)
    top_left_square_c = int(c / 3)
    for r_i in range(top_left_square_r * 3, top_left_square_r * 3 + 3):
        for c_i in range(top_left_square_c * 3, top_left_square_c * 3 + 3):
            if r_i != r and c_i != c:
                arc_list.append(Arc((r, c), (r_i, c_i)))

    return arc_list


def arc_consistency(b):
    q = []
    for m in range(9):
        for n in range(9):
            q.extend(add_arc(m, n))

    while q:
        current_arc = q.pop(0)
        if revised(b, current_arc.i, current_arc.j):
            if len(b.domain[current_arc.i]) == 0:
                return False
            xi = current_arc.i
            xj = current_arc.j
            r_idx = xi[0]
            c_idx = xi[1]
            if len(b.domain[xi]) == 1:
                assignment = b.domain[xi][0]
                b.board[r_idx][c_idx] = assignment
            temp_li = add_arc(r_idx, c_idx)
            for arc in temp_li:
                xk = arc.j
                if xk != xj and Arc(xk, xi) not in q:
                    q.append(Arc(xk, xi))

    return True


def revised(b, square1, square2):
    rev = False
    r2 = square2[0]
    c2 = square2[1]
    for idx in range(len(b.domain[square1])):
        if b.domain[square1][idx] == b.board[r2][c2]:
            b.domain[square1].pop(idx)
            rev = True
            break
    return rev


# Return a list of minimum-remaining-value position on the board
def mrv(b):
    mrv_list = []
    curr_min = 9
    for pos in b.domain.keys(): 
        if len(b.domain[pos]) == 1:
            continue
        if len(b.domain[pos]) < curr_min:
            curr_min = len(b.domain[pos])
            mrv_list.clear()
            mrv_list.append(pos)
        elif len(b.domain[pos]) == curr_min:
            mrv_list.append(pos)
    return mrv_list


def backtracking_solver(b):
    if completed(b):
        return b
    curr_mrv = mrv(b)
    curr_index = int(random.random() * len(curr_mrv))
    curr_square = curr_mrv[curr_index]
    for val in b.domain[curr_square]:
        next_b = copy.deepcopy(b)
        r = curr_square[0]
        c = curr_square[1]
        next_b.board[r][c] = val
        if not arc_consistency(next_b):
            continue
        else:
            result = backtracking_solver(next_b)
            if result:
                return result
    return False


def solve():
    file = open(sys.argv[1], 'r')
    f = file.read().split()
    file.close()
    initial_board = []
    k = 0
    for i in range(9):
        row = []
        for j in range(9):
            if f[k] != '.':
                row.append(int(f[k]))
            else:
                row.append(f[k])
            k += 1
        initial_board.append(row)
    sudoku = Board(initial_board)
    sudoku.give_domain()
    print("Initial sudoku board:")
    print(board_to_string(sudoku.board))
    if not arc_consistency(sudoku):
        print("No solution for the given board")
        return
    if completed(sudoku):
        print("Completed board:")
        print(board_to_string(sudoku.board))
    else:
        result_sudoku = backtracking_solver(sudoku)
        print("Completed board:")
        print(board_to_string(result_sudoku.board))


solve()
