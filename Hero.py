"""
玩家飞机类
"""

import pygame

# 窗口分辨率
SCREEN_WIDTH = 480
SCREEN_HEIGHT = 640


# 子弹类
class Bullet(pygame.sprite.Sprite):
    def __init__(self, image, position):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = position
        self.speed = 4

    def update(self):
        self.rect.top = self.rect.top - self.speed
        if self.rect.top <= -self.rect.height:
            self.kill()


# 英雄飞机类
class Hero():
    def __init__(self, hero_surface, hero_init_position):
        self.image = hero_surface
        self.rect = self.image.get_rect()  # get_rect返回一个矩形rect对象
        self.rect.topleft = hero_init_position  # 矩形位置（定左上角的位置）
        # 移动速度
        self.speed = 3
        # 子弹精灵组
        self.bullet_group = pygame.sprite.Group()
        # 是否被击中
        self.isHit=False
        # 爆炸动画切换索引
        self.boom_index = 0

    def move(self, offset):
        x = self.rect.left + offset[pygame.K_RIGHT] - offset[pygame.K_LEFT]
        y = self.rect.top + offset[pygame.K_DOWN] - offset[pygame.K_UP]
        # 若最左边坐标小于0，即出左边界，设为0
        if x < 0:
            self.rect.left = 0
        # 若最左边坐标大于界面宽度-飞机宽度，即出右边界，设为右边界值
        elif x > SCREEN_WIDTH - self.rect.width:
            self.rect.left = SCREEN_WIDTH - self.rect.width
        # 其他即为正常情况
        else:
            self.rect.left = x
        # 若最上边坐标小于0，即出上边界，设为0
        if y < 0:
            self.rect.top = 0
        # 若最上边坐标大于界面高度-飞机高度，即出下边界，设为下边界值
        elif y > SCREEN_HEIGHT - self.rect.height:
            self.rect.top = SCREEN_HEIGHT - self.rect.height
        # 其他视为正常情况
        else:
            self.rect.top = y

    # 射击方法
    def shoot(self, bullet_img):
        self.bullet_group.add(
            Bullet(bullet_img, self.rect.midtop)
        )
