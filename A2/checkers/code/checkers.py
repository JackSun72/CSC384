import math
import sys
map = {}
explored = set()
class State:
    def __init__(self, board, is_red_move):
        self.board = board
        self.is_red_move = is_red_move

    def move_down_left_one(self, row, col):
        if row <= 6 and col >= 1 and self.board[row + 1][col - 1] == '.':
            if self.is_red_move:
                if self.board[row][col] == 'R':
                    copy = tuple_to_list(self.board)
                    copy[row][col], copy[row + 1][col - 1] = '.', 'R'
                    return State(list_to_tuple(copy), not self.is_red_move)
            else:
                if self.board[row][col] == 'B':
                    copy = tuple_to_list(self.board)
                    copy[row][col], copy[row + 1][col - 1] = '.', 'B'
                    return State(list_to_tuple(copy), not self.is_red_move)
                if self.board[row][col] == 'b':
                    copy = tuple_to_list(self.board)
                    if row == 6:
                        copy[row][col], copy[row + 1][col - 1] = '.', 'B'
                    else:
                        copy[row][col], copy[row + 1][col - 1] = '.', 'b'
                    return State(list_to_tuple(copy), not self.is_red_move)
        return None

    def move_down_right_one(self, row, col):
        if row <= 6 and col <= 6 and self.board[row + 1][col + 1] == '.':
            if self.is_red_move:
                if self.board[row][col] == 'R':
                    copy = tuple_to_list(self.board)
                    copy[row][col], copy[row + 1][col + 1] = '.', 'R'
                    return State(list_to_tuple(copy), not self.is_red_move)
            else:
                if self.board[row][col] == 'B':
                    copy = tuple_to_list(self.board)
                    copy[row][col], copy[row + 1][col + 1] = '.', 'B'
                    return State(list_to_tuple(copy), not self.is_red_move)
                if self.board[row][col] == 'b':
                    copy = tuple_to_list(self.board)
                    if row == 6:
                        copy[row][col], copy[row + 1][col + 1] = '.', 'B'
                    else:
                        copy[row][col], copy[row + 1][col + 1] = '.', 'b'
                    return State(list_to_tuple(copy), not self.is_red_move)
        return None

    def move_up_left_one(self, row, col):
        if row >= 1 and col >= 1 and self.board[row - 1][col - 1] == '.':
            if not self.is_red_move:
                if self.board[row][col] == 'B':
                    copy = tuple_to_list(self.board)
                    copy[row][col], copy[row - 1][col - 1] = '.', 'B'
                    return State(list_to_tuple(copy), not self.is_red_move)
            else:
                if self.board[row][col] == 'R':
                    copy = tuple_to_list(self.board)
                    copy[row][col], copy[row - 1][col - 1] = '.', 'R'
                    return State(list_to_tuple(copy), not self.is_red_move)
                if self.board[row][col] == 'r':
                    copy = tuple_to_list(self.board)
                    if row == 1:
                        copy[row][col], copy[row - 1][col - 1] = '.', 'R'
                    else:
                        copy[row][col], copy[row - 1][col - 1] = '.', 'r'
                    return State(list_to_tuple(copy), not self.is_red_move)
        return None

    def move_up_right_one(self, row, col):
        if row >= 1 and col <= 6 and self.board[row - 1][col + 1] == '.':
            if not self.is_red_move:
                if self.board[row][col] == 'B':
                    copy = tuple_to_list(self.board)
                    copy[row][col], copy[row - 1][col + 1] = '.', 'B'
                    return State(list_to_tuple(copy), not self.is_red_move)
            else:
                if self.board[row][col] == 'R':
                    copy = tuple_to_list(self.board)
                    copy[row][col], copy[row - 1][col + 1] = '.', 'R'
                    return State(list_to_tuple(copy), not self.is_red_move)
                if self.board[row][col] == 'r':
                    copy = tuple_to_list(self.board)
                    if row == 1:
                        copy[row][col], copy[row - 1][col + 1] = '.', 'R'
                    else:
                        copy[row][col], copy[row - 1][col + 1] = '.', 'r'
                    return State(list_to_tuple(copy), not self.is_red_move)
        return None

    def move_down_left_two(self, row, col):
        if row <= 5 and col >= 2 and self.board[row + 2][col - 2] == '.':
            if self.is_red_move:
                if self.board[row][col] == 'R' and self.board[row + 1][col - 1] in 'bB':
                    copy = tuple_to_list(self.board)
                    copy[row][col], copy[row + 1][col - 1], copy[row + 2][col - 2] = '.', '.', 'R'
                    return State(list_to_tuple(copy), self.is_red_move)
            else:
                if self.board[row][col] == 'B' and self.board[row + 1][col - 1] in 'rR':
                    copy = tuple_to_list(self.board)
                    copy[row][col], copy[row + 1][col - 1], copy[row + 2][col - 2] = '.', '.', 'B'
                    return State(list_to_tuple(copy), self.is_red_move)
                if self.board[row][col] == 'b' and self.board[row + 1][col - 1] in 'rR':
                    copy = tuple_to_list(self.board)
                    if row == 5:
                        copy[row][col], copy[row + 1][col - 1], copy[row + 2][col - 2] = '.', '.', 'B'
                    else:
                        copy[row][col], copy[row + 1][col - 1], copy[row + 2][col - 2] = '.', '.', 'b'
                    return State(list_to_tuple(copy), self.is_red_move)
        return None

    def move_down_right_two(self, row, col):
        if row <= 5 and col <= 5 and self.board[row + 2][col + 2] == '.':
            if self.is_red_move:
                if self.board[row][col] == 'R' and self.board[row + 1][col + 1] in 'bB':
                    copy = tuple_to_list(self.board)
                    copy[row][col], copy[row + 1][col + 1], copy[row + 2][col + 2] = '.', '.', 'R'
                    return State(list_to_tuple(copy), self.is_red_move)
            else:
                if self.board[row][col] == 'B' and self.board[row + 1][col + 1] in 'rR':
                    copy = tuple_to_list(self.board)
                    copy[row][col], copy[row + 1][col + 1], copy[row + 2][col + 2] = '.', '.', 'B'
                    return State(list_to_tuple(copy), self.is_red_move)
                if self.board[row][col] == 'b' and self.board[row + 1][col + 1] in 'rR':
                    copy = tuple_to_list(self.board)
                    if row == 5:
                        copy[row][col], copy[row + 1][col + 1], copy[row + 2][col + 2] = '.', '.', 'B'
                    else:
                        copy[row][col], copy[row + 1][col + 1], copy[row + 2][col + 2] = '.', '.', 'b'
                    return State(list_to_tuple(copy), self.is_red_move)
        return None

    def move_up_right_two(self, row, col):
        if row >= 2 and col <= 5 and self.board[row - 2][col + 2] == '.':
            if not self.is_red_move:
                if self.board[row][col] == 'B' and self.board[row - 1][col + 1] in 'rR':
                    copy = tuple_to_list(self.board)
                    copy[row][col], copy[row - 1][col + 1], copy[row - 2][col + 2] = '.', '.', 'B'
                    return State(list_to_tuple(copy), self.is_red_move)
            else:
                if self.board[row][col] == 'R' and self.board[row - 1][col + 1] in 'bB':
                    copy = tuple_to_list(self.board)
                    copy[row][col], copy[row - 1][col + 1], copy[row - 2][col + 2] = '.', '.', 'R'
                    return State(list_to_tuple(copy), self.is_red_move)
                if self.board[row][col] == 'r' and self.board[row - 1][col + 1] in 'bB':
                    copy = tuple_to_list(self.board)
                    if row == 2:
                        copy[row][col], copy[row - 1][col + 1], copy[row - 2][col + 2] = '.', '.', 'R'
                    else:
                        copy[row][col], copy[row - 1][col + 1], copy[row - 2][col + 2] = '.', '.', 'r'
                    return State(list_to_tuple(copy), self.is_red_move)
        return None

    def move_up_left_two(self, row, col):
        if row >= 2 and col >= 2 and self.board[row - 2][col - 2] == '.':
            if not self.is_red_move:
                if self.board[row][col] == 'B' and self.board[row - 1][col - 1] in 'rR':
                    copy = tuple_to_list(self.board)
                    copy[row][col], copy[row - 1][col - 1], copy[row - 2][col - 2] = '.', '.', 'B'
                    return State(list_to_tuple(copy), self.is_red_move)
            else:
                if self.board[row][col] == 'R' and self.board[row - 1][col - 1] in 'bB':
                    copy = tuple_to_list(self.board)
                    copy[row][col], copy[row - 1][col - 1], copy[row - 2][col - 2] = '.', '.', 'R'
                    return State(list_to_tuple(copy), self.is_red_move)
                if self.board[row][col] == 'r' and self.board[row - 1][col - 1] in 'bB':
                    copy = tuple_to_list(self.board)
                    if row == 2:
                        copy[row][col], copy[row - 1][col - 1], copy[row - 2][col - 2] = '.', '.', 'R'
                    else:
                        copy[row][col], copy[row - 1][col - 1], copy[row - 2][col - 2] = '.', '.', 'r'
                    return State(list_to_tuple(copy), self.is_red_move)
        return None

    def can_capture(self):
        for i in range(8):
            for j in range(8):
                if (self.move_up_left_two(i, j) is not None) or (self.move_up_right_two(i, j) is not None) or (
                        self.move_down_left_two(i, j) is not None) or (self.move_down_right_two(i, j) is not None):
                    return True
        return False

    def capture_tracker(self, row, col, captured=False):
        states = []
        if not self.can_capture() and captured == True:
            states.append(self)
        state1 = self.move_up_left_two(row, col)
        state2 = self.move_up_right_two(row, col)
        state3 = self.move_down_left_two(row, col)
        state4 = self.move_down_right_two(row, col)
        if state1 is not None:
            states += state1.capture_tracker(row - 2, col - 2, True)
        if state2 is not None:
            states += state2.capture_tracker(row - 2, col + 2, True)
        if state3 is not None:
            states += state3.capture_tracker(row + 2, col - 2, True)
        if state4 is not None:
            states += state4.capture_tracker(row + 2, col + 2, True)
        new_states = []
        for i in states:
            new_states.append(State(i.board, not self.is_red_move))
        return new_states

    def normal_move_tracker(self, row, col):
        states = []
        state1 = self.move_up_left_one(row, col)
        state2 = self.move_up_right_one(row, col)
        state3 = self.move_down_left_one(row, col)
        state4 = self.move_down_right_one(row, col)
        potential = [state1, state2, state3, state4]
        for i in potential:
            if i is not None:
                states.append(i)
        return states

    def actions(self):
        capture_moves = []
        normal_moves = []

        for i in range(8):
            for j in range(8):
                normal_moves += self.normal_move_tracker(i, j)
                capture_moves += self.capture_tracker(i, j)
        if capture_moves:
            return capture_moves
        else:
            return normal_moves

    def heuristic(self, is_advanced=True):
        if is_advanced:
            heuristic = 0
            for i in range(8):
                for j in range(8):
                    piece = self.board[i][j]
                    if piece == 'r':
                        heuristic += 4 + (7 - i)
                    if piece == 'R':
                        heuristic += 12
                    if piece == 'b':
                        heuristic -= 4 + i
                    if piece == 'B':
                        heuristic -= 12
            return heuristic
        else:
            util = 0
            for i in self.board:
                for j in i:
                    if j == 'r':
                        util += 1
                    if j == 'R':
                        util += 2
                    if j == 'b':
                        util -= 1
                    if j == 'B':
                        util -= 2
            return util

    # def Minimax(self,depth):
    #     best_successor = None
    #     # global explored
    #     # explored.add((self.board, self.is_red_move))
    #     actions = self.actions()
    #     if self.is_red_move:
    #         value = -math.inf
    #     else:
    #         value = math.inf
    #     if depth == 6 and actions == []:
    #         return best_successor, value
    #     if depth == 6 and actions != []:
    #         return best_successor,self.heuristic(False)
    #     for next_pos in actions:
    #         # if (next_pos.board, next_pos.is_red_move) not in explored:
    #         if True:
    #             next_next_pos,next_val = next_pos.Minimax(depth + 1)
    #             if self.is_red_move:
    #                 if value < next_val:
    #                     value, best_successor = next_val, next_pos
    #             else:
    #                 if value > next_val:
    #                     value, best_successor = next_val, next_pos
    #     return best_successor,value

    def AlphaBeta(self, alpha=-math.inf, beta=math.inf, depth=0, limit=7,is_advanced=True,sort_heuristic = True):
        best_successor = None
        global explored
        if (self.board,self.is_red_move) in explored:
            if self.actions() !=[]:
                return None, self.heuristic(is_advanced)
            if self.is_red_move:
                return None,-math.inf
            else:
                return None,math.inf
        explored.add((self.board,self.is_red_move))
        if self.is_red_move:
            value = -math.inf
            actions = self.actions()
            if sort_heuristic:
                actions.sort(key=lambda x: x.heuristic())
                actions.reverse()
        else:
            value = math.inf
            actions = self.actions()
            if sort_heuristic:
                actions.sort(key=lambda x: x.heuristic())
        if depth == limit and actions == []:
            return best_successor, value
        if depth == limit and actions != []:
            return best_successor,self.heuristic(is_advanced)

        for next_pos in actions:
            next_next_pos,next_val = next_pos.AlphaBeta(alpha, beta, depth + 1, limit,is_advanced,sort_heuristic)
            if self.is_red_move:
                if value < next_val:
                    value, best_successor = next_val, next_pos
                if value >= beta:
                    return best_successor, value
                alpha = max(alpha, value)
            else:
                if value > next_val:
                    value, best_successor = next_val, next_pos
                if value <= alpha:
                    return best_successor, value
                beta = min(beta, value)
        return best_successor,value


