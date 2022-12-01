import copy
import math
import sys


def file_to_state(file):
    my_file = open(file, "r")
    lst = my_file.read().split()
    actual_row_constraints = [int(i) for i in lst[0]]
    actual_column_constraints = [int(i) for i in lst[1]]
    given_ships = [int(i) for i in lst[2]]
    new_given_ships = []
    size = 1
    for i in given_ships:
        new_given_ships += [size] * i
        size += 1
    numships = len(new_given_ships)
    size = len(actual_row_constraints)
    length = {i: new_given_ships[i] for i in range(numships)}

    hint = []
    for _ in range(3, 3 + size):
        hint.append([i for i in lst[_]])
    final_hint = []
    for i in range(size):
        for j in range(size):
            clue = hint[i][j]
            if clue in 'SWLRTBM':
                final_hint.append((i, j, clue))
    assignment = {i: [None] for i in range(numships)}
    return actual_row_constraints, actual_column_constraints, length, size, final_hint, assignment, numships


# GLOBAL VARIABLE
actual_row_constraints = []
actual_column_constraints = []
length = {}  # maps each variable to its length
size = 0  # size of the board
CurDom = {}  # CurDom of each variable
Assignment = {}  # Assigned value of each variable.
Constraints = []
numships = 0


def getCurDom(length, size):
    global CurDom, Constraints, Assignment, Assigned, constraint_containing_V
    CurDom = {}
    for i in range(numships):
        if length[i] == 1:
            lst = set()
            for j in range(size):
                for k in range(size):
                    lst.add((j, k, 0))
            CurDom[i] = lst
        if length[i] == 2:
            lst = set()
            for j in range(size - 1):
                for k in range(size):
                    lst.add((j, k, 1))
            for j in range(size):
                for k in range(size - 1):
                    lst.add((j, k, 0))
            CurDom[i] = lst
        if length[i] == 3:
            lst = set()
            for j in range(size - 2):
                for k in range(size):
                    lst.add((j, k, 1))
            for j in range(size):
                for k in range(size - 2):
                    lst.add((j, k, 0))
            CurDom[i] = lst
        if length[i] == 4:
            lst = set()
            for j in range(size - 3):
                for k in range(size):
                    lst.add((j, k, 1))
            for j in range(size):
                for k in range(size - 3):
                    lst.add((j, k, 0))
            CurDom[i] = lst
    return CurDom


def get_row_constraints():
    global CurDom, Constraints, Assignment, Assigned, constraint_containing_V
    # 1.category,  3->(3+n-1): relevant variables. remaining:values

    return (0, tuple(i for i in range(numships)),)


def get_column_constraints():
    global CurDom, Constraints, Assignment, Assigned, constraint_containing_V
    return (1, tuple(i for i in range(numships)),)


def get_check_collisions():
    global CurDom, Constraints, Assignment, Assigned, constraint_containing_V
    lst = set()
    for i in range(numships):
        for j in range(i):
            lst.add((2, (i, j),))
    return lst


def get_hint_constraints():
    global CurDom, Constraints, Assignment, Assigned, constraint_containing_V
    return (3, tuple(i for i in range(numships)),)


def get_all_constraints():
    global CurDom, Constraints, Assignment, Assigned, constraint_containing_V
    return {get_row_constraints()}.union({get_column_constraints()}).union(get_check_collisions()).union(
        {get_hint_constraints()})


def check_row(row_constraint):
    global CurDom, Constraints, Assignment, Assigned, constraint_containing_V
    # 2
    # 2
    # 1
    # 4
    # 5
    global length, size, numships
    n1 = [0] * size
    if all(Assigned[i] for i in Assigned):
        for i in range(numships):
            variable = Assignment[i]
            if variable[2] == 1:
                for j in range(variable[0], variable[0] + length[i]):
                    n1[j] += 1
            if variable[2] == 0:
                n1[variable[0]] += length[i]
        return all(n1[i] == actual_row_constraints[i] for i in range(size))
    else:
        for i in range(numships):
            if Assigned[i]:
                variable = Assignment[i]
                if variable[2] == 1:
                    for j in range(variable[0], variable[0] + length[i]):
                        n1[j] += 1
                if variable[2] == 0:
                    n1[variable[0]] += length[i]
        return all(n1[i] <= actual_row_constraints[i] for i in range(size))


