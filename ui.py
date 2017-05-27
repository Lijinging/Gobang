# coding:utf-8

import pygame
from pygame.locals import *
from sys import exit
import random

S_NULL = 'n'
S_BLACK = 'b'
S_WHITE = 'w'
S_LIST = [S_NULL, S_BLACK, S_WHITE]


class GoBang:
    def __init__(self, space=30, size=30, big=15):
        self.space = space
        self.size = size
        self.big = big
        self.stone_w = pygame.image.load(r"res/stone_w.png")
        self.stone_b = pygame.image.load(r"res/stone_b.png")
        self.background = pygame.image.load(r"res/background.jpg")
        self.map = [[S_NULL for col in range(self.big)] for row in range(self.big)]

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

    def add_chess(self, pos_x, pos_y, type):
        if gobang.update_map(pos_x, pos_y, type):
            gobang.draw_chess(pos_x, pos_y, type, edge=False)
            return True
        return  False

    def draw_chess(self, pos_x, pos_y, type, edge=False):
        x = gobang.space + pos_x * gobang.size - gobang.stone_b.get_width() / 2
        y = gobang.space + pos_y * gobang.size - gobang.stone_b.get_height() / 2
        if type == S_BLACK:
            self.screen.blit(self.stone_b, (x, y))
        if type == S_WHITE:
            self.screen.blit(self.stone_w, (x, y))

    def update_map(self, x, y, type):
        if self.map[x][y] == S_NULL:
            self.map[x][y] = type
            return True
        return False

    def show_map(self):
        self.draw_board()
        for (i, j) in [(i, j) for i in range(self.big) for j in range(self.big)]:
            if self.map[i][j] != S_NULL:
                self.draw_chess(i, j, self.map[i][j])

    def generate_map(self):
        for (i, j) in [(i, j) for i in range(self.big) for j in range(self.big)]:
            index = random.randint(0, 2)
            self.map[i][j] = S_LIST[index]


gobang = GoBang()
frames_per_sec = 30
fps_clock = pygame.time.Clock()
cnt = 0

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            exit()
        if event.type == MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            # 计算对应的左边
            pos_x = int(((x - gobang.space) + gobang.size / 2) / gobang.size)
            pos_y = int(((y - gobang.space) + gobang.size / 2) / gobang.size)
            print(pos_x, pos_y)
            x = gobang.space + pos_x * gobang.size - gobang.stone_b.get_width() / 2
            y = gobang.space + pos_y * gobang.size - gobang.stone_b.get_height() / 2
            if cnt % 2 == 0:
                type = S_BLACK
            else:
                type = S_WHITE
            if gobang.add_chess(pos_x, pos_y, type):
                cnt = cnt + 1
        if event.type == pygame.locals.KEYDOWN:
            print(event.key)
            # 按键 g
            if event.key == 103:
                gobang.generate_map()
                gobang.show_map()

    pygame.display.update()
    fps_clock.tick(frames_per_sec)



    # space = 10
    # size = 30
    # big = 15
    #
    # pygame.init()
    # window_size = (width, height) = (space * 2 + (big - 1) * size, space * 2 + (big - 1) * size)
    # color_white = (255, 255, 255)
    # screen = pygame.display.set_mode(window_size, 0, 32) #创建窗口，尺寸为640*480，色深度为32
    # screen.fill(color_white)
    # pygame.display.set_caption("GoBang") #设置窗口标题
    # stone_w = pygame.image.load(r"res/stone_w.png")
    # stone_b = pygame.image.load(r"res/stone_b.png")
    #
    # def draw_board(space = 10, size=30):
    #    for i in range(15):
    #        pygame.draw.aaline(screen, (0, 0, 0), (space, space + i * size), (space + 14 * size, space + i * size), 1)
    #        pygame.draw.aaline(screen, (0, 0, 0), (space + i * size, space), (space + i * size, space + 14 * size), 1)
    #    pass
    #
    # def draw_chess(x, y, c, edge = False):
    #    x = x
    #    y = y
    #    if c == 'w':
    #        screen.blit(stone_w, (x, y))
    #    else:
    #        screen.blit(stone_b, (x, y))
    #
    #
    # frames_per_sec = 30
    # fps_clock = pygame.time.Clock()
    # cnt = 0
    # draw_board()
    #
    # while True:
    #    for event in pygame.event.get():
    #        if event.type == QUIT:
    #            exit()
    #        if event.type == MOUSEBUTTONDOWN:
    #            x, y = pygame.mouse.get_pos()
    #
    #
    #            #计算对应的左边
    #            pos_x = int(((x - space) + size / 2) / size)
    #            pos_y = int(((y - space) + size / 2) / size)
    #            print(pos_x, pos_y)
    #            x = space + pos_x * size - stone_b.get_width() / 2
    #            y = space + pos_y * size - stone_b.get_height() / 2
    #
    #            if cnt % 2 == 0:
    #                draw_chess(x, y, 'b', edge=False)
    #            else:
    #                draw_chess(x, y, 'w', edge=False)
    #            cnt = cnt + 1
    #
    #
    #
    #
    #
    #    pygame.display.update()
    #    fps_clock.tick(frames_per_sec)
    #
    #
