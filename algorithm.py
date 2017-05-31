# coding: utf-8
import random
import time
import numpy

S_NULL = '.'
S_BLACK = 'b'
S_WHITE = 'w'
S_LIST = [S_NULL, S_BLACK, S_WHITE]


class Brain:
    def transToStr(self, map):
        for i in range(15):
            str = 's'
            for j in range(15):
                str = str + map[j][i]
            str = str + 's'
            print(str)

    def find(self, instr, key):
        pass

    def next(self, map, big):
        self.getValue(map, big)
        index = numpy.array(self.value).argmax()
        return int(index / big), index % big

    def getValue(self, map, big):
        self.value = [[min(col, row, 14 - col, 14 - row) for col in range(big)] for row in range(big)]

        round_index = lambda big, x, y, n: [(i + x, j + y)
                                            for i in [-n, 0, n] for j in [-n, 0, n]
                                            if 0 <= (i + x) < big
                                            if 0 <= (j + y) < big]

        for i in range(big):
            for j in range(big):
                self.value[i][j] = self.value[i][j]

                dis_a = 5
                for dis in range(1, dis_a):

                    if map[i][j] != S_NULL:
                        print(round_index(big, i, j, dis))
                        for index_i, index_j in round_index(big, i, j, dis):
                            if map[index_i][index_j] == S_NULL:
                                self.value[index_i][index_j] = dis_a - dis + self.value[index_i][index_j]

        # for i in range(big):
        #    for j in range(big):
        #        print(self.value[i][j], end=' ')
        #    print()
        # print()

        a = numpy.array(self.value)
        print(a)
        print((a + numpy.random.normal(scale=0.5, size=big*big).reshape((big, big))).argmax())


def ai_next(map):
    return random.randint(0, 14), random.randint(0, 14)
