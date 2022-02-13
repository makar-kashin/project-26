
"""
подключение модулей
"""
import os
import sys
import pygame
import random

"""
инициализация
"""
FPS = 60  # количество кадров в секунду
WINDOW_SIZE = (800, 450)  # размер окна
# WINDOW_SIZE = (1920, 1080)
JUMP_POWER = 10  # "сила" прыжка
GRAVITY = 0.45  # уровень гравитации

pygame.init()  # инициализия
screen = pygame.display.set_mode(WINDOW_SIZE)  # создание окна
pygame.display.set_caption("Project 26")  # заголовок окна
clock = pygame.time.Clock()  # pygame-часы


class Tile(pygame.sprite.Sprite):
    """
    создание стен и общего окружения
    """
    wall = pygame.image.load("data/wall.png").convert()
    grass = pygame.image.load(f"data/floors/floor_{random.randint(1, 21)}.png").convert()
    images = grass, wall

    grasses = pygame.sprite.Group()
    walls = pygame.sprite.Group()
    groups = grasses, walls

    def __init__(self, x, y, index):
        super().__init__(self.groups[index])
        self.image = self.images[index]
        self.rect = self.image.get_rect(x=x, y=y)


class Hero(pygame.sprite.Sprite):
    """
    создание игрока
    """
    group = pygame.sprite.Group()

    def __init__(self, x, y):
        super().__init__(self.group)
        self.image = pygame.image.load("data/astro.png").convert_alpha()
        self.rect = self.image.get_rect(x=x, y=y)
        self.xvel = 0   #скорость перемещения. 0 - стоять на месте
        self.startX = x # Начальная позиция Х, пригодится когда будем переигрывать уровень
        self.startY = y
        # self.image = Surface((WIDTH,HEIGHT))
        # self.image.fill(Color(COLOR))
        # self.rect = Rect(x, y, WIDTH, HEIGHT) # прямоугольный объект


    def update(self, dx, dy):
        old_rect = self.rect
        self.rect = self.rect.move(dx, dy)
        if not pygame.sprite.spritecollideany(self, Tile.grasses):
            self.rect = old_rect


    def update(self,  left, right):
        if left:
            self.xvel = -MOVE_SPEED # Лево = x- n
 
        if right:
            self.xvel = MOVE_SPEED # Право = x + n
         
        if not(left or right): # стоим, когда нет указаний идти
            self.xvel = 0

        self.rect.x += self.xvel # переносим свои положение на xvel 
   
    def draw(self, screen): # Выводим себя на экран
        screen.blit(self.image, (self.rect.x,self.rect.y))



def load_map(filename):
    """
    загрузка карты .map
    """
    lines = open(filename).readlines()
    maxlen = max(map(len, lines)) - 1
    return [x.rstrip().ljust(maxlen, ".") for x in lines]


def draw_map(filename):
    """
    создание карты
    """
    data = load_map(filename)
    # data, w, h = load_map(filename)
    w, h = len(data), len(data[0])
    surface = pygame.Surface((w * tw, h * th))
    dmap = {".": 0, "#": 1, "@": 2}
    for y in range(h):
        for x in range(w):
            index = dmap[data[y][x]]
            if index == 2:
                hero = Hero(x * tw, y * th)
                index = 0
            
            Tile(x * tw, y * th, index)


    Tile.walls.draw(surface)
    Tile.grasses.draw(surface)

    return surface, hero


def intro(filename):
    """
    создание заставки
    """
    pygame.event.set_blocked(None)
    pygame.event.set_allowed((pygame.QUIT, pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN))
    pygame.event.clear()

    bg = pygame.image.load(filename).convert()
    pygame.transform.scale(bg, WINDOW_SIZE, screen)
    pygame.display.update()
    event = pygame.event.wait()
    return event.type != pygame.QUIT

if not intro("data/intro.png"):
    exit()


bg, hero = draw_map("data/map.map")  # рисование карты и игрока
scene = bg.copy()  # копия окружения БЕЗ игрока
screen.fill(0x4C4C4C)  # заполнение окружения СЕРЫМ цветом
Hero.group.draw(scene)  # рисование игрока на поле
area = screen.get_rect(center=hero.rect.center)  # центрирование экрана по игроку
screen.blit(scene, (0, 0), area)  # отрисовка центрированной поверхности на экране
pygame.display.update()  # обновление экрана


wasd_keys = {
    pygame.K_w: (0, -th),
    pygame.K_a: (-tw, 0),
    pygame.K_s: (0, th),
    pygame.K_d: (tw, 0)
}  # кнопки WASD
rotate_keys = {
    pygame.K_LEFT: 90,
    pygame.K_UP: 180,
    pygame.K_DOWN: 360,
    pygame.K_RIGHT: 270 
}  # кнопки стрелок

pygame.event.set_blocked(None)  # блокирование ВСЕХ ивентов
pygame.event.set_allowed((pygame.QUIT, pygame.KEYDOWN))  # разрешение крестика и нажатий кнопок
pygame.event.clear()  # удаление ВСЕХ ивентов из очереди

while (event := pygame.event.wait()).type != pygame.QUIT:
    """
    main loop
    """
    clock.tick(FPS)
    if event.key in wasd_keys:
        Hero.group.update(wasd_keys[event.key][0], wasd_keys[event.key][1])
        Hero.group.clear(scene, bg)
        Hero.group.draw(scene)
        area = screen.get_rect(center=hero.rect.center)
        screen.fill(0x4C4C4C)
        screen.blit(scene, (0, 0), area)
        pygame.display.update()
    elif event.key in rotate_keys:
        pass

    if event.type == KEYDOWN and event.key == K_LEFT:
       left = True
    if event.type == KEYDOWN and event.key == K_RIGHT:
       right = True

    if event.type == KEYUP and event.key == K_RIGHT:
       right = False
    if event.type == KEYUP and event.key == K_LEFT:
        left = False
