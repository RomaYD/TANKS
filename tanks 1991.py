import pygame
import os
import sys


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
screen_size = (1000, 850)
screen = pygame.display.set_mode(screen_size)
FPS = 50

tile_images = {
    'brick': load_image('brick.png'),
    'steel': load_image('steel.png'),
    'empty': load_image('empty.png'),
    'grass': load_image('grass.png')
}
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


def load_level(filename):
    filename = "data/" + filename
    # читаем уровень, убирая символы перевода строки
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]
    # и подсчитываем максимальную длину
    max_width = max(map(len, level_map))
    # дополняем каждую строку пустыми клетками ('.')
    return list(map(lambda x: x.ljust(max_width, '*'), level_map))


def generate_level(level):
    new_player, x, y = None, None, None
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


# player_image = load_image('tank.png')
#level_map = load_level("map1.txt")
hero, max_x, max_y = generate_level(load_level('map1.txt'))
running = True
while running:
    for event in pygame.event.get():
        if event == pygame.QUIT:
            running = False
    screen.fill(pygame.Color(0, 0, 0))
    sprite_group.draw(screen)
    pygame.display.flip()

# screen.fill(pygame.Color(0, 0, 0))
# tiles_group.draw(screen)
# player_group.draw(screen)
