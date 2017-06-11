# coding: utf-8
import random

import numpy
import math
import bottleneck

S_NULL = '.'
S_BLACK = 'b'
S_WHITE = 'w'
S_LIST = [S_NULL, S_BLACK, S_WHITE]

# 这里x代表自己的棋子, o代表对方棋子或者障碍

KEY = {
    # 活四
    6000: [
        '.xxxx.',
        '.x.xxx.',
        '.xx.xx.',
        '.xxx.x'
    ],
    # 冲四、跳四
    5000: [
        '.xxxxo',
        'x.xxxo',
        'xx.xxo',
        'xxx.xo',
        'oxxx.x',
        'oxx.xx',
        'ox.xxx',
        'oxxxx.'
    ],
    # 活三
    2000: [
        '.xxx.',
        '.xx.x.',
        '.x.xx.'
    ],
    # 死三
    0: [
        'oxxxo',
        'oxxx.o',
        'oxx.xo',
        'ox.xxo',
        'o.xxxo'
    ],
    # 冲三、跳三
    800: [
        '..xxxo',
        'oxxx..',
        'oxx.x.',
        'oxx..x',
        'ox.x.x',
        'ox.xx.',
        'ox..xx',
        '..xxxo',
        '.x.xxo',
        'x..xxo',
        '.xx.xo',
        'xx..xo'
    ],
    # 活二、跳二
    420: [
        '.xx..',
        '..xx.',
        '.x.x.',
        '.x..x.'
    ],
    # 冲二
    200: [
        'oxx...',
        'ox.x..',
        'ox..x.',
        'ox...x',
        '...xxo',
        '..x.xo',
        '.x..xo',
        'x...x.'
    ],
    # 一个的
    40:[
        '.x...',
        '..x..',
        '...x.',
        '....x'
    ]
}

def largest_indices(ary, n):
    """Returns the n largest indices from a numpy array."""
    flat = ary.flatten()
    indices = numpy.argpartition(flat, -n)[-n:]
    indices = indices[numpy.argsort(-flat[indices])]
    return numpy.unravel_index(indices, ary.shape)


def transcode(code, self_chess=S_BLACK):
    st = ''.join(['x' if i == self_chess else '.' if i == S_NULL else 'o' for i in code])
    return st



