import pygame
import os
import sys
import time
import random
import uuid


def load_image(name, color_key=None):
    fullname = os.path.join('data', name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error as message:
        print('Не удаётся загрузить:', name)
        raise SystemExit(message)
    image = image.convert_alpha()
    if color_key is not None:
        if color_key is -1:
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)
    return image


pygame.init()
screen_size = (500, 500)
screen = pygame.display.set_mode(screen_size)
clock = pygame.time.Clock()
FPS = 50

tile_images = {
    'brick': load_image('brick.png'),
    'steel': load_image('steel.png'),
    'empty': load_image('empty.png'),
    'grass': load_image('grass.png')
}
player_image = load_image('tank.png')
tile_width = tile_height = 16


class SpriteGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()


#    def get_event(self, event):
#       for sprite in self:
#          sprite.get_event(event)


sprite_group = SpriteGroup()
hero_group = SpriteGroup()


class ScreenFrame(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.rect = (0, 0, 500, 500)


class Sprite(pygame.sprite.Sprite):
    def __init__(self, group):
        super().__init__(group)
        self.rect = None

    def get_event(self, event):
        pass


class Tile(Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(sprite_group)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)

class Bullet(Sprite):
    def __init__(self, pos_x, pos_y):
        self.damage = 100
        self.speed = 5
        super().__init__(hero_group)
        self.rect = self.image.get_rect().move(
            pos_x, pos_y)
        self.bullet_pos = (pos_x, pos_y)


class Tank(Sprite):
    def __init__(self, pos_x, pos_y):
        self.health = 100
        self.speed = 2
        self.tankx = 144
        self.tanky = 400
        super().__init__(hero_group)
        self.image = player_image
        self.rect = self.image.get_rect().move(
            self.tankx, self.tanky)
        self.pos = (pos_x, pos_y)
        self.post = (self.tankx, self.tanky)

    def move(self, x, y):
        global diratoin
        self.pos = (x, y)
        if side == 'up' and diratoin == 2:
            self.image = pygame.transform.rotate(self.image, 180)
            diratoin = 1
        elif side == 'up' and diratoin == 4:
            self.image = pygame.transform.rotate(self.image, 90)
            diratoin = 1
        elif side == 'up' and diratoin == 3:
            self.image = pygame.transform.rotate(self.image, 270)
            diratoin = 1
        elif side == 'down' and diratoin == 1:
            self.image = pygame.transform.rotate(self.image, 180)
            diratoin = 2
        elif side == 'down' and diratoin == 4:
            self.image = pygame.transform.rotate(self.image, 270)
            diratoin = 2
        elif side == 'down' and diratoin == 3:
            self.image = pygame.transform.rotate(self.image, 90)
            diratoin = 2
        elif side == 'right' and diratoin == 1:
            self.image = pygame.transform.rotate(self.image, 270)
            diratoin = 4
        elif side == 'right' and diratoin == 2:
            self.image = pygame.transform.rotate(self.image, 90)
            diratoin = 4
        elif side == 'right' and diratoin == 3:
            self.image = pygame.transform.rotate(self.image, 180)
            diratoin = 4
        elif side == 'left' and diratoin == 1:
            self.image = pygame.transform.rotate(self.image, 90)
            diratoin = 3
        elif side == 'left' and diratoin == 2:
            self.image = pygame.transform.rotate(self.image, 270)
            diratoin = 3
        elif side == 'left' and diratoin == 4:
            self.image = pygame.transform.rotate(self.image, 180)
            diratoin = 3
        elif side == 'up' and diratoin != 1:
            self.image = self.image
            diratoin = 1
        elif side == "down" and diratoin != 2:
            self.image = pygame.transform.rotate(self.image, 180)
            diratoin = 2
        elif side == "left" and diratoin != 3:
            self.image = pygame.transform.rotate(self.image, 90)
            diratoin = 3
        elif side == "right" and diratoin != 4:
            self.image = pygame.transform.rotate(self.image, 270)
            diratoin = 4
        self.rect = self.image.get_rect().move(
            tile_width * self.pos[0], tile_height * self.pos[1])


def load_level(filename):
    filename = "data/" + filename
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]
    max_width = max(map(len, level_map))
    return list(map(lambda x: x.ljust(max_width, '*'), level_map))


def generate_level(level):
    new_player, x, y = None, None, None
    xcord = 9
    ycord = 25
    new_player = Tank(xcord, ycord)
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Tile('empty', x, y)
            elif level[y][x] == '#':
                Tile('brick', x, y)
            elif level[y][x] == '@':
                Tile('steel', x, y)
            elif level[y][x] == '%':
                Tile('grass', x, y)
    return new_player, x, y
#144
#400

side = ''


def move(hero, movement):
    x, y = hero.pos
    xt, yt = hero.post
    global max_x, max_y
    if movement == "up":
        if y > 0 and (level_map[y - 1][x] == "." and level_map[y - 1][x + 1] == ".") or (
                level_map[y - 1][x] == "%" and level_map[y - 1][x + 1] == "%"):
            hero.move(x, y - 1)
    elif movement == "down":
        if y < max_y - 1 and (level_map[y + 2][x] == "." and level_map[y + 2][x + 1] == ".") or (
                level_map[y + 2][x] == "%" and level_map[y + 2][x + 1] == "%"):
            hero.move(x, y + 1)
    elif movement == "left":
        if x > 0 and (level_map[y][x - 1] == "." and level_map[y + 1][x - 1] == ".") or (
                level_map[y][x - 1] == "%" and level_map[y + 1][x - 1] == "%"):
            hero.move(x - 1, y)
    elif movement == "right":
        if x < max_x - 1 and (level_map[y][x + 2] == "." and level_map[y + 1][x + 2] == ".") or (
                level_map[y][x + 2] == "%" and level_map[y + 1][x + 2] == "%"):
            hero.move(x + 1, y)


# player_image = load_image('tank.png')
level_map = load_level("map1.txt")
hero, max_x, max_y = generate_level(load_level('map1.txt'))
running = True
diratoin = 0
while running:
    movement = True
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                side = 'up'
                move(hero, "up")
            elif event.key == pygame.K_DOWN:
                side = 'down'
                move(hero, "down")
            elif event.key == pygame.K_LEFT:
                side = 'left'
                move(hero, "left")
            elif event.key == pygame.K_RIGHT:
                side = 'right'
                move(hero, "right")

    screen.fill(pygame.Color(0, 0, 0))
    sprite_group.draw(screen)
    hero_group.draw(screen)

    pygame.display.flip()

# screen.fill(pygame.Color(0, 0, 0))
# tiles_group.draw(screen)
# player_group.draw(screen)
