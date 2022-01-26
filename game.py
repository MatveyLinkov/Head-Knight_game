import os
import random
import sys

import pygame
import pytmx


pygame.init()
pygame.mixer.music.load('music/intro.mp3')
pygame.mixer.music.play()
start_size = start_width, start_height = 1920, 1080
startscreen = pygame.display.set_mode(start_size)
map_number = '1'
maps = {'map1.tmx': [23, (11, 8)], 'map2.tmx': [24, (10, 7)],
        'map3.tmx': [23, (12, 5)]}
level = 'map' + map_number + '.tmx'
size = width, height = 1980, 1080
FPS = 60
start_success = False
clock = pygame.time.Clock()
MAPS_DIR = 'levels'
final = False
all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
walls_group = pygame.sprite.Group()
barriers_group = pygame.sprite.Group()
empty_group = pygame.sprite.Group()
bombs_group = pygame.sprite.Group()
doors_group = pygame.sprite.Group()
animated_sprites_group = pygame.sprite.Group()
particle_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
shot_group = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()
skulls_group = pygame.sprite.Group()
destroyer_group = pygame.sprite.Group()
scripts_group = pygame.sprite.Group()
rooms_group = pygame.sprite.Group()
chest_group = pygame.sprite.Group()
key_group = pygame.sprite.Group()
hatch_group = pygame.sprite.Group()
ladder_group = pygame.sprite.Group()
melee_group = pygame.sprite.Group()
health_group = pygame.sprite.Group()
slimes_group = pygame.sprite.Group()
tables_group = pygame.sprite.Group()
spikes_group = pygame.sprite.Group()
mini_player_group = pygame.sprite.Group()
mini_keys_group = pygame.sprite.Group()
mini_doors_group = pygame.sprite.Group()
all_cells_group = pygame.sprite.Group()
weapon_group = pygame.sprite.Group()


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f'Файл с изображением "{fullname}" отсутствует')
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is None:
        image = image.convert_alpha()
    else:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    return image


floor = [6, 15, 21, 22, 23, 24, 30, 31, 32, 33]
completed_levels = []
player_sheet = pygame.transform.scale(load_image('knight_sheet.png'), (552, 150))
skull_sheet = load_image('skull_sheet.png')
goblin_sheet = load_image('goblin_spritesheet.png')
bomber_sheet = pygame.transform.scale(load_image('bomber_spritesheet.png'), (288, 48))
cell_image = pygame.transform.scale(load_image('inventory_cell.png'), (50, 50))
choose_cell = pygame.transform.scale(load_image('active_cell.png'), (50, 50))
key_inventory = pygame.transform.scale(load_image('key_inv.png'), (20, 38))
opened_chest = load_image('chest_open_anim_3.png')
closed_chest = load_image('chest_open_anim_1.png')
key_image = load_image('key.png')
arrow_image = pygame.transform.scale(load_image('arrow.png'), (48, 48))
bomb_sheet = load_image('bomb_sheet.png')
hit_effect_sheet = pygame.transform.scale(load_image('hit_effect.png'), (96, 32))
explosion_sheet = pygame.transform.scale(load_image('explosion_sheet.png'), (336, 48))
enemy_dead_sheet = load_image('enemy_afterdead.png')
game_over = pygame.transform.scale(load_image('game_over.png'), (750, 375))
player_dead = pygame.transform.scale(load_image('knight_dead.png'), (138, 102))
animated_slimes = pygame.transform.scale(load_image('slime_animated.png'), (1728, 576))
mini_player_sheet = pygame.transform.scale(load_image('knight_sheet.png'), (448, 112))
slime_sheet = load_image('slime_idle_spritesheet.png')
spikes_images = ['holes.png', 'spikes.png', 'on_holes.png', 'on_spikes.png']
walls = []
doors = [37, 38, 39, 40, 47, 48, 49, 50, 57, 58, 59, 60, 67, 68]
barriers = [44, 45, 53, 54]
animated_sprites = {75: 'flag_sheet.png',
                    91: 'torch_sheet.png', 94: 'candle_sheet.png'}
weapons_image = {'wooden_bow': load_image('wooden_bow.png'),
                 'iron_sword':
                     pygame.transform.scale(load_image('iron_sword.png'), (20, 42))}
weapons = ['wooden_bow', 'iron_sword']
bows = ['wooden_bow']
swords = ['iron_sword']
splash_effect = load_image('slash_effect_anim.png')
inventory = {1: 'wooden_bow', 2: None, 3: None}
current_weapon = inventory[1]
ts = tile_width = tile_height = 48
chest = 84
key = 89
player = None


def terminate():
    pygame.quit()
    sys.exit()


def getting_weapon():
    global current_weapon, inventory
    new_weapon = random.choice(weapons[1:])
    inventory[2] = new_weapon
    WeaponInInventory(weapons_image[new_weapon], 1)


def choose_weapon(button):
    global current_weapon
    if button == 1:
        current_weapon = inventory[1]
        Inventory(0, True)
    elif button == 2:
        Inventory(1, True)
        if len(inventory) >= 2:
            current_weapon = inventory[2]


def pickup_key():
    pass


def show_text(text, font, position):  # преобразование текста
    font_color = pygame.Color("orange")
    text = font.render(text, 1, font_color)  # передаём строку для экрана, затем сглаживание, цвет
    startscreen.blit(text, position)


def start_screen():  # начальный экран
    text = ['Dungeon quest', 'play', 'exit']
    fon = pygame.transform.scale(load_image("start_fon.png"), (1920, 1080))
    startscreen.blit(fon, (0, 0))
    coord_x = [500, 830, 850]
    coord_y = [280, 680, 800]
    fonts_size = [150, 100, 100]
    for elem in range(len(text)):
        font = [pygame.font.Font("fonts/Dirtchunk.otf", fonts_size[elem]),
                pygame.font.Font("fonts/jelani.otf", fonts_size[elem]),
                pygame.font.Font("fonts/jelani.otf", fonts_size[elem])]
        show_text(text[elem], font[elem], (coord_x[elem], coord_y[elem]))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.MOUSEBUTTONDOWN:
                print(event.pos)
                if 830 <= event.pos[0] <= 1020 and 680 <= event.pos[1] <= 805:
                    return screen_with_levels()
                if 850 <= event.pos[0] <= 1040 and 840 <= event.pos[1] <= 905:
                    terminate()
        pygame.display.flip()
        clock.tick(50)


