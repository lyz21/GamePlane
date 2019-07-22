"""
敌人飞机类
"""
import pygame

SCREEN_WIDTH = 480
SCREEN_HEIGHT = 640


# 继承精灵类
class Enemy(pygame.sprite.Sprite):
    def __init__(self, image, position):  # 构造方法
        pygame.sprite.Sprite.__init__(self)  # 使用父类构造方法
        self.image = image  # 图片
        self.rect = self.image.get_rect()  # 获取rect对象
        self.rect.topleft = position  # 位置
        self.speed = 2  # 敌机移动速度
        self.boom_index = 0  # 爆炸动画切换索引

    # 更新
    def update(self):
        self.rect.top = self.rect.top + self.speed  # 向下飞
        if self.rect.top > SCREEN_HEIGHT:  # 越界，销毁
            self.kill()
