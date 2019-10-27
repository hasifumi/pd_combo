# -*- coding: utf-8 -*-
# vim:set foldmethod=marker:

import random
import pprint

ROW = 5
COL = 6

class pd_combo():
    def __init__(self, row, col, field=None):# {{{
        self.row = row
        self.col = col
        if field != None:
            self.field = field
        else:
            self.field = [[0 for _ in range(col)] for _ in range(row)]
        self.chainflag = [[0 for _ in range(col)] for _ in range(row)]
        self.dummy = [[0 for _ in range(col)] for _ in range(row)]
        self.t_erace = [[0 for _ in range(col)] for _ in range(row)]
        self.route_x = [0] * 100
        self.route_y = [0] * 100
        self.max_count = 0# }}}  # chained drop count

    def make_field(self):# {{{
        for i in range(self.row):
            for j in range(self.col):
                self.field[i][j] = random.randint(0, 6)# }}}

    def show_field(self):# {{{
        for i in range(self.row):
            for j in range(self.col):
                print(self.field[i][j], end="")
            print("\n", end="")# }}}

    def show_chainflag(self):# {{{
        for i in range(self.row):
            for j in range(self.col):
                print(self.chainflag[i][j], end="")
            print("\n", end="")# }}}

    def show_dummy(self):# {{{
        for i in range(self.row):
            for j in range(self.col):
                print(self.dummy[i][j], end="")
            print("\n", end="")# }}}

    def show_t_erace(self):# {{{
        for i in range(self.row):
            for j in range(self.col):
                print(self.t_erace[i][j], end="")
            print("\n", end="")# }}}

    def fall(self):# {{{
        for i in range(self.row):
            for j in range(self.col):
                for k in range(self.row):
                    if k+1 == self.row:
                        break
                    if self.field[k+1][j] == 0:
                        self.field[k+1][j] = self.field[k][j]
                        self.field[k][j] = 0# }}}

    def set(self):# {{{
        for i in range(self.row):
            for j in range(self.col):
                if self.field[i][j] == 0:
                    self.field[i][j] = random.randint(1, 6)# }}}

    def swap(self, i1, j1, i2, j2):# {{{
        temp = self.field[i1][j1]
        self.field[i1][j1] = self.field[i2][j2]
        self.field[i2][j2] = temp# }}}

    def operation(self):# {{{
        self.route_x[0]=0
        self.route_y[0]=0

        self.route_x[1]=1
        self.route_y[1]=0

        self.route_x[2]=2
        self.route_y[2]=0

        self.route_x[3]=3
        self.route_y[3]=0

        self.route_x[4]=4
        self.route_y[4]=0

        self.route_x[5]=5
        self.route_y[5]=0

        self.route_x[6]=6
        self.route_y[6]=0

        now_col = self.route_x[0]
        now_row = self.route_y[0]

        for i in range(6):
            self.swap(now_row, now_col, self.route_y[i], self.route_x[i])
            now_col = self.route_x[i]
            now_row = self.route_y[i]# }}}

    def chain(self, now_row, now_col, drop, count):# {{{
        # if out of filed range, return
        if now_row == -1 or now_row == self.row or now_col == -1 or now_col == self.col:
            return
        # if same color drop is not searced
        if self.field[now_row][now_col] == drop and self.chainflag[now_row][now_col] == 0:
            self.chainflag[now_row][now_col] = -1   # searched
            if self.max_count < count:
                self.max_count = count
            self.dummy[now_row][now_col] = -1

            self.chain(now_row - 1, now_col, drop, count + 1)
            self.chain(now_row + 1, now_col, drop, count + 1)
            self.chain(now_row, now_col - 1, drop, count + 1)
            self.chain(now_row, now_col + 1, drop, count + 1)# }}}

    def evaluate(self):# {{{
        value = 0
        self.chainflag = [[0 for _ in range(self.col)] for _ in range(self.row)]
        for i in range(self.row):
            for j in range(self.col):
                if self.chainflag[i][j] == 0 and self.field[i][j] != 0:
                    max_count = 0
                    self.dummy = [[0 for _ in range(self.col)] for _ in range(self.row)]
                    self.chain(i, j, self.field[i][j], 1)
                    if self.max_count >= 3:
                        if self.check() == 1:
                            value += 1
        return value# }}}

    def check(self):# {{{
        # if drop chain 3 times over, return 1
        v = 0
        for i in range(self.row):
            for j in range(self.col - 2):
                if self.dummy[i][j] == -1 and self.dummy[i][j + 1] == -1 and self.dummy[i][j + 2] == -1 and \
                 self.field[i][j] == self.field[i][j + 1] and self.field[i][j] == self.field[i][j +2]:
                    self.t_erace[i][j] = -1
                    self.t_erace[i][j + 1] = -1
                    self.t_erace[i][j + 2] = -1
                    v = 1

        for i in range(self.row - 2):
            for j in range(self.col):
                if self.dummy[i][j] == -1 and self.dummy[i + 1][j] == -1 and self.dummy[i + 2][j] == -1 and \
                 self.field[i][j] == self.field[i + 1][j] and self.field[i][j] == self.field[i + 2][j]:
                    self.t_erace[i][j] = -1
                    self.t_erace[i + 1][j] = -1
                    self.t_erace[i + 2][j] = -1
                    v = 1
        return v  # 0: 0 combo, 1: some combo
    # }}}

    def sum_e(self): # {{{
        # consider "otoshi",  not consider "ochikon" , and caliculate combo
        combo = 0
        while(1):
            self.t_erace = [[0 for _ in range(self.col)] for _ in range(self.row)]
            a = self.evaluate()
            if a == 0:  # when 0 combo, break
                break
            for i in range(self.row):
                for j in range(self.col):
                    if self.t_erace[i][j] == -1:
                        self.field[i][j] = 0  # clear combo drop
            self.fall()
            combo += a
        return combo # }}}


if __name__ == "__main__":
    pd_cmb = pd_combo(ROW, COL)

    pd_cmb.set()
    print("\nsetted field")
    pd_cmb.show_field()

    pd_cmb.operation()
    print("\noperated field")
    pd_cmb.show_field()

    combo = pd_cmb.sum_e()
    print("\ncombo:"+str(combo))

