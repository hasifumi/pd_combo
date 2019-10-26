# -*- coding: utf-8 -*-
# vim:set foldmethod=marker:

import random
import pprint

ROW = 5
COL = 6

field = [[0 for _ in range(COL)] for _ in range(ROW)]
chainflag = [[0 for _ in range(COL)] for _ in range(ROW)]
dummy = [[0 for _ in range(COL)] for _ in range(ROW)]
route_x = [0] * 100
route_y = [0] * 100
#print("len route_x:"+str(len(route_x))+", len(route_y):"+str(len(route_y)))

def init():
    field = [[random.randint(0, 6) for _ in range(COL)] for _ in range(ROW)]
    return field

def make_field(field):
    for i in range(ROW):
        for j in range(COL):
            field[i][j] = random.randint(0, 6)

def show_field(field):
    for i in range(ROW):
        for j in range(COL):
            print(field[i][j], end="")
        print("\n", end="")

def fall(field):
    for i in range(ROW):
        for j in range(COL):
            for k in range(ROW):
                if k+1 == ROW:
                    break
                if field[k+1][j] == 0:
                    field[k+1][j] = field[k][j]
                    field[k][j] = 0

def set(field):
    for i in range(ROW):
        for j in range(COL):
            if field[i][j] == 0:
                field[i][j] = random.randint(1, 6)

def chain(now_row, now_col, d, count):
    # if out of filed range, return
    if now_row == -1 or now_row == ROW or now_col == -1 or now_col == COL:
        return
    # if same color drop is not searced
    if field[now_row][now_col] == d and chainflag[now_row][now_col] == 0:
        chainflag[now_row][now_col] = -1   # searched
        if max_count < count:
            max_count = count
        dummy[now_row][now_col] = -1

        chain(now_row - 1, now_col, d, count + 1)
        chain(now_row + 1, now_col, d, count + 1)
        chain(now_row, now_col - 1, d, count + 1)
        chain(now_row, now_col + 1, d, count + 1)

def swap(field, i1, j1, i2, j2):
    temp = field[i1][j1]
    field[i1][j1] = field[i2][j2]
    field[i2][j2] = temp

def operation(field):
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

    now_col = route_x[0]
    now_row = route_y[0]

    for i in range(5):
        swap(field, now_row, now_col, route_y[i], route_x[i])
        now_col = route_x[i]
        now_row = route_y[i]


if __name__ == "__main__":
    #field = init()
    #print("init field")

    #print("pre field")
    #show_field(field)

    #make_field(field)
    #print("\nmade field")
    #show_field(field)

    #fall(field)
    #print("\nfalled field")
    #show_field(field)

    set(field)
    print("\nsetted field")
    show_field(field)

    operation(field)
    print("\noperated field")
    show_field(field)


