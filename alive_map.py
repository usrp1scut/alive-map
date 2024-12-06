import pygame
import random
import sys
import math
# 初始化 Pygame
pygame.init()
# 设置窗口尺寸
screen_width, screen_height = 1366, 768
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('霍格沃兹活点地图')

#起始和终结点位
start = (random.randint(0, 100),random.randint(0, screen_height/4))
end = (random.randint(screen_width - 100, screen_width),random.randint(screen_height/2, screen_height))

# 颜色定义
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# 设置脚印图片（你可以使用自己的脚印图片）
footprint_img = pygame.image.load('footprints-41236.png')
footprint_img = pygame.transform.scale(footprint_img,(50,50))

# 脚印类
class Footprint(pygame.sprite.Sprite):
    def __init__(self, x, y,a):
        super().__init__()
        self.image = pygame.transform.rotate(footprint_img,a)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.opacity = 500  # 脚印的透明度
        self.life_time = 600  # 脚印的生命周期（帧数）

    def update(self):
        # 模拟脚印的移动
        #self.rect.x += random.randint(-5, 5)
        # self.rect.y += -5

        # 脚印逐渐淡出
        if self.opacity > 0:
            self.opacity -= 5  # 每次减少透明度
            self.image.set_alpha(self.opacity)
        else:
            self.kill()  # 透明度为0时删除脚印

# 创建精灵组
all_sprites = pygame.sprite.Group()

# 脚印生成函数
def generate_footprint(x,y,a):
    footprint = Footprint(x,y,a)
    all_sprites.add(footprint)

#路径生成函数
def gen_path(s,e):
    path = [s]
    while path[-1] != e:
        x = random.randint(30, 50)
        y = random.randint(-30, 30)
        next = (path[-1][0] + x,path[-1][1]+y)
        if 0 <= next[0]<=screen_width and 0<= next[1] <= screen_height:
            path.append(next)
        else:
            break
    return path
# 计算两点角度
def get_angle(p1,p2):
    return math.degrees(math.atan2(p2[1]-p1[1], p2[0]-p1[0]))
# 主循环
clock = pygame.time.Clock()
# 创建初始脚印
generate_footprint(start[0],start[1],0)
p = gen_path(start,end)
# p = [[100,100],[150,150],[200,200],[250,250],[300,300],[350,350]]
i = 0
angle = [0]
# 游戏主循环
running = True
while running:
    screen.fill(WHITE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # 每隔一段时间生成一个新的脚印
    if random.random() < 0.07:  # 控制脚印生成的频率
        i += 1
        if i >= len(p)-1:
            break
        angle.append(- get_angle(p[i-1],p[i+1]))
        print(angle[i])
        generate_footprint(p[i][0],p[i][1],angle[i])
    # 更新和绘制所有脚印
    all_sprites.update()
    all_sprites.draw(screen)

    # 更新显示
    pygame.display.flip()

    # 控制帧率
    clock.tick(30)

pygame.quit()
sys.exit()
