# -*- coding: utf-8 -*-
# vim:set foldmethod=marker:

import random
import pprint

ROW = 5
COL = 6

field = [[0 for _ in range(COL)] for _ in range(ROW)]
chainflag = [[0 for _ in range(COL)] for _ in range(ROW)]
dummy = [[0 for _ in range(COL)] for _ in range(ROW)]
t_erace = [[0 for _ in range(COL)] for _ in range(ROW)]
route_x = [0] * 100
route_y = [0] * 100
max_count = 0

def init():# {{{
    field = [[random.randint(0, 6) for _ in range(COL)] for _ in range(ROW)]
    return field# }}}

def make_field(field):# {{{
    for i in range(ROW):
        for j in range(COL):
            field[i][j] = random.randint(0, 6)# }}}

def show_field(field):# {{{
    for i in range(ROW):
        for j in range(COL):
            print(field[i][j], end="")
        print("\n", end="")# }}}

def fall(field):# {{{
    for i in range(ROW):
        for j in range(COL):
            for k in range(ROW):
                if k+1 == ROW:
                    break
                if field[k+1][j] == 0:
                    field[k+1][j] = field[k][j]
                    field[k][j] = 0# }}}

def set(field):# {{{
    for i in range(ROW):
        for j in range(COL):
            if field[i][j] == 0:
                field[i][j] = random.randint(1, 6)# }}}

def swap(field, i1, j1, i2, j2):# {{{
    temp = field[i1][j1]
    field[i1][j1] = field[i2][j2]
    field[i2][j2] = temp# }}}

def chain(now_row, now_col, drop, count, max_count):
    # if out of filed range, return
    if now_row == -1 or now_row == ROW or now_col == -1 or now_col == COL:
        return
    # if same color drop is not searced
    if field[now_row][now_col] == drop and chainflag[now_row][now_col] == 0:
        chainflag[now_row][now_col] = -1   # searched
        if max_count < count:
            max_count = count
        dummy[now_row][now_col] = -1

        chain(now_row - 1, now_col, drop, count + 1, max_count)
        chain(now_row + 1, now_col, drop, count + 1, max_count)
        chain(now_row, now_col - 1, drop, count + 1, max_count)
        chain(now_row, now_col + 1, drop, count + 1, max_count)

def check(field):# {{{
    v = 0
    for i in range(ROW):
        for j in range(COL - 2):
            if dummy[i][j] == -1 and dummy[i][j + 1] == -1 and dummy[i][j + 2] == -1 and \
             field[i][j] == field[i][j + 1] and field[i][j] == field[i][j +2]:
                t_erace[i][j] = -1
                t_erace[i][j + 1] = -1
                t_erace[i][j + 2] = -1
                v = 1

    for i in range(ROW - 2):
        for j in range(COL):
            if dummy[i][j] == -1 and dummy[i + 1][j] == -1 and dummy[i + 2][j] == -1 and \
             field[i][j] == field[i + 1][j] and field[i][j] == field[i + 2][j]:
                t_erace[i][j] = -1
                t_erace[i + 1][j] = -1
                t_erace[i + 2][j] = -1
                v = 1
    return v  # 0: 0 combo, 1: some combo
# }}}

def evaluate(field, max_count):# {{{
    value = 0
    chainflag = [[0 for _ in range(COL)] for _ in range(ROW)]
    for i in range(ROW):
        for j in range(COL):
            if chainflag[i][j] == 0 and field[i][j] != 0:
                max_count = 0
                dummy = [[0 for _ in range(COL)] for _ in range(ROW)]
                chain(i, j, field[i][j], 1, max_count)
                if max_count >= 3:
                    if check() == 1:
                        value += 1
    return value# }}}

def sum_e(field, max_count): # {{{
    # consider "otoshi",  not consider "ochikon" , and caliculate combo
    combo = 0
    while(1):
        t_erace = [[0 for _ in range(COL)] for _ in range(ROW)]
        a = evaluate(field, max_count)
        if a == 0:  # when 0 combo, break
            break
        for i in range(ROW):
            for j in range(COL):
                if t_erace[i][j] == -1:
                    field[i][j] = 0  # clear combo drop
        fall(field)
        combo += a# }}}

def operation(field):# {{{
    route_x[0]=0
    route_y[0]=0

    route_x[1]=1
    route_y[1]=0

    route_x[2]=2
    route_y[2]=0

    route_x[3]=3
    route_y[3]=0

    route_x[4]=4
    route_y[4]=0

    route_x[5]=5
    route_y[5]=0

    route_x[6]=6
    route_y[6]=0

    now_col = route_x[0]
    now_row = route_y[0]

    for i in range(6):
        swap(field, now_row, now_col, route_y[i], route_x[i])
        now_col = route_x[i]
        now_row = route_y[i]# }}}

if __name__ == "__main__":
    set(field)
    print("\nsetted field")
    show_field(field)

    operation(field)
    print("\noperated field")
    show_field(field)

    combo = sum_e(field, max_count)
    print("\nafter combo, field")
    show_field(field)
    print("combo:"+str(combo))

