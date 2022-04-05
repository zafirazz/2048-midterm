import random
import visual as v

def creating_game(n):
    matrix = []
    for i in range(n):
        matrix.append([0] * n)
    matrix = another_round(matrix)
    return matrix

def another_round(matrix):
    r = random.randint(0, len(matrix) - 1)
    c = random.randint(0, len(matrix) - 1)
    while matrix[r][c] != 0:
        r = random.randint(0, len(matrix) - 1)
        c = random.randint(0, len(matrix) - 1)
    matrix[r][c] = 2
    return matrix

def curr_state(matrix):
    for i in range(len(matrix)):
        for j in range(len(matrix)):
            if matrix[i][j] == 2048:
                return 'WON!'
    for i in range(len(matrix)):
        for j in range(len(matrix)):
            if matrix[i][j] == 0:
                return 'KEEP GOING'
    for i in range(len(matrix) - 1):
        for j in range(len(matrix) - 1):
            if matrix[i][j] == matrix[i + 1][j] or matrix[i][j + 1] == matrix[i][j]:
                return 'KEEP GOING'
    for k in range(len(matrix) - 1):
        if matrix[len(matrix) - 1][k] == matrix[len(matrix) - 1][k + 1]:
            return 'KEEP GOING'
    for j in range(len(matrix) - 1):
        if matrix[j][len(matrix) - 1] == matrix[j + 1][len(matrix) - 1]:
            return 'KEEP GOING'
    return 'LOST!'

def compressing_game(matrix):
    status = False
    new_matrix = []
    for j in range(v.LENGTH):
        new_matrix.append([0]*4)
    for i in range(v.LENGTH):
        count = 0
        for j in range(v.LENGTH):
            if matrix[i][j] != 0:
                new_matrix[i][count] = matrix[i][j]
                if j != count:
                    status = True
                count += 1
    return new_matrix, status

def merge(matrix, status):
    for i in range(v.LENGTH):
        for j in range(v.LENGTH-1):
            if matrix[i][j] == matrix[i][j + 1] and matrix[i][j] != 0:
                matrix[i][j] *= 2
                matrix[i][j + 1] = 0
                status = True
    return matrix, status

def reverse(matrix):
    new = []
    for i in range(len(matrix)):
        new.append([])
        for j in range(len(matrix)):
            new[i].append(matrix[i][len(matrix)-j-1])
    return new

def transpose(matrix):
    new = []
    for i in range(len(matrix)):
        new.append([])
        for j in range(len(matrix)):
            new[i].append(matrix[j][i])
    return new

def up(move):
    new_move = transpose(move)
    new_move, status = left(new_move)
    new_move = transpose(new_move)
    return new_move, status

def down(move):
    new_move = transpose(move)
    new_move, status = right(new_move)
    new_move = transpose(new_move)
    return new_move, status

def left(move):
    move, status = compressing_game(move)
    move, status = merge(move, status)
    move = compressing_game(move)[0]
    return move, status

def right(move):
    move = reverse(move)
    move, status = compressing_game(move)
    move, status = merge(move, status)
    move = compressing_game(move)[0]
    move = reverse(move)
    return move, status