def getValue_one(code):
    #print(code, end=':')
    for v, key_list in KEY.items():
        for key in key_list:
            if code == key:
    #            print(v)
                return v
    #print(0)
    return 0


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

    def next_defense(self, map, big):
        self.getValue(map, big)
        print('max = %d' % self.value_s.max())
        index = self.value_s.argmax()
        print("index = %d" % index)
        return int(index / big), index % big


    def next_MCTS(self, map, big):
        scorearray = self.next_MCTS_step(map, big)
        index = scorearray.argmax()
        return int(index / big), index % big


    # 评分每次加最大值，胜利是20000
    def next_MCTS_step(self, map, big, chess=S_WHITE, lastdeep=1, step=4):
        if lastdeep<0:
            return numpy.zeros((big, big), dtype='int32')
        self.getValue(map, big, False)
        #defense = self.value_s.max()
        #attack = self.value_a.max()
        #score = defense + attack
        indices = largest_indices(self.value_s+self.value_a, step)
        # cnt_w = numpy.sum(self.value_s[indices[:][:3]])
        # cnt_b = numpy.sum(self.value_a[indices[:][:3]])
        scorearray = numpy.zeros((big, big), dtype='int32')
        scorearray[indices[:][:4]] = self.value_s[indices[:][:3]] + self.value_a[indices[:][:3]]
        if chess==S_WHITE:
            next_chess = S_BLACK
        else:
            next_chess = S_WHITE
        for i in range(step):
            map_n = map.copy()
            print('test:(%d,%d)'% (indices[0][i], indices[1][i]))
            map_n[indices[0][i]][indices[1][i]] = chess
            # 进入迭代
            scorestep = self.next_MCTS_step(map_n, big, chess=next_chess, lastdeep=lastdeep-1)
            sum = 0 + numpy.sum(scorestep)
            scorearray[indices[0][i]][indices[1][i]] += sum
        return scorearray




    def next(self, map, big):
        self.getValue(map, big)
        defense = self.value_s.max()
        attack = self.value_a.max()
        print('defense max = %d' % defense)
        print('attack  max = %d' % attack)
        if defense > attack *0.1:
            index = self.value_s.argmax()
        else:
            index = (self.value_a + 0.3*self.value_s).argmax()
        print("index = %d" % index)
        return int(index / big), index % big

    def next_max(self, map, big):
        self.getValue(map, big)
        defense = self.value_s.max()
        attack = self.value_a.max()
        print('defense max = %d' % defense)
        print('attack  max = %d' % attack)
        index = (self.value_s+self.value_a).argmax()
        print("index = %d" % index)
        return int(index / big), index % big


    def getValue(self, map, big, show=True, selfchess=S_WHITE):
        if selfchess==S_WHITE:
            ch_s = S_WHITE
            ch_d = S_BLACK
        else:
            ch_s = S_BLACK
            ch_d = S_WHITE
        # 自己的评分
        self.value_s = numpy.array([[min(col, row, big - col - 1, big - row - 1) for col in range(big)] for row in range(big)])
        # 对方的评分
        self.value_a = numpy.array([[min(col, row, big - col - 1, big - row - 1) for col in range(big)] for row in range(big)])



        #左右方向
        for i in range(big):
            for j in range(big - 6):
                index = [numpy.array([i] * 7), numpy.arange(j, j + 7)]
                for k in range(5, 8):
                    index_v = [index[0][1:k] - 1, index[1][1:k] - 1]
                    code_s = transcode(map[index_v[0], index_v[1]].tolist(), ch_s)
                    code_a = transcode(map[index_v[0], index_v[1]].tolist(), ch_d)
                    self.value_s[index_v[0], index_v[1]] += getValue_one(code_a)
                    self.value_a[index_v[0], index_v[1]] += getValue_one(code_s)
        #上下方向
        for j in range(big):
            for i in range(big - 6):
                index = [numpy.arange(i, i + 7), numpy.array([j] * 7)]
                for k in range(5, 8):
                    index_v = [index[0][1:k] - 1, index[1][1:k] - 1]
                    code_s = transcode(map[index_v[0], index_v[1]].tolist(), ch_s)
                    code_a = transcode(map[index_v[0], index_v[1]].tolist(), ch_d)
                    self.value_s[index_v[0], index_v[1]] += getValue_one(code_a)
                    self.value_a[index_v[0], index_v[1]] += getValue_one(code_s)

        #上左 下右
        for i in range(big - 6):
            for j in range(big - 6):
                index = [numpy.arange(i, i + 7), numpy.arange(j, j + 7)]
                for k in range(5, 8):
                    index_v = [index[0][1:k] - 1, index[1][1:k] - 1]
                    code_s = transcode(map[index_v[0], index_v[1]].tolist(), ch_s)
                    code_a = transcode(map[index_v[0], index_v[1]].tolist(), ch_d)
                    self.value_s[index_v[0], index_v[1]] += int(getValue_one(code_a)*1.2)
                    self.value_a[index_v[0], index_v[1]] += int(getValue_one(code_s)*1.2)

        for i in range(6, big):
            for j in range(big - 6):
                index = [numpy.arange(i, i - 7, -1), numpy.arange(j, j + 7)]
                for k in range(5, 8):
                    index_v = [index[0][1:k] - 1, index[1][1:k] - 1]
                    code_s = transcode(map[index_v[0], index_v[1]].tolist(), ch_s)
                    code_a = transcode(map[index_v[0], index_v[1]].tolist(), ch_d)
                    self.value_s[index_v[0], index_v[1]] += int(getValue_one(code_a)*1.2)
                    self.value_a[index_v[0], index_v[1]] += int(getValue_one(code_s)*1.2)







        for i in range(big):
            for j in range(big):
                if map[i][j] != S_NULL:
                    self.value_s[i][j] = 0
                    self.value_a[i][j] = 0

        if show:
            print(numpy.array_str(self.value_s, 100))
        self.value_s = self.value_s.astype('float')
        self.value_s += numpy.random.normal(scale=0.5, size=big ** 2).reshape((big, big))
        if show:
            print((self.value_s + numpy.random.normal(scale=0.5, size=big ** 2).reshape(
                (big, big))).argmax())

    def getValue_near(self, map, big):
        self.value = numpy.array([[min(col, row, 14 - col, 14 - row) for col in range(big)] for row in range(big)])

        round_index = lambda big, x, y, n: [(i + x, j + y)
                                            for i in range(-n, n + 1) for j in range(-n, n + 1)
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

        for i in range(big):
            for j in range(big):
                if map[i][j] != S_NULL:
                    self.value[i][j] = 0

        # for i in range(big):
        #    for j in range(big):
        #        print(self.value[i][j], end=' ')
        #    print()
        # print()

        print(self.value)
        print((self.value + numpy.random.normal(scale=0.5, size=big * big).reshape((big, big))).argmax())


def ai_next(map):
    return random.randint(0, 14), random.randint(0, 14)
