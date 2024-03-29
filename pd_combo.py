# -*- coding: utf-8 -*-
# vim:set foldmethod=marker:

import random
import pprint
import copy
import pprint
import operator
import time
import numpy as np
import sys
import numba

ROW = 5
COL = 6
#MAX_TURN = 40
MAX_TURN = 30
#BEAM_WIDTH = 5000
BEAM_WIDTH = 100

class member(): # route pattern{{{
    def __init__(self, nowC, nowR, prev=-1, length=MAX_TURN):
        self.score = 0  # combo number
        self.nowC  = nowC # now column
        self.nowR  = nowR # now row
        self.prev = prev # previous position (1:up, 2:down, 3:left, 4:right, -1:None)
        self.movei = [[-1] * 2] * length
        #self.movei = np.full(length * 2, -1, dtype=np.int8).reshape(length, 2)
        # }}}

class pd_combo():
    def __init__(self, row=5, col=6, field=None, max_turn=MAX_TURN, beam_width=BEAM_WIDTH):# {{{
        self.row = row
        self.col = col
        self.max_turn = max_turn
        self.beam_width = BEAM_WIDTH
        if field != None:
            self.field = field
        else:
            #self.field = [[0 for _ in range(self.col)] for _ in range(self.row)]
            #self.field = [[0] * self.col] * self.row
            self.field = np.zeros(self.row * self.col, dtype=np.int8).reshape(self.row, self.col)
        #self.chainflag = [[0 for _ in range(self.col)] for _ in range(self.row)]
        #self.chainflag = [[0] * self.col] * self.row
        self.chainflag = np.zeros(self.row * self.col, dtype=np.int8).reshape(self.row, self.col)
        #self.dummy = [[0 for _ in range(self.col)] for _ in range(self.row)]
        #self.dummy = [[0] * self.col] * self.row
        self.dummy = np.zeros(self.row * self.col, dtype=np.int8).reshape(self.row, self.col)
        #self.t_erace = [[0 for _ in range(self.col)] for _ in range(self.row)]
        #self.t_erace = [[0] * self.col] * self.row
        self.t_erace = np.zeros(self.row * self.col, dtype=np.int8).reshape(self.row, self.col)
        self.max_count = 0  # chained drop count
        self.route = [[-1] * 2] * self.max_turn
        #self.f_field = [[0 for _ in range(self.col)] for _ in range(self.row)]
        #self.f_field = [[0] * self.col] * self.row
        self.f_field = np.zeros(self.row * self.col, dtype=np.int8).reshape(self.row, self.col)
        self.max_count = 0  # chained drop count
        self.d_1 = 0 # fire
        self.d_2 = 0 # water
        self.d_3 = 0 # wood
        self.d_4 = 0 # light
        self.d_5 = 0 # dark
        self.d_6 = 0 # cure