def screen_with_levels():
    global map_number, start_success
    startscreen.fill(pygame.Color("black"))
    fon = pygame.transform.scale(load_image("fon_lvl.png"), (1920, 1080))
    startscreen.blit(fon, (0, 0))
    images = ['fon1.png', 'analog_fon.png', 'dop_fon.png', 'fon3.png', 'fon2.png']
    for name in range(len(images)):
        img = pygame.transform.scale(load_image(images[name]), (200, 200))
        startscreen.blit(img, (40 + 210 * name, 25))
    text_level = ['1', '2', '3', '4', '5']
    for elem in range(len(text_level)):
        font = pygame.font.Font("fonts/DS VTCorona Cyr.ttf", 90)
        show_text(text_level[elem], font, (50 + 210 * elem, 30))
    font = pygame.font.Font("fonts/jelani.otf", 90)
    show_text('back', font, (15, 950))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if 3 <= event.pos[0] <= 128 and 538 <= event.pos[1] <= 597:
                    home = True
                    start_screen()
                    return home
                if 40 <= event.pos[0] <= 240 and 25 <= event.pos[1] <= 225:
                    map_number = '1'
                    return
                if 280 <= event.pos[0] <= 480 and 25 <= event.pos[1] <= 225:
                    map_number = '2'
                    return
                if 520 <= event.pos[0] <= 720 and 25 <= event.pos[1] <= 225:
                    map_number = '3'
                    return
                if 760 <= event.pos[0] <= 960 and 25 <= event.pos[1] <= 225:
                    pass
                if 1000 <= event.pos[0] <= 1300 and 25 <= event.pos[1] <= 225:
                    pass
        pygame.display.flip()
        clock.tick(50)