def check_column(col_constraint):
    global CurDom, Constraints, Assignment, Assigned, constraint_containing_V
    # 2 2 1 4 5
    global length, size
    n = [0] * size
    if all(Assigned[i] for i in Assigned):
        for i in range(numships):
            variable = Assignment[i]
            if variable[2] == 0:
                for j in range(variable[1], variable[1] + length[i]):
                    n[j] += 1
            if variable[2] == 1:
                n[variable[1]] += length[i]
        return all(n[i] == actual_column_constraints[i] for i in range(size))
    else:
        for i in range(numships):
            if Assigned[i]:
                variable = Assignment[i]
                if variable[2] == 0:
                    for j in range(variable[1], variable[1] + length[i]):
                        n[j] += 1
                if variable[2] == 1:
                    n[variable[1]] += length[i]
        return all(n[i] <= actual_column_constraints[i] for i in range(size))


def get_collision_box(variable, i):
    global CurDom, Constraints, Assignment, Assigned, constraint_containing_V
    global length, size
    l = length[i]
    if variable[2] == 1:
        # upper left, lower right
        return (variable[0] - 1, variable[1] - 1), (variable[0] + length[i], variable[1] + 1)
    if variable[2] == 0:
        # upper left, upper right, lower left, lower right
        return (variable[0] - 1, variable[1] - 1), (variable[0] + 1, variable[1] + length[i])


def get_normal_collision_box(variable, i):
    global CurDom, Constraints, Assignment, Assigned, constraint_containing_V
    global length, size
    l = length[i]
    if variable[2] == 1:
        # upper left, lower right
        return (variable[0], variable[1]), (variable[0] + length[i] - 1, variable[1])
    if variable[2] == 0:
        # upper left, upper right, lower left, lower right
        return (variable[0], variable[1]), (variable[0], variable[1] + length[i] - 1)


def check_collision(collision_constraint):
    global CurDom, Constraints, Assignment, Assigned, constraint_containing_V
    x, y = Assignment[collision_constraint[1][0]], Assignment[collision_constraint[1][1]]
    x_upperleft, x_lowerright = get_collision_box(x, collision_constraint[1][0])
    y_upperleft, y_lowerright = get_normal_collision_box(y, collision_constraint[1][1])
    if (x_upperleft[0] <= y_upperleft[0] <= x_lowerright[0] and x_upperleft[1] <= y_upperleft[1] <= x_lowerright[
        1]) or (
            x_upperleft[0] <= y_upperleft[0] <= x_lowerright[0] and x_upperleft[1] <= y_lowerright[1] <= x_lowerright[
        1]) or (
            x_upperleft[0] <= y_lowerright[0] <= x_lowerright[0] and x_upperleft[1] <= y_lowerright[1] <= x_lowerright[
        1]) or (
            x_upperleft[0] <= y_lowerright[0] <= x_lowerright[0] and x_upperleft[1] <= y_upperleft[1] <= x_lowerright[
        1]):
        return False
    return True