# }}}

    def make_field(self):# {{{
        for i in range(self.row):
            for j in range(self.col):
                self.field[i][j] = random.randint(0, 6)# }}}

    def show_field(self):# {{{
        for i in range(self.row):
            for j in range(self.col):
                print(self.field[i, j], end="")
            print("\n", end="")# }}}

    def show_field2(self):# {{{
        for i in range(self.row):
            for j in range(self.col):
                print(self.field[i][j], end="")
            print("\n", end="")# }}}

    def show_f_field(self):# {{{
        for i in range(self.row):
            for j in range(self.col):
                print(self.f_field[i][j], end="")
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
                    self.field[i][j] = random.randint(1, 6)
        # }}}

    def count_drop(self):# {{{
        for i in range(self.row):
            for j in range(self.col):
                if self.field[i][j] == 1:
                    self.d_1 += 1
                elif self.field[i][j] == 2:
                     self.d_2 += 1
                elif self.field[i][j] == 3:
                     self.d_3 += 1
                elif self.field[i][j] == 4:
                     self.d_4 += 1
                elif self.field[i][j] == 5:
                     self.d_5 += 1
                elif self.field[i][j] == 6:
                     self.d_6 += 1
         # }}}

    def swap(self, i1, j1, i2, j2):# {{{
        temp = self.field[i1][j1]
        self.field[i1][j1] = self.field[i2][j2]
        self.field[i2][j2] = temp# }}}

    def operation(self):# {{{
        now_col = self.route[0][0]
        now_row = self.route[0][1]

        for i in range(self.max_turn):
            if self.route[i][0] == -1 or self.route[i][1] == -1:
                break
            self.swap(now_row, now_col, self.route[i][1], self.route[i][0])
            #print("movei[i]:"+str(i))
            #self.show_field()
            now_col = self.route[i][0]
            now_row = self.route[i][1]

        # }}}

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

    def beam_search(self):# {{{
        queue = []
        for i in range(self.row):
            for j in range(self.col):
                cand = member(j, i, -1)
                cand.movei[0]= [j, i]
                queue.append(cand)

        dx = [-1,  0, 0, 1]
        dy = [ 0, -1, 1, 0]

        for p in range(1,self.max_turn):
            pqueue = []
            for q in range(len(queue)):
                temp = copy.deepcopy(queue[q])
                for j in range(len(dx)):
                    self.field = copy.deepcopy(self.f_field)
                    cand = copy.deepcopy(temp)
                    if ( 0 <= temp.nowC + dx[j] < self.col and \
                            0 <= temp.nowR + dy[j] < self.row ):
                        if cand.prev + j == 3:
                            continue
                        cand.nowC = temp.nowC + dx[j]
                        cand.nowR = temp.nowR + dy[j]
                        cand.movei[p] = [cand.nowC, cand.nowR]
                        #print("q:"+str(q)+", p:"+str(p)+", cand.nowC:"+str(cand.nowC)+", cand.nowR:"+str(cand.nowR))
                        #print("cand.movei", end="")
                        #print(cand.movei)
                        self.route = copy.deepcopy(cand.movei)
                        self.operation()
                        #print("operated field")
                        #self.show_field()
                        cand.score = self.sum_e()
                        #print("cand.score:"+str(cand.score))
                        cand.prev = j
                        pqueue.append(cand)

            pqueue.sort(key=operator.attrgetter("score"), reverse=True)
            #print("pqueue[0].score:"+str(pqueue[0].score))
            #print("pqueue[1].score:"+str(pqueue[1].score))

            queue = []
            if self.beam_width < len(pqueue):
                width = self.beam_width
            else:
                width = len(pqueue)
            for i in range(width):
                queue.append(pqueue[i])
            #print("len(queue):"+str(len(queue)))

        return queue[0] # best route(=movei)

# }}}

if __name__ == "__main__":

    avg = 0
    avg_time = time.time() - time.time()
    repeat_count = 1
    for i in range(repeat_count):
        start_time = time.time()
        #pd_cmb = pd_combo(3, 4)
        #pd_cmb = pd_combo(4, 5)
        pd_cmb = pd_combo(ROW, COL)
        #print("pd_cmb.col:"+str(pd_cmb.col))
        #print("pd_cmb.row:"+str(pd_cmb.row))
        #print(pd_cmb.field)
        #print("pd_cmb.field size:"+str(sys.getsizeof(pd_cmb.field)))
        #print(pd_cmb.field.dtype)
        #print("\ninitial field")
        #pd_cmb.show_field()
        pd_cmb.set()  # make initial filed
        print("\nsetted field")
        pd_cmb.show_field()
        #pd_cmb.show_field2()

        pd_cmb.f_field = copy.deepcopy(pd_cmb.field)  # copy initial field
        best_member = pd_cmb.beam_search()  # best member(route, score,,,)
        #print("(x, y): ("+str(best_member.movei[0][0])+", "+str(best_member.movei[0][1])+")")
        #print(best_member.movei)

        #for i in range(pd_cmb.max_turn):
        #    if best_member.movei[i][0] == -1 or best_member.movei[i][1] == -1 :
        #        break
        #    if best_member.movei[i][0] == (best_member.movei[i - 1][0] + 1):
        #        print("RIGHT")
        #    if best_member.movei[i][0] == (best_member.movei[i - 1][0] - 1):
        #        print("LEFT")
        #    if best_member.movei[i][1] == (best_member.movei[i - 1][1] + 1):
        #        print("UP")
        #    if best_member.movei[i][1] == (best_member.movei[i - 1][1] - 1):
        #        print("DOWN")
        #    print("\n")
        pd_cmb.field  = copy.deepcopy(pd_cmb.f_field)
        pd_cmb.route = copy.deepcopy(best_member.movei)
        pd_cmb.operation()
        print("\noperated field")
        pd_cmb.show_field()
        elapsed_time = time.time() - start_time
        #print("elapsed_time:{0}".format(elapsed_time) + "[sec]")
        avg += best_member.score
        avg_time += elapsed_time
    print("avarage score:"+str(avg/repeat_count))
    print("avarage time:{0}".format(avg_time/repeat_count) + str("[sec]"))
