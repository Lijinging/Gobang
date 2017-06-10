# coding: utf-8
import random
import time
import numpy

S_NULL = '.'
S_BLACK = 'b'
S_WHITE = 'w'
S_LIST = [S_NULL, S_BLACK, S_WHITE]


# 这里x代表自己的棋子, o代表对方棋子或者障碍

KEY = {
    # 活四
    6000:[
        '.xxxx.'
    ],
    # 冲四、跳四
    5000:[
        '.xxxxo',
        'xxx.x',
        'xx.xx',
        'x.xxx',
        'oxxxx.'
    ],
    # 活三
    2000:[
        '.xxx.',
        '.xx.x.',
        '.x.xx.'
    ],
    # 死三
    0:[
        'oxxxo',
        'oxxx.o',
        'oxx.xo',
        'ox.xxo',
        'o.xxxo'
    ],
    # 冲三、跳三
    1000:[
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
    400:[
        '.xx.',
        '.x.x.',
        '.x..x.'
    ],
    # 冲二
    200:[
        'oxx...',
        'ox.x..',
        'ox..x.',
        'ox...x',
        '...xxo',
        '..x.xo',
        '.x..xo',
        'x...x.'
    ]
}





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
        self.getValue_near(map, big)
        index = self.value.argmax()
        return int(index / big), index % big

    def getValue_near(self, map, big):
        self.value = numpy.array([[min(col, row, 14 - col, 14 - row) for col in range(big)] for row in range(big)])

        round_index = lambda big, x, y, n: [(i + x, j + y)
                                            for i in range(-n, n+1) for j in range(-n, n+1)
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
        print((self.value + numpy.random.normal(scale=0.5, size=big*big).reshape((big, big))).argmax())


def ai_next(map):
    return random.randint(0, 14), random.randint(0, 14)
