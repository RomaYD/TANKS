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
screen_size = (1000, 800)
screen = pygame.display.set_mode(screen_size)
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


class Tank(Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(hero_group)
        self.image = player_image
        self.rect = self.image.get_rect().move(
            tile_width * pos_x + 15, tile_height * pos_y + 5)
        self.pos = (pos_x, pos_y)

    def move(self, x, y):
        self.pos = (x, y)
        self.rect = self.image.get_rect().move(
            tile_width * self.pos[0], tile_height * self.pos[1])


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
    xcord = 9
    ycord = 26
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

side = ''

def move(hero, movement):
    x, y = hero.pos
    if movement == "up":
        side = 'up'
        if y > 0 and (level_map[y - 1][x] == "." and level_map[y - 1][x + 1] == ".") or (level_map[y - 1][x] == "%" and level_map[y - 1][x + 1] == "%"):
            hero.move(x, y - 1)
    #      hit.play()
    elif movement == "down":
        side =  'down'
        if y < max_y - 1 and (level_map[y + 2][x] == "." and level_map[y + 2][x + 1] == ".") or (level_map[y + 2][x] == "%" and level_map[y + 2][x + 1] == "%"):
            hero.move(x, y + 1)
    #        hit.play()
    elif movement == "left":
        side = 'left'
        if x > 0 and (level_map[y][x - 1] == "." and level_map[y + 1][x - 1] == ".") or (level_map[y][x - 1] == "%" and level_map[y + 1][x - 1] == "%"):
            hero.move(x - 1, y)

    #       hit.play()
    elif movement == "right":
        side = 'right'
        if x < max_x - 1 and (level_map[y][x + 2] == "." and level_map[y + 1][x + 2] == ".") or (level_map[y][x + 2] == "%" and level_map[y + 1][x + 2] == "%"):
            hero.move(x + 1, y)


# player_image = load_image('tank.png')
level_map = load_level("map1.txt")
hero, max_x, max_y = generate_level(load_level('map1.txt'))
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                move(hero, "up")
            elif event.key == pygame.K_DOWN:
                move(hero, "down")
            elif event.key == pygame.K_LEFT:
                move(hero, "left")
            elif event.key == pygame.K_RIGHT:
                move(hero, "right")

    screen.fill(pygame.Color(0, 0, 0))
    sprite_group.draw(screen)
    hero_group.draw(screen)

    pygame.display.flip()

# screen.fill(pygame.Color(0, 0, 0))
# tiles_group.draw(screen)
# player_group.draw(screen)

import os, pygame, time, random, uuid, sys

class Game():
    # Флаги направления движения
    (DIR_UP, DIR_RIGHT, DIR_DOWN, DIR_LEFT) = range(4)

    TILE_SIZE = 16

    def __init__(self):

        global screen, sprites, play_sounds, sounds

        pygame.init()

        # центрирование камеры
        os.environ['SDL_VIDEO_WINDOW_POS'] = 'center'

        if play_sounds:
            pygame.mixer.pre_init(44100, -16, 1, 512)

        pygame.display.set_caption("Battle City")

        size = width, height = 480, 416

        if "-f" in sys.argv[1:]:
            screen = pygame.display.set_mode(size, pygame.FULLSCREEN)
        else:
            screen = pygame.display.set_mode(size)

        self.clock = pygame.time.Clock()

        # загрузка спрайтов версия funk
        sprites = pygame.transform.scale2x(pygame.image.load("images/sprites.gif"))
        screen.set_colorkey((0,138,104))

        # загрузка спрайтов версия pixel
        # sprites = pygame.transform.scale(pygame.image.load("images/sprites.gif"), [192, 224])

        pygame.display.set_icon(sprites.subsurface(0, 0, 13 * 2, 13 * 2))

        # Загрузка звуков
        if play_sounds:
            pygame.mixer.init(44100, -16, 1, 512)

            sounds["start"] = pygame.mixer.Sound("sounds/gamestart.ogg")
            sounds["end"] = pygame.mixer.Sound("sounds/gameover.ogg")
            sounds["score"] = pygame.mixer.Sound("sounds/score.ogg")
            sounds["fire"] = pygame.mixer.Sound("sounds/fire.ogg")
            sounds["explosion"] = pygame.mixer.Sound("sounds/explosion.ogg")
            sounds["brick"] = pygame.mixer.Sound("sounds/brick.ogg")
            sounds["steel"] = pygame.mixer.Sound("sounds/steel.ogg")

        self.enemy_life_image = sprites.subsurface(81 * 2, 57 * 2, 7 * 2, 7 * 2)
        self.player_life_image = sprites.subsurface(89 * 2, 56 * 2, 7 * 2, 8 * 2)
        self.flag_image = sprites.subsurface(64 * 2, 49 * 2, 16 * 2, 15 * 2)

        # Интро
        self.player_image = pygame.transform.rotate(sprites.subsurface(0, 0, 13 * 2, 13 * 2), 270)

        # Враги не появляются пока True
        self.timefreeze = False

        # загрузка шрифта
        self.font = pygame.font.Font("fonts/prstart.ttf", 16)

        # предварительная обработка "GAME OVER"
        self.im_go = pygame.Surface((64, 40))
        self.im_go.set_colorkey((0, 0, 0))
        self.im_go.blit(self.font.render("GAME", False, (127, 64, 64)), [0, 0])
        self.im_go.blit(self.font.render("OVER", False, (127, 64, 64)), [0, 20])

        self.num_players = 1
        del players[:]
        del bullets[:]
        del enemies[:]
        del bonuses[:]


    def shieldPlayer(self, player, shield=True, duration=None):
        # Добавить\убрать щит
        # Для игрока

        player.shielded = shield
        if shield:
            player.timer_uuid_shield = gtimer.add(100, lambda: player.toggleShieldImage())
        else:
            gtimer.destroy(player.timer_uuid_shield)

        if shield and duration != None:
            gtimer.add(duration, lambda: self.shieldPlayer(player, False), 1)

    def spawnEnemy(self):
        # Появление врагов если:
        # -хотя бы 1 в очереди
        # -не превышает максимальное число для карты
        # -timefreeze != True

        global enemies

        if len(enemies) >= self.level.max_active_enemies:
            return
        if len(self.level.enemies_left) < 1 or self.timefreeze:
            return
        enemy = Enemy(self.level, 1)

        enemies.append(enemy)

    def respawnPlayer(self, player, clear_scores=False):
        player.reset()

        if clear_scores:
            player.trophies = {
                "enemy0": 0, "enemy1": 0, "enemy2": 0, "enemy3": 0
            }

        self.shieldPlayer(player, True, 4000)

    def gameOver(self):
        # Анимация "GAME OVER" и переход в меню

        global play_sounds, sounds

        print("Game Over")
        if play_sounds:
            for sound in sounds:
                sounds[sound].stop()
            sounds["end"].play()

        self.game_over_y = 416 + 40

        self.game_over = True
        gtimer.add(3000, lambda: self.showScores(), 1)

    def gameOverScreen(self):
        # Показывает картинку "GAME OVER"

        global screen

        # Остановка главного цикла
        self.running = False
        screen.fill([0, 0, 0])

        self.writeInBricks("game", [125, 140])
        self.writeInBricks("over", [125, 220])
        pygame.display.flip()

        while 1:
            time_passed = self.clock.tick(50)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                        self.showMenu()
                        return

    def showMenu(self):
        # Показывает меню
        # Картинка меняется если нажаты кнопки UP или DOWN
        # При нажатии ENTER запускается игра с выбраным колисеством игроков

        global players, screen

        self.running = False

        # Очистка таймеров
        del gtimer.timers[:]

        # Выбор начальной карты
        self.stage = 1

        self.animateIntroScreen()

        main_loop = True
        while main_loop:
            time_passed = self.clock.tick(50)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        quit()
                    elif event.key == pygame.K_UP:
                        if self.num_of_players == 2:
                            self.num_of_players = 1
                            self.drawIntroScreen()
                    elif event.key == pygame.K_DOWN:
                        if self.num_of_players == 1:
                            self.num_of_players = 2
                            self.drawIntroScreen()
                    elif event.key == pygame.K_RETURN:
                        main_loop = False

        del players[:]
        self.nextLevel()

    def reloadPlayers(self):
        # Инициализация игроков
        # Если игроки уже существуют, то перезагрузить их

        global players

        if len(players) == 0:
            # Игрок 1
            x = 8 * self.TILE_SIZE + (self.TILE_SIZE * 2 - 26) / 2
            y = 24 * self.TILE_SIZE + (self.TILE_SIZE * 2 - 26) / 2

            player = Player(
                self.level, 0, [x, y], self.DIR_UP, (0, 0, 13 * 2, 13 * 2)
            )
            players.append(player)

            # Игрок 2, если существует
            if self.num_of_players == 2:
                x = 16 * self.TILE_SIZE + (self.TILE_SIZE * 2 - 26) / 2
                y = 24 * self.TILE_SIZE + (self.TILE_SIZE * 2 - 26) / 2
                player = Player(
                    self.level, 0, [x, y], self.DIR_UP, (16 * 2, 0, 13 * 2, 13 * 2)
                )
                player.controls = [102, 119, 100, 115, 98]
                players.append(player)

        for player in players:
            player.level = self.level
            self.respawnPlayer(player, True)


    def draw(self):
        global screen, castle, players, enemies, bullets, bonuses

        screen.fill([0, 0, 0])

        self.level.draw([self.level.TILE_EMPTY, self.level.TILE_BRICK, self.level.TILE_STEEL, self.level.TILE_FROZE,
                         self.level.TILE_WATER])

        castle.draw()

        for enemy in enemies:
            enemy.draw()

        for label in labels:
            label.draw()

        for player in players:
            player.draw()

        for bullet in bullets:
            bullet.draw()

        self.level.draw([self.level.TILE_GRASS])

        if self.game_over:
            if self.game_over_y > 188:
                self.game_over_y -= 4
            screen.blit(self.im_game_over, [176, self.game_over_y])

        # self.drawSidebar()

        pygame.display.flip()
