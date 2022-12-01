import heapq
import sys

def get_block_pos(self, k):
    pos = []
    for i in range(5):
        for j in range(4):
            if self[i][j] == k:
                pos.append((i, j))
    return pos


def get_manhattan_heuristic(self):
    upper_left_row, upper_left_col = get_block_pos(self, 1)[0]
    return abs(upper_left_row - 3) + abs(upper_left_col - 1)


def get_advanced_heuristic(self):
    upper_left_row, upper_left_col = get_block_pos(self, 1)[0]
    if get_manhattan_heuristic(self) == 0:
        return 0
    elif (upper_left_row <= 2 and self[upper_left_row + 2][upper_left_col] == self[upper_left_row + 2][
        upper_left_col + 1] == 0) or \
            (upper_left_col == 0 and self[upper_left_row][upper_left_col + 2] == self[upper_left_row + 1][
                upper_left_col + 2] == 0) or \
            (upper_left_col == 2 and self[upper_left_row][upper_left_col - 1] == self[upper_left_row + 1][
                upper_left_col - 1] == 0):
        return get_manhattan_heuristic(self)
    return get_manhattan_heuristic(self) + 1


def successor(self):
    states = []
    for i in range(1, 8):
        if i == 1:
            row, col = get_block_pos(self, 1)[0]
            # move left
            # 0 1 1    1 1 0
            # 0 1 1 -> 1 1 0
            if col >= 1 and self[row][col - 1] == self[row + 1][col - 1] == 0:
                board1 = tuple_to_list(self)
                board1[row][col - 1], board1[row + 1][col - 1], board1[row][col + 1], \
                board1[row + 1][col + 1] = 1, 1, 0, 0
                states.append(list_to_tuple(board1))
            # move left
            # 1 1 0    0 1 1
            # 1 1 0 -> 0 1 1
            if col <= 1 and self[row][col + 2] == self[row + 1][col + 2] == 0:
                board1 = tuple_to_list(self)
                board1[row][col + 2], board1[row + 1][col + 2], board1[row][col], board1[row + 1][
                    col] = 1, 1, 0, 0
                states.append(list_to_tuple(board1))
            # move up
            # 0 0 0    1 1 0
            # 1 1 0 -> 1 1 0
            # 1 1 0    0 0 0
            if row >= 1 and self[row - 1][col] == self[row - 1][col + 1] == 0:
                board1 = tuple_to_list(self)
                board1[row - 1][col], board1[row - 1][col + 1], board1[row + 1][col], board1[row + 1][
                    col + 1] = 1, 1, 0, 0
                states.append(list_to_tuple(board1))
            # move down
            # 1 1 0    0 0 0
            # 1 1 0 -> 1 1 0
            # 0 0 0    1 1 0
            if row <= 2 and self[row + 2][col] == self[row + 2][col + 1] == 0:
                board1 = tuple_to_list(self)
                board1[row + 2][col], board1[row + 2][col + 1], board1[row][col], board1[row][
                    col + 1] = 1, 1, 0, 0
                states.append(list_to_tuple(board1))
        if 2 <= i <= 6:
            row1, col1 = get_block_pos(self, i)[0]
            row2, col2 = get_block_pos(self, i)[1]
            # 0 2 2 -> 2 2 0
            # move left
            if col1 >= 1 and col2 == col1 + 1 and self[row1][col1 - 1] == 0:
                board1 = tuple_to_list(self)
                board1[row1][col1 - 1], board1[row1][col2] = board1[row1][col2], board1[row1][col1 - 1]
                states.append(list_to_tuple(board1))
            # 0 2
            # 0 2
            # move left
            if col1 >= 1 and row2 == row1 + 1 and self[row1][col1 - 1] == self[row2][col1 - 1] == 0:
                board1 = tuple_to_list(self)
                board1[row1][col1], board1[row1][col1 - 1] = board1[row1][col1 - 1], board1[row1][col1]
                board1[row2][col1], board1[row2][col1 - 1] = board1[row2][col1 - 1], board1[row2][col1]
                states.append(list_to_tuple(board1))

            # 2 2 0
            # move right
            if col2 <= 2 and col2 == col1 + 1 and self[row1][col2 + 1] == 0:
                board1 = tuple_to_list(self)
                board1[row1][col1], board1[row1][col2 + 1] = board1[row1][col2 + 1], board1[row1][col1]
                states.append(list_to_tuple(board1))

            # x x 2 0
            # x x 2 0
            if col2 <= 2 and row2 == row1 + 1 and self[row1][col2 + 1] == self[row2][col2 + 1] == 0:
                board1 = tuple_to_list(self)
                board1[row1][col1], board1[row1][col1 + 1] = board1[row1][col1 + 1], board1[row1][col1]
                board1[row2][col1], board1[row2][col1 + 1] = board1[row2][col1 + 1], board1[row2][col1]
                states.append(list_to_tuple(board1))

            # move up
            # 0
            # 2
            # 2
            if row1 >= 1 and row2 == row1 + 1 and self[row1 - 1][col1] == 0:
                board1 = tuple_to_list(self)
                board1[row2][col1], board1[row1 - 1][col1] = board1[row1 - 1][col1], board1[row2][col1]
                states.append(list_to_tuple(board1))

            # 0 0
            # 2 2
            if row1 >= 1 and col2 == col1 + 1 and self[row1 - 1][col1] == self[row2 - 1][col2] == 0:
                board1 = tuple_to_list(self)
                board1[row1][col1], board1[row1 - 1][col1] = board1[row1 - 1][col1], board1[row1][col1]
                board1[row2][col2], board1[row2 - 1][col2] = board1[row2 - 1][col2], board1[row2][col2]
                states.append(list_to_tuple(board1))

            # move down
            # 2
            # 2
            # 0
            if row2 <= 3 and row2 == row1 + 1 and self[row2 + 1][col1] == 0:
                board1 = tuple_to_list(self)
                board1[row1][col1], board1[row2 + 1][col1] = board1[row2 + 1][col1], board1[row1][col1]
                states.append(list_to_tuple(board1))

            # 2 2
            # 0 0
            if row2 <= 3 and col2 == col1 + 1 and self[row1 + 1][col1] == self[row2 + 1][col2] == 0:
                board1 = tuple_to_list(self)
                board1[row1][col1], board1[row1 + 1][col1] = board1[row1 + 1][col1], board1[row1][col1]
                board1[row2][col2], board1[row2 + 1][col2] = board1[row2 + 1][col2], board1[row2][col2]
                states.append(list_to_tuple(board1))
        if i == 7:
            for j in get_block_pos(self, 7):
                row, col = j[0], j[1]
                # move left
                if col >= 1 and self[row][col - 1] == 0:
                    board1 = tuple_to_list(self)
                    board1[row][col], board1[row][col - 1] = board1[row][col - 1], board1[row][col]
                    states.append(list_to_tuple(board1))
                # move right
                if col <= 2 and self[row][col + 1] == 0:
                    board1 = tuple_to_list(self)
                    board1[row][col], board1[row][col + 1] = board1[row][col + 1], board1[row][col]
                    states.append(list_to_tuple(board1))

                # up
                if row >= 1 and self[row - 1][col] == 0:
                    board1 = tuple_to_list(self)
                    board1[row - 1][col], board1[row][col] = board1[row][col], board1[row - 1][col]
                    states.append(list_to_tuple(board1))

                # down
                if row <= 3 and self[row + 1][col] == 0:
                    board1 = tuple_to_list(self)
                    board1[row + 1][col], board1[row][col] = board1[row][col], board1[row + 1][col]
                    states.append(list_to_tuple(board1))
    return states


