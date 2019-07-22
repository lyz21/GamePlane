"""
精灵测试
"""
import pygame
from random import randint
from sys import exit
from pygame.locals import *

SCREEN_WIDTH = 480
SCREEN_HEIGHT = 640


# 继承Sprite精灵类
class Player(pygame.sprite.Sprite):
    # 构造函数
    def __init__(self, init_position):
        pygame.sprite.Sprite.__init__(self)  # 父类构造函数
        '''精灵图片：加载图片（1）或者绘制（2）'''
        # 方法（1）
        # self.image = pygame.image.load('resources/images/enemy.png')
        # 方法（2）
        self.image = pygame.Surface([10, 20])  # 绘制大小
        self.image.fill((0, 0, 0))  # 填充颜色
        self.rect = self.image.get_rect()
        self.rect.topleft = init_position
        self.speed = 1

    # 每个精灵组执行update，组内所有精灵都会update
    def update(self):
        self.rect.top = self.rect.top + self.speed
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()


# 初始化pygame
pygame.init()
# 初始化窗口
screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
# 窗口标题
pygame.display.set_caption('精灵类测试')
# 建立精灵组
group = pygame.sprite.Group()
# 创建时钟对象（可控制游戏循环频率）
clock = pygame.time.Clock()
# 主循环
while True:
    # 通过时钟对象指定循环频率(每秒60次)
    clock.tick(60)
    # 绘制背景
    screen.fill((255, 255, 255))
    # 往精灵组添加精灵
    group.add(
        Player(
            (randint(0, SCREEN_WIDTH), randint(0, SCREEN_HEIGHT))
        )
    )
    # 更新精灵组
    group.update()
    # 绘制精灵组
    group.draw(screen)
    # 界面更新
    pygame.display.update()
    # 退出
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()