def AlphaBetaRunner(input_file, output_file, limit,is_advanced,is_sorted):
    state = file_to_state(input_file)
    best_successor,best_value = state.AlphaBeta(-math.inf, math.inf,0,limit,is_advanced,is_sorted)
    # best_successor, best_value = state.Minimax(0)
    if best_successor is None:
        state_to_file(state, output_file)
    else:
        state_to_file(best_successor, output_file)

    return best_successor,best_value

# def MinimaxRunner(input_file, output_file):
#     state = file_to_state(input_file)
#     best_successor,best_value = state.Minimax(0)
#     state_to_file(best_successor, output_file)
#     return best_successor,best_value


def file_to_state(file):
    my_file = open(file, "r")
    lst = tuple(tuple(j for j in i) for i in my_file.read().split())
    return State(lst, True)


def state_to_file(state,output_file):
    with open(output_file, 'w') as f:
        for i in range(7):
            r = ''
            for j in state.board[i]:
                r += str(j)
            f.write(r + '\n')
        r=''
        for j in state.board[7]:
            r += str(j)
        f.write(r)


def list_to_tuple(lst: list):
    if type(lst) == str:
        return lst
    if type(lst) == list and all(type(j) == str for j in lst):
        return tuple(lst)
    else:
        return tuple(list_to_tuple(j) for j in lst)


def tuple_to_list(lst: tuple):
    if type(lst) == str:
        return lst
    if type(lst) == tuple and all(type(j) == str for j in lst):
        return list(lst)
    else:
        return list(tuple_to_list(j) for j in lst)


if __name__ == "__main__":
    AlphaBetaRunner('input2.txt','sol2.txt',7, True,True)
    # AlphaBetaRunner(sys.argv[1], sys.argv[2],7,True,True)