def check_hint(hint_constraint):
    global CurDom, Constraints, Assignment, Assigned, constraint_containing_V
    global final_hint
    if all(Assigned[i] == True for i in Assigned):
        for h in final_hint:
            if h[2] == 'W':
                for i in range(numships):
                    if Assignment[i][2] == 1:
                        if Assignment[i][1] == h[1] and Assignment[i][0] <= h[0] <= Assignment[i][0] + length[i] - 1:
                            return False
                    if Assignment[i][2] == 0:
                        if Assignment[i][0] == h[0] and Assignment[i][1] <= h[1] <= Assignment[i][1] + length[i] - 1:
                            return False
            if h[2] == 'S':
                if not any(Assignment[i][0] == h[0] and Assignment[i][1] == h[1] and length[i] == 1 for i in
                           range(numships)):
                    return False
            if h[2] == 'L':
                if not any(Assignment[i][0] == h[0] and Assignment[i][1] == h[1] and length[i] >= 2 and Assignment[i][
                    2] == 0 for i in range(numships)):
                    return False
            if h[2] == 'R':
                if not any(Assignment[i][0] == h[0] and Assignment[i][1] + length[i] - 1 == h[1] and length[i] >= 2 and
                           Assignment[i][2] == 0 for i in range(numships)):
                    return False
            if h[2] == 'T':
                if not any(Assignment[i][0] == h[0] and Assignment[i][1] == h[1] and length[i] >= 2 and Assignment[i][
                    2] == 1 for i in range(numships)):
                    return False
            if h[2] == 'B':
                if not any(Assignment[i][0] + length[i] - 1 == h[0] and Assignment[i][1] == h[1] and length[i] >= 2 and
                           Assignment[i][2] == 1 for i in range(numships)):
                    return False
            if h[2] == 'M':
                if not any((length[i] >= 3 and (
                        (Assignment[i][0] == h[0] and Assignment[i][1] + 1 == h[1] and Assignment[i][2] == 0) or (
                        Assignment[i][1] == h[1] and Assignment[i][0] + 1 == h[0] and Assignment[i][2] == 1))) or (
                                   length[i] == 4 and ((Assignment[i][0] == h[0] and Assignment[i][1] + 2 == h[1] and
                                                        Assignment[i][2] == 0) or (
                                                               Assignment[i][1] == h[1] and Assignment[i][0] + 2 == h[
                                                           0] and Assignment[i][2] == 1))) for i in range(numships)):
                    return False
    else:
        for h in final_hint:
            if h[2] == 'W':
                # ONLY ASSIGNED
                for i in range(numships):
                    if Assigned[i]:
                        if Assignment[i][2] == 1:
                            if Assignment[i][1] == h[1] and Assignment[i][0] <= h[0] <= Assignment[i][0] + length[
                                i] - 1:
                                return False
                        if Assignment[i][2] == 0:
                            if Assignment[i][0] == h[0] and Assignment[i][1] <= h[1] <= Assignment[i][1] + length[
                                i] - 1:
                                return False
            if h[2] == 'S':
                for i in range(numships):
                    if Assigned[i] and not (
                            length[i] == 1 and Assignment[i][0] == h[0] and Assignment[i][1] == h[1]) and ((Assignment[
                                                                                                                i][
                                                                                                                0] - 1 <=
                                                                                                            h[0] <=
                                                                                                            Assignment[
                                                                                                                i][
                                                                                                                0] + 1 and
                                                                                                            Assignment[
                                                                                                                i][
                                                                                                                1] - 1 <=
                                                                                                            h[1] <=
                                                                                                            Assignment[
                                                                                                                i][
                                                                                                                1] + 1) or (
                                                                                                                   Assignment[
                                                                                                                       i][
                                                                                                                       1] - 1 <=
                                                                                                                   h[
                                                                                                                       1] <=
                                                                                                                   Assignment[
                                                                                                                       i][
                                                                                                                       1] + 1 and
                                                                                                                   Assignment[
                                                                                                                       i][
                                                                                                                       0] <=
                                                                                                                   h[
                                                                                                                       0] <=
                                                                                                                   Assignment[
                                                                                                                       i][
                                                                                                                       0] +
                                                                                                                   length[
                                                                                                                       i] and
                                                                                                                   length[
                                                                                                                       i] >= 2 and
                                                                                                                   Assignment[
                                                                                                                       i][
                                                                                                                       2] == 1) or (
                                                                                                                   Assignment[
                                                                                                                       i][
                                                                                                                       0] - 1 <=
                                                                                                                   h[
                                                                                                                       0] <=
                                                                                                                   Assignment[
                                                                                                                       i][
                                                                                                                       0] + 1 and
                                                                                                                   Assignment[
                                                                                                                       i][
                                                                                                                       1] <=
                                                                                                                   h[
                                                                                                                       1] <=
                                                                                                                   Assignment[
                                                                                                                       i][
                                                                                                                       1] +
                                                                                                                   length[
                                                                                                                       i] and
                                                                                                                   length[
                                                                                                                       i] >= 2 and
                                                                                                                   Assignment[
                                                                                                                       i][
                                                                                                                       2] == 0)):
                        return False

            if h[2] == 'L':
                for i in range(numships):
                    if Assigned[i] and not (
                            length[i] >= 2 and Assignment[i][0] == h[0] and Assignment[i][1] == h[1] and Assignment[i][
                        2] == 0) and (
                            (h[0] - 1 <= Assignment[i][0] <= h[0] + 1 and h[1] - 1 <= Assignment[i][1] <= h[1] + 2) or (
                            h[1] - 1 <= Assignment[i][1] <= h[1] + 1 and h[0] - length[i] <= Assignment[i][0] <= h[
                        0] and Assignment[i][2] == 1) or (
                                    h[0] - 1 <= Assignment[i][0] <= h[0] + 1 and h[1] - length[i] <= Assignment[i][1] <=
                                    h[1] and Assignment[i][2] == 0)):
                        return False
            if h[2] == 'R':
                for i in range(numships):
                    if Assigned[i]:
                        if not (length[i] >= 2 and Assignment[i][0] == h[0] and Assignment[i][2] == 0 and Assignment[i][
                            1] + length[i] - 1 == h[1]):
                            if (h[0] - 1 <= Assignment[i][0] <= h[0] + 1 and h[1] - length[i] - 1 <= Assignment[i][1] <=
                                h[1] + 1 and Assignment[i][2] == 0) or (
                                    h[1] - 2 <= Assignment[i][1] <= h[1] + 1 and h[0] - length[i] <= Assignment[i][0] <=
                                    h[0] + 1 and Assignment[i][2] == 1):
                                return False
            if h[2] == 'T':
                for i in range(numships):
                    if Assigned[i] and not (
                            length[i] >= 2 and Assignment[i][0] == h[0] and Assignment[i][1] == h[1] and Assignment[i][
                        2] == 1) and (
                            (h[0] - 1 <= Assignment[i][0] <= h[0] + 2 and h[1] - 1 <= Assignment[i][1] <= h[1] + 1) or (
                            h[1] - 1 <= Assignment[i][1] <= h[1] + 1 and h[0] - length[i] <= Assignment[i][0] <= h[
                        0] and Assignment[i][2] == 1) or (
                                    h[0] - 1 <= Assignment[i][0] <= h[0] + 2 and h[1] - length[i] <= Assignment[i][1] <=
                                    h[1] and Assignment[i][2] == 0)):
                        return False
            if h[2] == 'B':
                for i in range(numships):
                    if Assigned[i]:
                        if not (length[i] >= 2 and Assignment[i][1] == h[1] and Assignment[i][2] == 1 and Assignment[i][
                            0] + length[i] - 1 == h[0]):
                            if (h[1] - 1 <= Assignment[i][1] < h[1] + 1 and h[0] - length[i] - 1 <= Assignment[i][0] <=
                                h[0] + 1 and Assignment[i][2] == 1) or (
                                    h[0] - 2 <= Assignment[i][0] <= h[0] + 1 and h[1] - length[i] <= Assignment[i][1] <=
                                    h[1] and Assignment[i][2] == 0):
                                return False
            if h[2] == 'M':
                for i in range(numships):
                    if Assigned[i]:
                        if not ((length[i] >= 3 and ((Assignment[i][0] == h[0] - 1 and Assignment[i][1] == h[1] and
                                                      Assignment[i][2] == 1) or (
                                                             Assignment[i][1] == h[1] - 1 and Assignment[i][0] == h[
                                                         0] and Assignment[i][2] == 0))) or (length[i] == 4 and ((
                                                                                                                         Assignment[
                                                                                                                             i][
                                                                                                                             0] ==
                                                                                                                         h[
                                                                                                                             0] - 2 and
                                                                                                                         Assignment[
                                                                                                                             i][
                                                                                                                             1] ==
                                                                                                                         h[
                                                                                                                             1] and
                                                                                                                         Assignment[
                                                                                                                             i][
                                                                                                                             2] == 1) or (
                                                                                                                         Assignment[
                                                                                                                             i][
                                                                                                                             1] ==
                                                                                                                         h[
                                                                                                                             1] - 2 and
                                                                                                                         Assignment[
                                                                                                                             i][
                                                                                                                             0] ==
                                                                                                                         h[
                                                                                                                             0] and
                                                                                                                         Assignment[
                                                                                                                             i][
                                                                                                                            2] == 0)))):
                            if ((Assignment[i][2] == 1 and h[1] - 1 <= Assignment[i][1] <= h[1] + 1 and h[0] - length[
                                i] <= Assignment[i][0] <= h[0] + 1) or (
                                    Assignment[i][2] == 0 and h[0] - 1 <= Assignment[i][0] <= h[0] + 1 and h[1] -
                                    length[i] <= Assignment[i][1] <= h[1] + 1)):
                                return False
    return True


