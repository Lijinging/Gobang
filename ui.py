# coding:utf-8

import pygame
from pygame.locals import *
from sys import exit
import random
from algorithm import *


class GoBang:
    def __init__(self, space=30, size=30, big=15):
        self.space = space
        self.size = size
        self.big = big
        self.stone_w = pygame.image.load(r"res/stone_w.png")
        self.stone_b = pygame.image.load(r"res/stone_b.png")
        self.background = pygame.image.load(r"res/background.jpg")
        self.map = [[S_NULL for col in range(self.big)] for row in range(self.big)]
        self.s_last = None

        pygame.init()
        self.window_size = (width, height) = (space * 2 + (big - 1) * size, space * 2 + (big - 1) * size)
        self.color_white = (255, 255, 255)
        self.screen = pygame.display.set_mode(self.window_size, 0, 32)  # 创建窗口，尺寸为640*480，色深度为32
        self.screen.blit(self.background, (0, 0))
        pygame.display.set_caption("GoBang")  # 设置窗口标题

        self.draw_board()

    def draw_board(self):
        # self.screen.fill(self.color_white)
        self.screen.blit(self.background, (0, 0))
        for i in range(15):
            pygame.draw.aaline(self.screen, (60, 60, 60), (self.space, self.space + i * self.size),
                               (self.space + 14 * self.size, self.space + i * self.size), 1)
            pygame.draw.aaline(self.screen, (60, 60, 60), (self.space + i * self.size, self.space),
                               (self.space + i * self.size, self.space + 14 * self.size), 1)

    def clear(self):
        self.map = [[S_NULL for col in range(self.big)] for row in range(self.big)]
        self.show_map()

    def add_chess(self, pos_x, pos_y, type):
        if gobang.update_map(pos_x, pos_y, type):
            gobang.draw_chess(pos_x, pos_y, type, edge=False)
            self.s_last = [pos_x, pos_y]
            return True
        return False

    def draw_chess(self, pos_x, pos_y, type, edge=False):
        x = gobang.space + pos_x * gobang.size - gobang.stone_b.get_width() / 2
        y = gobang.space + pos_y * gobang.size - gobang.stone_b.get_height() / 2
        if type == S_BLACK:
            self.screen.blit(self.stone_b, (y, x))
        if type == S_WHITE:
            self.screen.blit(self.stone_w, (y, x))

    def update_map(self, x, y, type):
        if self.map[x][y] == S_NULL:
            self.map[x][y] = type
            return True
        return False

    def show(self):
        for i in range(self.big):
            for j in range(self.big):
                if self.map[i][j] == S_NULL:
                    if i == 0:
                        if j == 0:
                            print('┌', end=' ')
                        elif j == self.big - 1:
                            print('┐', end=' ')
                        else:
                            print('┬', end=' ')
                    elif i == self.big - 1:
                        if j == 0:
                            print('└', end=' ')
                        elif j == self.big - 1:
                            print('┘', end=' ')
                        else:
                            print('┴', end=' ')
                    else:
                        if j == 0:
                            print('├', end=' ')
                        elif j == self.big - 1:
                            print('┤', end=' ')
                        else:
                            print('┼', end=' ')
                elif self.map[j][i] == S_BLACK:
                    print('●', end=' ')
                else:
                    print('○', end=' ')
            print()
        print()

    def show_map(self):
        self.draw_board()
        for (i, j) in [(i, j) for i in range(self.big) for j in range(self.big)]:
            if self.map[i][j] != S_NULL:
                self.draw_chess(i, j, self.map[i][j])
        self.draw_last_box()

    def generate_map(self):
        for (i, j) in [(i, j) for i in range(self.big) for j in range(self.big)]:
            index = random.randint(0, 2)
            self.map[i][j] = S_LIST[index]

    def draw_box(self, x, y):
        if x >= 0 and x < self.big and y >= 0 and y < self.big:
            pygame.draw.aalines(self.screen, (80, 100, 160), True,
                                [(self.space + (x - 0.5) * self.size, self.space + (y - 0.5) * self.size),
                                 (self.space + (x - 0.5) * self.size, self.space + (y + 0.5) * self.size),
                                 (self.space + (x + 0.5) * self.size, self.space + (y + 0.5) * self.size),
                                 (self.space + (x + 0.5) * self.size, self.space + (y - 0.5) * self.size)], 1)

    def draw_last_box(self):
        if self.s_last != None:
            pygame.draw.aalines(self.screen, (110, 110, 110), True,
                                [(self.space + (self.s_last[0] - 0.5) * self.size,
                                  self.space + (self.s_last[1] - 0.5) * self.size),
                                 (self.space + (self.s_last[0] - 0.5) * self.size,
                                  self.space + (self.s_last[1] + 0.5) * self.size),
                                 (self.space + (self.s_last[0] + 0.5) * self.size,
                                  self.space + (self.s_last[1] + 0.5) * self.size),
                                 (self.space + (self.s_last[0] + 0.5) * self.size,
                                  self.space + (self.s_last[1] - 0.5) * self.size)], 1)


gobang = GoBang()
frames_per_sec = 30
fps_clock = pygame.time.Clock()
cnt = 0
ai = Brain()

while True:

    for event in pygame.event.get():
        if event.type == QUIT:
            exit()
        if event.type == MOUSEBUTTONDOWN:
            y, x = pygame.mouse.get_pos()
            # 计算对应的左边
            pos_x = int(((x - gobang.space) + gobang.size / 2) / gobang.size)
            pos_y = int(((y - gobang.space) + gobang.size / 2) / gobang.size)
            if pos_x < 0 or pos_x >= 15 or pos_y < 0 or pos_y >= 15:
                continue
            # print(pos_x, pos_y)
            x = gobang.space + pos_x * gobang.size - gobang.stone_b.get_width() / 2
            y = gobang.space + pos_y * gobang.size - gobang.stone_b.get_height() / 2

            if gobang.add_chess(pos_x, pos_y, S_BLACK):
                gobang.show_map()
                pygame.display.update()
                s_next = ai.next(gobang.map, gobang.big)
                print("AI:", s_next)
                while gobang.add_chess(s_next[0], s_next[1], S_WHITE) is False:
                    s_next = ai.next(gobang.map, gobang.big)
                    print("RE AI:", s_next)
                gobang.show_map()
                gobang.show()
                cnt = cnt + 1
        if event.type == MOUSEMOTION:
            x, y = pygame.mouse.get_pos()
            # 计算对应的左边
            pos_x = int(((x - gobang.space) + gobang.size / 2) / gobang.size)
            pos_y = int(((y - gobang.space) + gobang.size / 2) / gobang.size)
            if pos_x < 0 or pos_x >= 15 or pos_y < 0 or pos_y >= 15:
                continue
            gobang.show_map()
            gobang.draw_box(pos_x, pos_y)

        if event.type == pygame.locals.KEYDOWN:
            print(event.key)
            # 按键 g
            if event.key == 103:
                gobang.generate_map()
                gobang.show_map()
            # 按键 r
            if event.key == 114:
                gobang.clear()
                cnt = 0
            # 按键s
            if event.key == 115:
                ai.next(gobang.map, gobang.big)

    pygame.display.update()
    fps_clock.tick(frames_per_sec)