class FinalScreen(pygame.sprite.Sprite):
    def __init__(self, columns, rows, pos_x, pos_y, image, flip=False):
        super().__init__(animated_sprites_group, all_sprites)
        self.frames = []
        self.crop_sheet(image, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(pos_x, pos_y)
        self.flip = flip

    def crop_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for i in range(rows):
            for j in range(columns):
                frame_coord = (self.rect.w * j, self.rect.h * i)
                [self.frames.append(sheet.subsurface(pygame.Rect(frame_coord, self.rect.size)))
                 for i in range(6)]

    def update(self):
        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        self.image = self.frames[self.cur_frame]
        self.image = pygame.transform.flip(self.image, self.flip, False)


class Dungeon:
    def __init__(self, filename):
        super().__init__()
        self.map = pytmx.load_pygame(f'{MAPS_DIR}/{filename}')
        self.height = self.map.height
        self.width = self.map.width
        self.tile_size = self.map.tilewidth
        for obj in self.map.objects:
            if obj.type == 'player':
                self.player_x, self.player_y = obj.x // ts, obj.y // ts
            elif obj.type == 'room' and obj.name not in completed_levels:
                Room(obj.name, obj.x, obj.y, obj.width, obj.height)
            elif obj.name == 'Skull':
                Skull(4, 1, obj.x // ts, obj.y // ts, )
            elif obj.name == 'Goblin':
                Goblin(6, 2, obj.x // ts, obj.y // ts, )
            elif obj.name == 'Bomber':
                Bomber(6, 1, obj.x // ts, obj.y // ts, )
            elif obj.type == 'script':
                Script(obj.x, obj.y, obj.width, obj.height)

    def render(self):
        for i in range(4):
            for y in range(self.height):
                for x in range(self.width):
                    image = self.map.get_tile_image(x, y, i)
                    if image:
                        if i == 1 and self.get_tile_id((x, y), i) not in walls:
                            walls.append(self.get_tile_id((x, y), i))
                        if self.get_tile_id((x, y), i) in doors:
                            Door(x, y, image)
                        elif i == 3:
                            Barrier(self.get_tile_id((x, y), i), x, y, image)
                        elif self.get_tile_id((x, y), i) in animated_sprites:
                            AnimatedSprite(self.get_tile_id((x, y), i), 4, 1, x, y)
                        elif self.get_tile_id((x, y), i) - 100 in animated_sprites:
                            AnimatedSprite(self.get_tile_id((x, y), i) - 100, 4, 1, x, y)
                        elif self.get_tile_id((x, y), i) - 100 == chest or \
                                self.get_tile_id((x, y), i) == chest:
                            Chest(x, y)
                        elif self.get_tile_id((x, y), i) == key or \
                                self.get_tile_id((x, y), i) - 100 == key:
                            Key(x, y)
                        elif self.get_tile_id((x, y), i) == 81 or \
                                self.get_tile_id((x, y), i) - 100 == 81:
                            Hatch(x, y, image)
                        elif self.get_tile_id((x, y), i) == 82 or \
                                self.get_tile_id((x, y), i) - 100 == 82:
                            Ladder(x, y, image)
                        else:
                            Tile(self.get_tile_id((x, y), i), x, y, image)

        return self.player_x, self.player_y

    def get_tile_id(self, position, layer):
        return self.map.tiledgidmap[self.map.get_tile_gid(*position, layer)]


class Castle:
    def __init__(self, filename):
        super().__init__()
        self.map = pytmx.load_pygame(f'{MAPS_DIR}/{filename}')
        self.height = self.map.height
        self.width = self.map.width
        self.tile_size = self.map.tilewidth
        for obj in self.map.objects:
            if obj.name == 'Player':
                self.player_x, self.player_y = obj.x // tile_width, obj.y // tile_height
            elif obj.name == 'Slime':
                Slime(6, 1, obj.x // tile_width, obj.y // tile_height)
            elif obj.name == 'Spike':
                Spikes(obj.x // tile_width, obj.y // tile_height)

    def render(self):
        for i in range(4):
            for y in range(self.height):
                for x in range(self.width):
                    image = self.map.get_tile_image(x, y, i)
                    if image:
                        if i == 3:
                            Table(x, y, image)
                        elif self.get_tile_id((x, y), i) == 6:
                            MiniKey(x, y, image)
                        elif self.get_tile_id((x, y), i) == 37:
                            MiniDoor(x, y, image)
                        else:
                            Tile(self.get_tile_id((x, y), i), x, y, image)
        return self.player_x, self.player_y

    def get_tile_id(self, position, layer):
        try:
            return self.map.tiledgidmap[self.map.get_tile_gid(*position, layer)]
        except KeyError:
            pass


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_id, pos_x, pos_y, image):
        super().__init__(tiles_group, all_sprites)
        if tile_id in walls:
            self.add(walls_group)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(tile_width * pos_x, tile_height * pos_y)


class Barrier(pygame.sprite.Sprite):
    def __init__(self, id,  pos_x, pos_y, image):
        super().__init__(barriers_group, all_sprites)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(tile_width * pos_x, tile_height * pos_y)
        if id == 79 or id - 100 == 79:
            self.add(empty_group)

    def update(self):
        if pygame.sprite.spritecollideany(self, destroyer_group):
            if [(destroyer.update(True), Particle(7, 1, self.rect.x, self.rect.y,
                explosion_sheet, destroyer)) for destroyer in destroyer_group
                    if pygame.sprite.collide_mask(self, destroyer)]:
                self.kill()
        elif pygame.sprite.spritecollideany(self, bombs_group) and self not in empty_group:
            bombs_group.update(True)
            self.kill()


class Key(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(key_group, all_sprites)
        self.image = key_image
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(tile_width * pos_x, tile_height * pos_y)

    def update(self):
        if pygame.sprite.spritecollideany(self, player_group):
            inventory[3] = 'key'
            WeaponInInventory(key_inventory, 2)
            self.kill()


class AnimatedSprite(pygame.sprite.Sprite):
    def __init__(self, id, columns, rows, pos_x, pos_y):
        super().__init__(animated_sprites_group, all_sprites)
        self.frames = []
        self.crop_sheet(load_image(animated_sprites[id]), columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(tile_width * pos_x, tile_height * pos_y)

    def crop_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for i in range(rows):
            for j in range(columns):
                frame_coord = (self.rect.w * j, self.rect.h * i)
                [self.frames.append(sheet.subsurface(pygame.Rect(frame_coord, self.rect.size)))
                 for i in range(8)]

    def update(self):
        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        self.image = self.frames[self.cur_frame]


class Particle(pygame.sprite.Sprite):
    def __init__(self, columns, rows, pos_x, pos_y, image, enemy=None):
        super().__init__(particle_group, all_sprites)
        self.frames = []
        self.sheet = image
        self.enemy = enemy
        self.crop_sheet(image, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(pos_x, pos_y)

    def crop_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for i in range(rows):
            for j in range(columns):
                frame_coord = (self.rect.w * j, self.rect.h * i)
                [self.frames.append(sheet.subsurface(pygame.Rect(frame_coord, self.rect.size)))
                 for i in range(8)]

    def update(self, enemy=None):
        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        self.image = self.frames[self.cur_frame]
        if self.cur_frame == len(self.frames) - 1:
            self.kill()
        if self.cur_frame == len(self.frames) // 2:
            if self.sheet == explosion_sheet:
                if self.enemy:
                    self.enemy.update(True)


class Door(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, image):
        super().__init__(doors_group, walls_group, all_sprites)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(tile_width * pos_x, tile_height * pos_y)

    def update(self, close):
        if not close:
            self.remove(walls_group)
        else:
            self.add(walls_group)


class Room(pygame.sprite.Sprite):
    def __init__(self, name, pos_x, pos_y, width, height):
        super().__init__(rooms_group, all_sprites)
        self.name = name
        self.image = pygame.Surface((width, height))
        self.rect = pygame.Rect(pos_x, pos_y, width, height)
        self.fight = False

    def update(self):
        global doors_close
        if pygame.sprite.spritecollideany(self, player_group):
            if not pygame.sprite.spritecollideany(self, enemy_group):
                doors_close = False
                self.kill()
                completed_levels.append(self.name)
            if not self.fight and doors_close:
                [enemy.update(True) for enemy in enemy_group if
                 pygame.sprite.collide_mask(self, enemy)]
                self.fight = True
                for script in scripts_group:
                    if pygame.sprite.collide_mask(self, script):
                        script.update(self.fight)


class Hatch(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, image):
        super().__init__(hatch_group, all_sprites)
        self.image = image
        self.count = 0
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(tile_width * pos_x, tile_height * pos_y)

    def update(self, button, key_available):
        global dungeon_map, change_mode
        if button == 'e' and key_available is True and not change_mode:
            if pygame.sprite.spritecollideany(self, player_group):
                self.count += 1
                [s.kill() for s in all_sprites]
                dungeon_map = False
                change_mode = True
                inventory[3] = None


class Ladder(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, image):
        super().__init__(ladder_group, all_sprites)
        self.image = image
        self.count = 0
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(tile_width * pos_x, tile_height * pos_y)

    def update(self, button):
        global map_number, restart, transit
        if button == 'e':
            if pygame.sprite.spritecollideany(self, player_group) and self.count == 0:
                self.count += 1
                map_number = str(int(map_number) + 1)
                restart = True
                transit = True


class Melee(pygame.sprite.Sprite):
    def __init__(self, x, y, weapon, angle):
        super().__init__(melee_group)
        self.frames = []
        self.crop_sheet(splash_effect, 3, 1)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.angle = angle
        self.weapon = weapon
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x - 15, y - 10
        if angle == 270:
            self.rect = self.rect.move(-6, 9)
        elif angle == 180:
            self.rect = self.rect.move(-18, -6)
        elif angle == 90:
            self.rect = self.rect.move(-6, -30)
        elif angle == 0:
            self.rect = self.rect.move(12, -6)

    def crop_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for i in range(rows):
            for j in range(columns):
                frame_coord = (self.rect.w * j, self.rect.h * i)
                [self.frames.append(sheet.subsurface(pygame.Rect(frame_coord, self.rect.size)))
                 for i in range(6)]

    def update(self):
        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        self.image = self.frames[self.cur_frame]
        self.image = pygame.transform.rotate(self.image, self.angle)
        if self.cur_frame == len(self.frames) - 1:
            self.kill()


class Script(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, width, height):
        super().__init__(scripts_group, all_sprites)
        self.image = pygame.Surface((240, 240))
        self.rect = pygame.Rect(pos_x, pos_y, width, height)

    def update(self, fight=False):
        global doors_close
        if pygame.sprite.spritecollideany(self, player_group) or fight:
            doors_close = True
            self.kill()
        elif not pygame.sprite.spritecollideany(self, rooms_group):
            self.kill()


class Player(pygame.sprite.Sprite):
    def __init__(self, columns, rows, pos_x, pos_y, change):
        super().__init__(player_group, all_sprites)
        self.frames = []
        self.half_frames = 24
        self.crop_sheet(player_sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.image.get_rect()
        if not final:
            self.rect = self.rect.move(tile_width * pos_x + 12, tile_height * pos_y + 12)
            if change:
                for hatch in hatch_group:
                    self.rect.x, self.rect.y = hatch.rect.x - 12, hatch.rect.y - 12
        else:
            self.rect = self.rect.move(600, 350)
        self.damage = False
        self.visible = True
        self.time = 0

    def crop_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for i in range(rows):
            for j in range(columns):
                frame_coord = (self.rect.w * j, self.rect.h * i)
                [self.frames.append(sheet.subsurface(pygame.Rect(frame_coord, self.rect.size)))
                 for i in range(3)]

    def update(self, x, y, flip=False):
        if moving:
            self.cur_frame = (self.cur_frame + 1) % len(self.frames[self.half_frames:])
            self.image = self.frames[self.half_frames:][self.cur_frame]
        else:
            self.cur_frame = (self.cur_frame + 1) % len(self.frames[:self.half_frames])
            self.image = self.frames[:self.half_frames][self.cur_frame]
        self.image = pygame.transform.flip(self.image, flip, False)
        if pygame.sprite.spritecollideany(self, walls_group) or\
                pygame.sprite.spritecollideany(self, barriers_group):
            self.rect.x -= x
            self.rect.y -= y
        if pygame.sprite.spritecollideany(self, enemy_group):
            return True
        elif pygame.sprite.spritecollideany(self, bombs_group):
            bombs_group.update(True)
            return True


class Chest(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(chest_group, all_sprites)
        self.image = closed_chest
        self.count = 0
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(tile_width * pos_x, tile_height * pos_y + 55)

    def update(self, button):
        if pygame.sprite.spritecollideany(self, player_group):
            if button == 'e':
                self.image = opened_chest
                self.count += 1
                if self.count == 1:
                    getting_weapon()


class Shot(pygame.sprite.Sprite):
    def __init__(self, x, y, vx, vy, angle):
        super().__init__(shot_group, all_sprites)
        self.image = arrow_image
        self.image = pygame.transform.rotate(self.image, angle)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y
        self.vx, self.vy = vx, vy
        if angle == 270:
            self.particle_x, self.particle_y = 0, 3
        elif angle == 180:
            self.particle_x, self.particle_y = 6, 0
        elif angle == 90:
            self.particle_x, self.particle_y = 12, 3
        elif angle == 0:
            self.particle_x, self.particle_y = 6, 12

    def update(self, damage):
        self.rect = self.rect.move(self.vx, self.vy)
        if pygame.sprite.spritecollideany(self, walls_group) or \
                (pygame.sprite.spritecollideany(self, barriers_group) and not
                 pygame.sprite.spritecollideany(self, empty_group)) or \
                ((pygame.sprite.spritecollideany(self, enemy_group) or
                  pygame.sprite.spritecollideany(self, bombs_group)) and damage):
            Particle(3, 1, self.rect.x + self.particle_x, self.rect.y + self.particle_y,
                     hit_effect_sheet)
            self.kill()


class Skull(pygame.sprite.Sprite):
    def __init__(self, columns, rows, pos_x, pos_y):
        super().__init__(enemy_group, skulls_group, all_sprites)
        self.frames = []
        self.crop_sheet(skull_sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(tile_width * pos_x + 12, tile_height * pos_y + 12)
        self.mask = pygame.mask.from_surface(self.image)
        self.hp = 8
        self.damage = 0
        self.melee_strike = True
        self.speed = 7
        self.moving = False
        self.move_x, self.move_y = 0, 0
        self.flip = False
        self.close = False

    def crop_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for i in range(rows):
            for j in range(columns):
                frame_coord = (self.rect.w * j, self.rect.h * i)
                [self.frames.append(sheet.subsurface(pygame.Rect(frame_coord, self.rect.size)))
                 for i in range(8)]

    def update(self, close=False):
        if close:
            self.close = close
        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        self.image = self.frames[self.cur_frame]
        if len([self.rect.x + j for j in range(self.rect.width + 1)
                if self.rect.x + j in
                [player.rect.x + i for i in range(player.rect.width + 1)]]) >= 1\
                and not self.moving and self.close:
            if self.rect.y < player.rect.y:
                self.move_y = self.speed
            else:
                self.move_y = -self.speed
            self.moving = True
        elif len([self.rect.y + j for j in range(self.rect.height + 1)
                  if self.rect.y + j in
                  [player.rect.y + i for i in range(player.rect.height + 1)]]) >= 1 \
                and not self.moving and self.close:
            if self.rect.x < player.rect.x:
                self.move_x = self.speed
                self.flip = False
            else:
                self.move_x = -self.speed
                self.flip = True
            self.moving = True
        if self.flip:
            self.image = pygame.transform.flip(self.image, True, False)
        if not (pygame.sprite.spritecollideany(self, walls_group) or
                pygame.sprite.spritecollideany(self, barriers_group)):
            if self.moving:
                self.rect.x += self.move_x
                self.rect.y += self.move_y
        else:
            self.rect.x -= self.move_x
            self.rect.y -= self.move_y
            self.move_x, self.move_y = 0, 0
            self.moving = False
        if pygame.sprite.spritecollideany(self, shot_group):
            if current_weapon == 'wooden_bow':
                self.damage = 1
                shot_group.update(True)
        if pygame.sprite.spritecollideany(self, melee_group) and self.melee_strike:
            if current_weapon == 'iron_sword':
                self.damage = 4
        self.hp -= self.damage
        self.damage = 0
        if self.hp <= 0 or not pygame.sprite.spritecollideany(self, rooms_group):
            Particle(4, 1, self.rect.x, self.rect.y,
                     pygame.transform.scale(enemy_dead_sheet, (288, 72)))
            self.kill()
        self.melee_strike = False
        if len(melee_group) == 0:
            self.melee_strike = True


class Goblin(pygame.sprite.Sprite):
    def __init__(self, columns, rows, pos_x, pos_y):
        super().__init__(enemy_group, destroyer_group, all_sprites)
        self.frames = []
        self.half_frames = 36
        self.crop_sheet(goblin_sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(tile_width * pos_x, tile_height * pos_y)
        self.hp = 5
        self.damage = 0
        self.melee_strike = True
        self.speed = 3
        self.moving = False
        self.move_x, self.move_y = 0, 0
        self.flip = False
        self.close = False

    def crop_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for i in range(rows):
            for j in range(columns):
                frame_coord = (self.rect.w * j, self.rect.h * i)
                [self.frames.append(sheet.subsurface(pygame.Rect(frame_coord, self.rect.size)))
                 for i in range(6)]

    def update(self, close=False):
        self.move_x, self.move_y = 0, 0
        if close:
            self.close = not self.close
        if (self.rect.x // ts, self.rect.y // ts) != (player.rect.x // ts, player.rect.y // ts) and\
                self.close:
            self.moving = True
        if self.moving:
            self.cur_frame = (self.cur_frame + 1) % len(self.frames[self.half_frames:])
            self.image = self.frames[self.half_frames:][self.cur_frame]
        else:
            self.cur_frame = (self.cur_frame + 1) % len(self.frames[:self.half_frames])
            self.image = self.frames[:self.half_frames][self.cur_frame]
        if self.rect.x // ts < player.rect.x // ts:
            self.move_x = self.speed
            self.flip = False
        elif self.rect.x // ts > player.rect.x // ts:
            self.move_x = -self.speed
            self.flip = True
        if self.rect.y // ts < player.rect.y // ts:
            self.move_y = self.speed
        elif self.rect.y // ts > player.rect.y // ts:
            self.move_y = -self.speed
        if self.flip:
            self.image = pygame.transform.flip(self.image, True, False)
        if not pygame.sprite.spritecollideany(self, walls_group):
            if self.moving:
                self.rect.x += self.move_x
                self.rect.y += self.move_y
        else:
            self.rect.x -= self.move_x
            self.rect.y -= self.move_y
        self.moving = False
        if pygame.sprite.spritecollideany(self, shot_group):
            if current_weapon == 'wooden_bow':
                self.damage = 1
                shot_group.update(True)
        if pygame.sprite.spritecollideany(self, melee_group):
            if current_weapon == 'iron_sword' and self.melee_strike:
                self.damage = 4
        self.hp -= self.damage
        self.damage = 0
        if self.hp <= 0 or not pygame.sprite.spritecollideany(self, rooms_group):
            Particle(4, 1, self.rect.x, self.rect.y, enemy_dead_sheet)
            self.kill()
        self.melee_strike = False
        if len(melee_group) == 0:
            self.melee_strike = True


class Bomber(pygame.sprite.Sprite):
    def __init__(self, columns, rows, pos_x, pos_y):
        super().__init__(enemy_group, destroyer_group, all_sprites)
        self.frames = []
        self.crop_sheet(bomber_sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(tile_width * pos_x, tile_height * pos_y)
        self.hp = 3
        self.damage = 0
        self.move_x, self.move_y = 0, 0
        self.flip = False
        self.close = False
        self.bomb = None
        self.time = 0

    def crop_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for i in range(rows):
            for j in range(columns):
                frame_coord = (self.rect.w * j, self.rect.h * i)
                [self.frames.append(sheet.subsurface(pygame.Rect(frame_coord, self.rect.size)))
                 for i in range(6)]

    def update(self, close=False):
        if close:
            self.close = close
        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        self.image = self.frames[self.cur_frame]
        if len([self.rect.y + j for j in range(self.rect.height + 1)
                if self.rect.y + j in
                   [player.rect.y + i for i in range(player.rect.height + 1)]]) >= 1 and self.close:
            if self.rect.x < player.rect.x:
                if not self.bomb or not self.bomb.alive():
                    self.time += 1
                    if self.time == 25:
                        self.bomb = Bomb(10, 1, self.rect.x, self.rect.y)
                        self.time = 0
        if pygame.sprite.spritecollideany(self, shot_group):
            if current_weapon == 'wooden_bow':
                self.damage = 1
                shot_group.update(True)
        self.hp -= self.damage
        self.damage = 0
        if self.hp <= 0 or not pygame.sprite.spritecollideany(self, rooms_group):
            Particle(4, 1, self.rect.x, self.rect.y, enemy_dead_sheet)
            self.kill()


class Bomb(pygame.sprite.Sprite):
    def __init__(self, columns, rows, pos_x, pos_y):
        super().__init__(bombs_group, all_sprites)
        self.frames = []
        self.crop_sheet(bomb_sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(pos_x + 48, pos_y)
        self.speed = 12

    def crop_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for i in range(rows):
            for j in range(columns):
                frame_coord = (self.rect.w * j, self.rect.h * i)
                [self.frames.append(sheet.subsurface(pygame.Rect(frame_coord, self.rect.size)))
                 for i in range(8)]

    def update(self, damage=False):
        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        self.image = self.frames[self.cur_frame]
        self.rect.x += self.speed
        if pygame.sprite.spritecollideany(self, walls_group) or \
            ((pygame.sprite.spritecollideany(self, barriers_group) and damage) and not
             pygame.sprite.spritecollideany(self, empty_group)) or \
                (pygame.sprite.spritecollideany(self, player_group) and damage) or\
                pygame.sprite.spritecollideany(self, shot_group) or\
                pygame.sprite.spritecollideany(self, melee_group):
            if pygame.sprite.spritecollideany(self, shot_group):
                shot_group.update(True)
            Particle(7, 1, self.rect.x, self.rect.y, explosion_sheet)
            self.kill()


class HealthPoints(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(health_group)
        self.image = load_image('health_ui.png')
        self.rect = self.image.get_rect()


class Inventory(pygame.sprite.Sprite):
    def __init__(self, section, active=False):
        super().__init__(all_cells_group)
        if active:
            self.image = choose_cell
            Inventory((section + 3) % 2)
        else:
            self.image = cell_image
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(1770 + section * tile_width, 0)


class WeaponInInventory(pygame.sprite.Sprite):
    def __init__(self, weapon, section):
        super().__init__(weapon_group)
        self.image = weapon
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(1785 + 50 * section, 5)


class MiniPlayer(pygame.sprite.Sprite):
    def __init__(self, columns, rows, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.pos_x, self.pos_y = pos_x, pos_y
        self.frames = []
        self.half_frames = 24
        self.crop_sheet(mini_player_sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(tile_width * pos_x + 4, tile_height * pos_y + 4)
        self.mask = pygame.mask.from_surface(self.image)
        self.attempt = maps[level][0]
        self.color = 'white'

    def crop_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for i in range(rows):
            for j in range(columns):
                frame_coord = (self.rect.w * j, self.rect.h * i)
                [self.frames.append(sheet.subsurface(pygame.Rect(frame_coord, self.rect.size)))
                 for i in range(3)]

    def update(self, x, y, flip, back=False):
        damage = 0
        self.cur_frame = (self.cur_frame + 1) % len(self.frames[:self.half_frames])
        self.image = self.frames[:self.half_frames][self.cur_frame]
        self.pos_x += x // ts
        self.pos_y += y // ts
        if moving:
            damage += 1
        if flip:
            self.image = pygame.transform.flip(self.image, True, False)
        if not castle.get_tile_id((self.rect.x // 64, self.rect.y // 64), 0) or back:
            self.rect.x -= x
            self.rect.y -= y
            self.pos_x = self.rect.x // ts
            self.pos_y = self.rect.y // ts
            damage -= 1
        if damage == 1:
            self.color = 'white'
        if ((self.pos_x, self.pos_y) in [(s.rect.x // ts, s.rect.y // ts) for s in spikes_group] and
            damage == 1 and not pygame.sprite.spritecollideany(self, tables_group or slimes_group))\
                or (back and (self.pos_x, self.pos_y) in [(s.rect.x // ts, s.rect.y // ts)
                                                          for s in spikes_group]):
            damage += 1
            self.color = 'red'
        self.attempt -= damage
        draw(screen, self.attempt, (self.rect.x // ts, self.rect.y // ts), self.color)


class Slime(pygame.sprite.Sprite):
    def __init__(self, columns, rows, pos_x, pos_y):
        super().__init__(slimes_group, all_sprites)
        self.pos_x, self.pos_y = pos_x, pos_y
        self.frames = []
        self.crop_sheet(slime_sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(tile_width * pos_x + 8, tile_height * pos_y + 8)

    def crop_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for i in range(rows):
            for j in range(columns):
                frame_coord = (self.rect.w * j, self.rect.h * i)
                [self.frames.append(sheet.subsurface(pygame.Rect(frame_coord, self.rect.size)))
                 for i in range(5)]

    def update(self, x, y, flip):
        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        self.image = self.frames[self.cur_frame]
        if (self.pos_x, self.pos_y) == (player.rect.x // ts, player.rect.y // ts):
            self.rect.x += x
            self.rect.y += y
            self.pos_x += x // ts
            self.pos_y += y // ts
            player_group.update(x, y, flip, True)
            if pygame.sprite.spritecollideany(self, tables_group):
                self.kill()
        tile_id = castle.get_tile_id((self.pos_x, self.pos_y), 0)
        if (tile_id not in floor or len([sprite for slime_sprite in slimes_group
                                         if self != slime_sprite and (self.rect.x, self.rect.y) ==
                                        (slime_sprite.rect.x, slime_sprite.rect.y)]) >= 1):
            self.kill()


class Table(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, image):
        super().__init__(tables_group, all_sprites)
        self.pos_x, self.pos_y = pos_x, pos_y
        self.image = image
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(tile_width * pos_x, tile_height * pos_y)

    def update(self, x, y, flip):
        touch = 0
        if (self.rect.x // ts, self.rect.y // ts) == (player.rect.x // ts, player.rect.y // ts):
            self.rect.x += x
            self.rect.y += y
            touch += 1
            player_group.update(x, y, flip, True)
        if (castle.get_tile_id((self.rect.x // ts, self.rect.y // ts), 1) or (
                (self.rect.x // ts, self.rect.y // ts) in
                [(spike_sprite.rect.x // ts, spike_sprite.rect.y // ts)
                 for spike_sprite in tables_group if self != spike_sprite] and touch >= 1) or
                ((self.rect.x // ts, self.rect.y // ts) in
                 [(round(slimes_sprite.rect.x / ts), round(slimes_sprite.rect.y / ts))
                  for slimes_sprite in slimes_group])):
            self.rect.x -= x
            self.rect.y -= y


class Spikes(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(spikes_group, all_sprites)
        self.pos_x, self.pos_y = pos_x, pos_y
        self.image = pygame.transform.scale(load_image(spikes_images[0]), (64, 64))
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(tile_width * pos_x, tile_height * pos_y)

    def update(self):
        self.image = pygame.transform.scale(load_image(spikes_images[1]), (64, 64))
        if (self.pos_x, self.pos_y) in [(s.rect.x // ts, s.rect.y // ts) for s in tables_group] or\
                pygame.sprite.spritecollideany(self, player_group):
            self.image = pygame.transform.scale(load_image(spikes_images[3]), (64, 64))


class MiniKey(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, image):
        super().__init__(mini_keys_group, all_sprites)
        self.pos_x, self.pos_y = pos_x, pos_y
        self.image = image
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(tile_width * pos_x, tile_height * pos_y)

    def update(self):
        if pygame.sprite.spritecollideany(self, player_group):
            self.kill()


class MiniDoor(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, image):
        super().__init__(mini_doors_group, all_sprites)
        self.pos_x, self.pos_y = pos_x, pos_y
        self.image = image
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(tile_width * pos_x, tile_height * pos_y)

    def update(self):
        if len(mini_keys_group.sprites()) == 0:
            self.kill()
        if pygame.sprite.spritecollideany(self, player_group):
            player_group.update(x, y, flip, True)


class Camera:
    def __init__(self):
        self.dx = 0
        self.dy = 0

    def apply(self, obj):
        obj.rect.x += self.dx
        obj.rect.y += self.dy

    def update(self, target):
        self.dx = width // 2 - target.rect.x - target.rect.w // 2
        self.dy = height // 2 - target.rect.y - target.rect.h // 2


def transition():
    screen.fill(pygame.Color(0, 0, 0))


def draw(screen, text, position, color):
    global restart, dungeon_map
    if text == 0:
        text = 'X'
    elif text < 0:
        restart = True
    if position == maps[level][1] and text != -1:
        text = ''
        [s.kill() for s in all_sprites]
        dungeon_map = True
    screen.fill((0, 0, 0))
    font = pygame.font.Font(None, 50)
    text = font.render(str(text), True, color)
    text_x = 10
    text_y = 10
    screen.blit(text, (text_x, text_y))


if __name__ == '__main__':
    pygame.display.set_caption('Dungeon Quest: beta')

    dungeon_map = True
    x, y = 0, 0
    player_v = 6
    shot_v = 16
    hp = 4
    frames = 0
    chest_opened_count = 0
    start_screen()
    screen = pygame.display.set_mode(size)
    camera = Camera()
    clock = pygame.time.Clock()
    button = None
    moving = False
    flip = False
    doors_close = False
    damage = False
    visible = True
    restart = False
    change_mode = False
    transit = False
    transit_time = 0
    running = True
    while running:
        screen.fill(pygame.Color((37, 19, 26)))
        moving = False
        if dungeon_map:
            if len(player_group) == 0:
                if map_number != '4':
                    transit = True
                    ts = tile_width = tile_height = 48
                    dungeon = Dungeon(f'map0{map_number}.tmx')
                    pygame.mouse.set_visible(False)

                    player_x, player_y = dungeon.render()
                    player = Player(8, 2, player_x, player_y, change_mode)
                    x, y = 0, 0
                    player_v = 6
                    heath = HealthPoints()
                    choose_weapon(1)
                    for section in range(0, 3):
                        cell = Inventory(section)
                    cell = Inventory(0, True)
                    WeaponInInventory(weapons_image.get('wooden_bow'), 0)
                    pygame.mixer.music.load('music/dungeon.mp3')
                    pygame.mixer.music.play(-1)
                    pygame.mixer.music.set_volume(0.3)

            if restart:
                if map_number != '4':
                    [s.kill() for s in all_sprites]
                    [s.kill() for s in weapon_group]
                    completed_levels.clear()
                    dungeon = Dungeon(f'map0{map_number}.tmx')
                    player_x, player_y = dungeon.render()
                    player = Player(8, 2, player_x, player_y, change_mode)
                    hp = 4
                    completed_levels.clear()
                    inventory = {1: 'wooden_bow', 2: None, 3: None}
                    flip = False
                    doors_close = False
                    damage = False
                    visible = True
                    change_mode = False
                    restart = False
                    transit = True
                    for section in range(0, 3):
                        cell = Inventory(section)
                    cell = Inventory(0, True)
                    WeaponInInventory(weapons_image.get('wooden_bow'), 0)
                else:
                    if not final:
                        final = True
                        [s.kill() for s in all_sprites]
                        FinalScreen(1, 1, 265, 0, game_over)
                        # FinalScreen(8, 1, 571, 400, player_win)
                        # for i in range(3):
                        #    FinalScreen(1, 1, bags_coord[i][0], bags_coord[i][1], bag_coins)
                        #    FinalScreen(1, 1, golden_chest_coord[i][0],
                        #                golden_chest_coord[i][1], golden_chest)
                        pygame.mixer.music.load('music/bad_end.mp3')
                        # pygame.mixer.music.load('music/good_end.mp3')
                        pygame.mixer.music.play()
                        FinalScreen(1, 1, 571, 400, player_dead)
                        FinalScreen(6, 4, 500, 300, animated_slimes)
                        FinalScreen(6, 4, 500, 400, animated_slimes, True)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_a:
                        x -= player_v
                    elif event.key == pygame.K_w:
                        y -= player_v
                    elif event.key == pygame.K_d:
                        x += player_v
                    elif event.key == pygame.K_s:
                        y += player_v
                    if event.key == pygame.K_LEFT:
                        if current_weapon in bows:
                            Shot(player.rect.x - 39, player.rect.y + 13, -shot_v, 0, 270)
                        elif current_weapon in swords and len(melee_group.sprites()) == 0:
                            Melee(player.rect.x - 39, player.rect.y + 13, current_weapon, 180)
                    elif event.key == pygame.K_RIGHT:
                        if current_weapon in bows:
                            Shot(player.rect.x + 60, player.rect.y + 13, shot_v, 0, 90)
                        elif current_weapon in swords and len(melee_group.sprites()) == 0:
                            Melee(player.rect.x + 60, player.rect.y + 13, current_weapon, 0)
                    elif event.key == pygame.K_UP:
                        if current_weapon in bows:
                            Shot(player.rect.x + 12, player.rect.y - 36, 0, -shot_v, 180)
                        elif current_weapon in swords and len(melee_group.sprites()) == 0:
                            Melee(player.rect.x + 12, player.rect.y - 36, current_weapon, 90)
                    elif event.key == pygame.K_DOWN:
                        if current_weapon in bows:
                            Shot(player.rect.x + 12, player.rect.y + 69, 0, shot_v, 0)
                        elif current_weapon in swords and len(melee_group.sprites()) == 0:
                            Melee(player.rect.x + 12, player.rect.y + 69, current_weapon, 270)
                    elif event.key == pygame.K_r:
                        restart = True
                    elif event.key == pygame.K_e:
                        button = 'e'
                    elif event.key == pygame.K_1:
                        choose_weapon(1)
                    elif event.key == pygame.K_2:
                        choose_weapon(2)

                elif event.type == pygame.KEYUP and not change_mode:
                    if event.key == pygame.K_a:
                        x += player_v
                    elif event.key == pygame.K_w:
                        y += player_v
                    elif event.key == pygame.K_d:
                        x -= player_v
                    elif event.key == pygame.K_s:
                        y -= player_v
            if (x, y) != (0, 0):
                moving = True
            if x < 0:
                flip = True
            elif x > 0:
                flip = False
            if not final:
                change_mode = False
                player.rect.x += x
                player.rect.y += y
                player_damage = player.update(x, y, flip)
                if player_damage and not damage:
                    hp -= 1
                    damage = True
                    visible = False
                    if hp == 0:
                        restart = True
                shot_group.update(False)
                melee_group.update()
                doors_group.update(doors_close)
                camera.update(player)
                scripts_group.update()
                rooms_group.update()
                particle_group.update()
                barriers_group.update()
                animated_sprites_group.update()
                enemy_group.update()
                bombs_group.update()
                chest_group.update(button)
                key_group.update()
                if inventory[3] is not None:
                    hatch_group.update(button, True)
                else:
                    hatch_group.update(button, False)
                ladder_group.update(button)
                for sprite in all_sprites:
                    camera.apply(sprite)

                tiles_group.draw(screen)
                barriers_group.draw(screen)
                animated_sprites_group.draw(screen)
                if doors_close:
                    doors_group.draw(screen)
                ladder_group.draw(screen)
                melee_group.draw(screen)
                chest_group.draw(screen)
                hatch_group.draw(screen)
                key_group.draw(screen)
                enemy_group.draw(screen)
                bombs_group.draw(screen)
                if damage:
                    frames += 1
                    if frames % 20 == 0:
                        visible = not visible
                    if frames == 100:
                        frames = 0
                        damage = False
                if visible:
                    player_group.draw(screen)
                shot_group.draw(screen)
                particle_group.draw(screen)
                pygame.draw.rect(screen, pygame.Color((172, 50, 50)), (5, 0, 230, 48), 0)
                pygame.draw.rect(screen, pygame.Color((0, 0, 0)), (55 + 45 * hp, 0, 45 * (4 - hp),
                                                                   48), 0)
                health_group.draw(screen)
                all_cells_group.draw(screen)
                weapon_group.draw(screen)
                button = None
        else:
            if len(player_group) == 0:
                transit = True
                ts = tile_width = tile_height = 64
                castle = Castle(level)
                player_x, player_y = castle.render()
                player = MiniPlayer(8, 2, player_x, player_y)
                player_v = 64
                pygame.mixer.music.load('music/castle.mp3')
                pygame.mixer.music.play(-1)
                pygame.mixer.music.set_volume(0.3)
            moving = False
            x, y = 0, 0
            if restart:
                [sprite.kill() for sprite in all_sprites]
                castle = Castle(level)
                player_x, player_y = castle.render()
                player = MiniPlayer(8, 2, player_x, player_y)
                restart = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_a:
                        x = -player_v
                        flip = True
                    elif event.key == pygame.K_w:
                        y = -player_v
                    elif event.key == pygame.K_d:
                        x = player_v
                        flip = False
                    elif event.key == pygame.K_s:
                        y = player_v
                    elif event.key == pygame.K_r:
                        restart = True
            if (x, y) != (0, 0):
                moving = True

            player.rect.x += x
            player.rect.y += y
            player.update(x, y, flip, False)
            slimes_group.update(x, y, flip)
            tables_group.update(x, y, flip)
            spikes_group.update()
            mini_keys_group.update()
            mini_doors_group.update()

            tiles_group.draw(screen)
            slimes_group.draw(screen)
            tables_group.draw(screen)
            mini_keys_group.draw(screen)
            mini_doors_group.draw(screen)
            player_group.draw(screen)
            spikes_group.draw(screen)
        if final:
            screen.fill('black')
            animated_sprites_group.update()
            animated_sprites_group.draw(screen)
        if transit:
            transition()
            transit_time += 1
            if transit_time == 20:
                transit = False
                transit_time = 0
        clock.tick(FPS)
        pygame.display.flip()
    pygame.quit()