def check_constraint(constraint):
    global CurDom, Constraints, Assignment, Assigned, constraint_containing_V
    if constraint[0] == 0:
        return check_row(constraint)
    if constraint[0] == 1:
        return check_column(constraint)
    if constraint[0] == 2:
        return check_collision(constraint)
    if constraint[0] == 3:
        return check_hint(constraint)


def find_constraint_containing_V():
    global CurDom, Constraints, Assignment, Assigned, constraint_containing_V
    constraint_containing_V = {}
    for v in range(numships):
        lst = set()
        for i in Constraints:
            if v in i[1]:
                lst.add(i)
        constraint_containing_V[v] = lst
    return constraint_containing_V


# def find_constraint_missing_one(variable):
#     global CurDom,Constraints,Assignment,Assigned,constraint_containing_V
#     lst = []
#     for i in constraint_containing_V[variable]:
#
#         if i[0] in {0,1,3} and variable<=numships-2:
#             lst.append([i,variable+1])
#         else:
#             for j in i[1]:
#                 if not Assigned[j] and j!=variable:
#                     lst.append([i,j])
#                     break
#     return lst


def find_constraint_missing_one(variable, level):
    global CurDom, Constraints, Assignment, Assigned, constraint_containing_V
    lst = []
    for i in constraint_containing_V[variable]:
        if i[0] in {0, 1, 3} and level <= numships - 2:
            for j in Assigned:
                if Assigned[j] == False:
                    lst.append([i, j])
        else:
            if Assigned[i[1][0]] and not Assigned[i[1][1]]:
                lst.append([i, i[1][1]])
            if Assigned[i[1][1]] and not Assigned[i[1][0]]:
                lst.append([i, i[1][0]])
    return lst


