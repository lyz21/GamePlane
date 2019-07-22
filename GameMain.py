import pygame
from sys import exit
from Hero import Hero
from Enemy import Enemy
from random import randint

# 计数，根据计数做一些定时操作
tick = 0
# 创建时钟对象控制游戏帧率
clock = pygame.time.Clock()
# 游戏帧率(每秒刷新次数)
RATE = 60
# 玩家射击速度
SHOOT_SPEED = 40
# 敌机增加速度
ENEMY_ADD_SPEED = 60
# 设置按键状态，用字典存储。字典中存储的键是前后左右四个按键值，后面数字对相应该方向移动距离
offset = {pygame.K_LEFT: 0, pygame.K_RIGHT: 0, pygame.K_UP: 0, pygame.K_DOWN: 0}
# 窗口分辨率
SCREEN_WIDTH = 480
SCREEN_HEIGHT = 640
# 载入背景图片
background_img = pygame.image.load('resources/images/background.png')
# 载入游戏结束图片
gameover_img = pygame.image.load('resources/images/fail.png')

'载入玩家战斗机'
# 玩家战斗机图片
player_plane_image = pygame.image.load('resources/images/feiji.png')
# 取出不带火焰的飞机部分
player_plane_imageA = player_plane_image.subsurface(pygame.Rect(0, 0, 102, 89))
# 取出带火焰的飞机部分
player_plane_imageB = player_plane_image.subsurface(pygame.Rect(0, 0, 102, 109))
# 用列表存储图像
player_plane_images = []
player_plane_images.append(player_plane_imageA)
player_plane_images.append(player_plane_imageB)
# 玩家飞机出现位置
hero_position = [200, 400]
# 创建玩家
hero = Hero(player_plane_image, hero_position)
# 载入子弹图片
bullet_img = pygame.image.load('resources/images/bullet.png')
'载入敌机'
# 敌机图片
enemy_image = pygame.image.load('resources/images/enemy.png')
# 敌机组
enemy_group = pygame.sprite.Group()
'载入爆炸动画'
# 载入爆炸图片
boom_img = pygame.image.load('resources/images/boom.png')
# 对爆炸图片进行切割，切成四个图片，轮换播放，形成爆炸动画效果
boom_img1 = boom_img.subsurface(pygame.Rect(0, 0, 71, 85))
boom_img2 = boom_img.subsurface(pygame.Rect(66, 0, 71, 85))
boom_img3 = boom_img.subsurface(pygame.Rect(131, 0, 71, 85))
boom_img4 = boom_img.subsurface(pygame.Rect(206, 0, 80, 85))
# 将爆炸图片存入列表中
boom_imgs = []
boom_imgs.append(boom_img1)
boom_imgs.append(boom_img2)
boom_imgs.append(boom_img3)
boom_imgs.append(boom_img4)
# 击毁组，存储需要展示爆炸动画的精灵
boom_group = pygame.sprite.Group()
'''初始化界面'''
# 初始化pygame
pygame.init()
# 初始化窗口
screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
# 设置窗口标题
pygame.display.set_caption('飞机大战')
'分数相关'
# 可用下面方法打印可用字体
# print(pygame.font.get_fonts())
# 设置字体及大小
font = pygame.font.SysFont("方正小标宋简体", 20)
# 分数
score = 0
'''事件循环'''
while True:
    # 设定游戏帧率
    clock.tick(RATE)
    # 绘制背景
    screen.blit(background_img, (0, 0))
    '''分数相关'''
    # 连接文字
    score_text = '成绩：' + str(score)
    # 生成surface
    score_surface = font.render(score_text, True, (0, 0, 0))
    # 绘制出文字
    screen.blit(score_surface, (10, 10))
    '''玩家飞机相关'''
    # 根据计数切换飞机图片
    if tick % 13 == 0:
        hero.image = player_plane_images[tick % 2]
    # 调用射击方法
    if tick % SHOOT_SPEED == 0:
        hero.shoot(bullet_img)
    # 更新子弹
    hero.bullet_group.update()
    # 绘制子弹
    hero.bullet_group.draw(screen)
    # 绘制玩家飞机
    screen.blit(hero.image, hero.rect)
    '''敌机相关'''
    # 根据计数添加敌机
    if tick % ENEMY_ADD_SPEED == 0:
        enemy_group.add(
            Enemy(
                enemy_image, (randint(0, SCREEN_WIDTH - 50), -49)  # 50,49是飞机的宽高
            )
        )
    # 更新敌机组
    enemy_group.update()
    # 将敌机组显示到界面
    enemy_group.draw(screen)
    '''敌机与子弹碰撞处理'''
    # 碰撞检测(groupcollide()方法为检测group与group之间的碰撞，后面两个True分别代表是否kill掉相碰撞的两个精灵)
    enemy_down_list = pygame.sprite.groupcollide(enemy_group, hero.bullet_group, True, True)
    if len(enemy_down_list) > 0:
        score += 1
        boom_group.add(enemy_down_list)  # 若发生碰撞，将碰撞的精灵加入击毁组
    '''敌机与玩家碰撞处理'''
    # 碰撞检测(参数：sprite,group,后面的True是指kill掉碰撞的group内的精灵)
    hero_down = pygame.sprite.spritecollide(hero, enemy_group, True)
    # 如果hero_down长度大于0，则证明玩家发生碰撞，游戏结束
    if len(hero_down) > 0:
        # 敌机爆炸
        boom_group.add(hero_down)
        # 战机被击中标志位改为True
        hero.isHit = True
    # 玩家爆炸
    if hero.isHit:
        hero.image = boom_imgs[hero.boom_index]  # 切换玩家图片
        hero.boom_index += 1  # 更新索引
        if hero.boom_index >= 4:  # 爆炸动画结束
            break
    # 敌机爆炸动画
    for boom_sprite in boom_group:
        # 绘制画面
        screen.blit(boom_imgs[boom_sprite.boom_index], boom_sprite.rect)
        if tick % 6 == 0:
            if boom_sprite.boom_index < 3:
                boom_sprite.boom_index = boom_sprite.boom_index + 1  # 更新索引
            else:
                boom_group.remove(boom_sprite)  # 爆炸动画结束，将精灵移除
    # 更新计数
    tick = tick + 1
    # 更新屏幕
    pygame.display.update()
    # 处理按键
    for event in pygame.event.get():
        # 游戏退出
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        # 按键按下
        if event.type == pygame.KEYDOWN:
            # 是否在offset字典中，即按下的是否是前后左右四个键
            if event.key in offset:
                # 在的话，将该方向的移动值设置为相应的值
                offset[event.key] = hero.speed
        # 按键松开
        if event.type == pygame.KEYUP:
            # 是否在offset字典中，即按下的是否是前后左右四个键
            if event.key in offset:
                # 在的话，将该方向的移动值归0
                offset[event.key] = 0
    # 调用移动方法
    hero.move(offset)
# 绘制游戏结束图片
screen.blit(gameover_img, (0, 0))
# 绘制分数
screen.blit(score_surface, (10, 10))
# 更新画面
pygame.display.update()
# 用一个while循环，可停留在最后这个画面
while True:
    # 处理退出
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