def list_to_tuple(lst: list):
    if type(lst) == int:
        return lst
    if type(lst) == list and all(type(j) == int for j in lst):
        return tuple(lst)
    else:
        return tuple(list_to_tuple(j) for j in lst)


def tuple_to_list(lst: tuple):
    if type(lst) == int:
        return lst
    if type(lst) == tuple and all(type(j) == int for j in lst):
        return list(lst)
    else:
        return list(tuple_to_list(j) for j in lst)


def file_to_state(file):
    my_file = open(file, "r")
    lst = tuple(tuple(int(j) for j in list(i)) for i in my_file.read().split())
    return lst


def dfs(initial, filename):
    frontier = [initial]
    parents = {}
    explored = set()
    while len(frontier) > 0:
        curr = frontier.pop()
        explored.add(curr)
        if is_goal(curr):
            solution = backtrack(parents, curr)
            length = str(len(solution) - 1)
            with open(filename, 'w') as f:
                f.write('Cost of the solution: ' + length + '\n')
                for i in solution:
                    b = state_transfer(i)
                    for j in b:
                        r = ''
                        for k in j:
                            r += str(k)
                        f.write(r + '\n')
                    f.write('\n')
            return
        else:
            for new_state in successor(curr):
                if new_state not in explored:
                    parents[new_state] = curr
                    frontier.append(new_state)