def find_filled_constraint(variable):
    global CurDom, Constraints, Assignment, Assigned, constraint_containing_V
    lst = []

    for i in constraint_containing_V[variable]:
        if i[0] in {0, 1}:
            lst.append(i)
        elif i[0] == 3 and all(Assigned[k] for k in Assigned):
            lst.append(i)
        else:
            if variable in i[1] and all(Assigned[j] for j in i[1]):
                lst.append(i)
    return lst


def MRV():
    min = math.inf
    min_index = 0
    for i in range(numships):
        if not Assigned[i] and len(CurDom[i]) < min:
            min = len(CurDom[i])
            min_index = i
    return min_index


def FCCheck(C, X):
    global CurDom, Constraints, Assignment, Assigned, constraint_containing_V
    to_be_removed = []

    for d in CurDom[X]:
        Assigned[X] = True
        Assignment[X] = d
        if not check_constraint(C):
            to_be_removed.append(d)
        Assigned[X] = False

    for i in to_be_removed:
        CurDom[X].remove(i)
    if CurDom[X] == set():
        return True  # DWO
    else:
        return False


def FC(level):
    global CurDom, Constraints, Assignment, Assigned, constraint_containing_V
    if level == numships:
        return True
    Assigned[level] = True
    DomOfLevel = copy.deepcopy(CurDom)
    for k in DomOfLevel[level]:
        original = copy.deepcopy(CurDom)
        Assignment[level] = k
        DWOoccured = False
        for constraint_tuple in find_constraint_missing_one(level, level):
            if (FCCheck(constraint_tuple[0], constraint_tuple[1])):
                DWOoccured = True
                break
        if not DWOoccured:
            if FC(level + 1):
                return True
        CurDom = original
    Assigned[level] = False
    return False


def FC_MRV(level):
    global CurDom, Constraints, Assignment, Assigned, constraint_containing_V
    if level == numships:
        return True
    i = MRV()
    Assigned[i] = True
    DomOfLevel = copy.deepcopy(CurDom)
    for k in DomOfLevel[i]:
        original = copy.deepcopy(CurDom)
        Assignment[i] = k
        DWOoccured = False
        for constraint_tuple in find_constraint_missing_one(i, level):
            if (FCCheck(constraint_tuple[0], constraint_tuple[1])):
                DWOoccured = True
                break
        if not DWOoccured:
            if FC_MRV(level + 1):
                return True
        CurDom = original
    Assigned[i] = False
    return False


def BT(level):
    if level == numships:
        return True

    Assigned[level] = True
    for d in CurDom[level]:
        Assignment[level] = d
        ConstraintsOK = True
        for i in find_filled_constraint(level):
            if not check_constraint(i):
                ConstraintsOK = False

                break

        if ConstraintsOK:
            if BT(level + 1):
                return True
    Assigned[level] = False
    return False


def ships_to_board():
    global CurDom, Constraints, Assignment, Assigned, constraint_containing_V
    grid = []
    for i in range(numships):
        temp = []
        for j in range(numships):
            temp.append('W')
        grid.append(temp)
    for i in range(numships):
        # Vertical
        if Assignment[i][2] == 1:
            if length[i] == 1:
                grid[Assignment[i][0]][Assignment[i][1]] = 'S'
            if length[i] == 2:
                grid[Assignment[i][0]][Assignment[i][1]] = 'T'
                grid[Assignment[i][0] + 1][Assignment[i][1]] = 'B'
            if length[i] == 3:
                grid[Assignment[i][0]][Assignment[i][1]] = 'T'
                grid[Assignment[i][0] + 1][Assignment[i][1]] = 'M'
                grid[Assignment[i][0] + 2][Assignment[i][1]] = 'B'
            if length[i] == 4:
                grid[Assignment[i][0]][Assignment[i][1]] = 'T'
                grid[Assignment[i][0] + 1][Assignment[i][1]] = 'M'
                grid[Assignment[i][0] + 2][Assignment[i][1]] = 'M'
                grid[Assignment[i][0] + 3][Assignment[i][1]] = 'B'
        # Horizontal
        if Assignment[i][2] == 0:
            if length[i] == 1:
                grid[Assignment[i][0]][Assignment[i][1]] = 'S'
            if length[i] == 2:
                grid[Assignment[i][0]][Assignment[i][1]] = 'L'
                grid[Assignment[i][0]][Assignment[i][1] + 1] = 'R'
            if length[i] == 3:
                grid[Assignment[i][0]][Assignment[i][1]] = 'L'
                grid[Assignment[i][0]][Assignment[i][1] + 1] = 'M'
                grid[Assignment[i][0]][Assignment[i][1] + 2] = 'R'
            if length[i] == 4:
                grid[Assignment[i][0]][Assignment[i][1]] = 'L'
                grid[Assignment[i][0]][Assignment[i][1] + 1] = 'M'
                grid[Assignment[i][0]][Assignment[i][1] + 2] = 'M'
                grid[Assignment[i][0]][Assignment[i][1] + 3] = 'R'
    return grid


def state_to_file(output_file):
    global CurDom, Constraints, Assignment, Assigned, constraint_containing_V
    with open(output_file, 'w') as f:
        for i in range(size - 1):
            r = ''
            for j in grid[i]:
                r += str(j)
            f.write(r + '\n')
        r = ''
        for j in grid[size - 1]:
            r += str(j)
        f.write(r)


if __name__ == '__main__':
    actual_row_constraints, actual_column_constraints, length, size, final_hint, assignment, numships = file_to_state(
        sys.argv[1])
    CurDom = getCurDom(length, size)
    Constraints = get_all_constraints()
    row_constraints = get_row_constraints()
    column_constraints = get_column_constraints()
    Assigned = {i: False for i in range(numships)}
    Assignment = {}
    constraint_containing_V = find_constraint_containing_V()
    FC_MRV(0)
    grid = ships_to_board()
    state_to_file(sys.argv[2])