def A_manhattan(initial, filename):
    frontier = []
    heapq.heappush(frontier, (get_manhattan_heuristic(initial), initial))
    # step = 0
    steps = {initial: 0}
    parents = {}
    while len(frontier) > 0:
        curr = heapq.heappop(frontier)
        if is_goal(curr[1]):
            solution = backtrack(parents, curr[1])
            with open(filename, 'w') as f:
                f.write('Cost of the solution: ' + str(steps[curr[1]]) + '\n')
                for i in solution:
                    b = state_transfer(i)
                    for j in b:
                        r = ''
                        for k in j:
                            r += str(k)
                        f.write(r + '\n')
                    f.write('\n')
            return
        else:
            for new_state in successor(curr[1]):
                if new_state not in steps or steps[curr[1]] + 1 < steps[new_state]:
                    parents[new_state] = curr[1]
                    steps[new_state] = steps[curr[1]] + 1
                    heapq.heappush(frontier, (steps[curr[1]] + 1 + get_manhattan_heuristic(new_state), new_state))


def A_advanced(initial, filename):
    frontier = []
    heapq.heappush(frontier, (get_advanced_heuristic(initial), initial))
    # step = 0
    steps = {initial: 0}
    parents = {}
    while len(frontier) > 0:
        curr = heapq.heappop(frontier)
        if is_goal(curr[1]):
            solution = backtrack(parents, curr[1])
            with open(filename, 'w') as f:
                f.write('Cost of the solution: ' + str(steps[curr[1]]) + '\n')
                for i in solution:
                    b = state_transfer(i)
                    for j in b:
                        r = ''
                        for k in j:
                            r += str(k)
                        f.write(r + '\n')
                    f.write('\n')
            return
        else:
            for new_state in successor(curr[1]):
                if new_state not in steps or steps[curr[1]] + 1 < steps[new_state]:
                    parents[new_state] = curr[1]
                    steps[new_state] = steps[curr[1]] + 1
                    heapq.heappush(frontier, (steps[curr[1]] + 1 + get_advanced_heuristic(new_state), new_state))


def state_transfer(state):
    # after transfer, state only has 0,1,2,3,4.
    new_state = [[-1, -1, -1, -1], [-1, -1, -1, -1], [-1, -1, -1, -1], [-1, -1, -1, -1], [-1, -1, -1, -1]]
    for i in range(5):
        for j in range(4):
            if state[i][j] == 0:
                new_state[i][j] = 0
            if state[i][j] == 1:
                new_state[i][j] = 1
            if state[i][j] == 7:
                new_state[i][j] = 4
            if 2 <= state[i][j] <= 6 and i <= 3 and state[i][j] == state[i + 1][j]:
                new_state[i][j] = 3
                new_state[i + 1][j] = 3
            if 2 <= state[i][j] <= 6 and j <= 2 and state[i][j] == state[i][j + 1]:
                new_state[i][j] = 2
                new_state[i][j + 1] = 2
    return tuple(tuple(k) for k in new_state)


# def manhattan(initial, filename):
#     frontier = []
#     heapq.heappush(frontier, (get_manhattan_heuristic(initial), [initial]))
#     while len(frontier) < 20:
#         curr = heapq.heappop(frontier)
#         print(curr, len(curr[1]))
#         if is_goal(curr[1][len(curr[1])-1]):
#             with open(filename, 'w') as f:
#                 f.write('Cost of the solution: ' + str(len(curr[1])-1) + '\n')
#                 for i in curr[1]:
#                     b = i
#                     for j in b:
#                         r = ''
#                         for k in j:
#                             r += str(k)
#                         f.write(r + '\n')
#                     f.write('\n')
#             return
#         else:
#             for new_state in successor(curr[1][len(curr[1])-1]):
#                 new_cost = curr[0]-get_manhattan_heuristic(curr[1][len(curr[1])-1])+1+get_manhattan_heuristic(new_state)
#                 new_path = curr[1] + [new_state]
#                 heapq.heappush(frontier, (new_cost, new_path))
#     print(frontier)


def backtrack(parents, last):
    curr = last
    result = [last]
    while curr in parents:
        curr = parents[curr]
        result.append(curr)
    return result[::-1]


def is_goal(self):
    return get_manhattan_heuristic(self) == 0


if __name__ == "__main__":
    # state1 = ((2, 1, 1, 3), (2, 1, 1, 3), (7, 4, 0, 7), (7, 4, 0, 7), (5, 5, 6, 6))
    # state2 = ((5, 5, 6, 6), (0, 3, 3, 4), (2, 1, 1, 4), (2, 1, 1, 0), (7, 7, 7, 7))
    # state3 = ((2, 2, 7, 7), (4, 4, 3, 3), (6, 1, 1, 5), (6, 1, 1, 5), (0, 7, 7, 0))
    # dfs(state3, 'dfs1.txt')
    # A_advanced(state2, 'advanced.txt')
    state = file_to_state(sys.argv[1])
    dfs(state, sys.argv[2])
    A_advanced(state,sys.argv[3])
