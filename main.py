import csv
import socket
import threading
import time
import pygame as pygame
from spritesheet import Spritesheet
import os
import sys


def load_image(name, colorkey=None):
    fullname = os.path.join("skins", name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname).convert_alpha()
    return image


def listen():
    global other_plays
    try:
        while 1:
            data = sock.recv(4096).decode("utf-8")
            other_plays = eval(data)
    except SyntaxError:
        listen()


BLACK_COLOR = pygame.Color("black")
WHITE_COLOR = pygame.Color("white")
GRAY_COLOR = pygame.Color("dimgray")
BLUE_COLOR = pygame.Color("blue")
DARK_GREEN_COLOR = pygame.Color("forestgreen")
GREEN_COLOR = pygame.Color("green")
RED_COLOR = pygame.Color("red")
old_pos_x = 0
old_pos_y = 0

SCREEN_SIZE = WIDTH, HEIGHT = 850, 550
start = (87, 145)
other_plays = {}
other_plays_classes = {}
server = ("192.168.1.65", 10001)


def draw_text(x, y, text, size=20, color=WHITE_COLOR):
    font_name = pygame.font.match_font("hack")
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.topleft = (x, y)
    screen.blit(text_surface, text_rect)


wall_codes = [1, 72, 166, 171, 172, 201, 202, 203, 220, 223, 226, 307, 340, 342, 344]
ladder_codes = [132, 133]
rope = [112]


def collide_with(sprite_rect, level_map, tile_codes_to_check):
    for r, row in enumerate(level_map):
        for c, item_code in enumerate(row):
            if item_code in tile_codes_to_check:
                rect = pygame.Rect(
                    start_x + c * spritesheet.tile_width,
                    start_y + r * spritesheet.tile_height,
                    spritesheet.tile_width,
                    spritesheet.tile_height,
                )

                if sprite_rect.colliderect(rect):
                    # print(f"sprite:{sprite_rect} collides with: {rect},
                    # row: {r}, col: {c}, item_code: {item_code}")
                    return True

    return False


class OtherHero:
    def __init__(self, x, y, color, _ip):
        self.position = pygame.Vector2(x, y)
        self.velocity = pygame.Vector2(0, 0)
        self.id = _ip

        self.width = 24
        self.height = 24
        self.color = color

    def get_bbox(self, position=None):  # -> pygame.Rect
        if position is None:
            return pygame.Rect(
                self.position.x, self.position.y, self.width, self.height
            )
        else:
            return pygame.Rect(position.x, position.y, self.width, self.height)

    def draw(self, _screen):
        if other_plays[self.id][3] == "default":
            pygame.draw.rect(_screen, self.color, self.get_bbox(), 2)
        else:
            scale = pygame.transform.scale(
                surf_skins[
                    other_plays[self.id][3]
                    if self.color == BLUE_COLOR
                    else "r_" + other_plays[self.id][3]
                ],
                (24, 24),
            )
            screen.blit(scale, (self.position.x, self.position.y))
        draw_text(self.position.x, self.position.y - 20, other_plays[self.id][2])

    def update(self):
        if other_plays[self.id] is None:
            del other_plays[self.id]
            del other_plays_classes[self.id]
        else:
            self.position = pygame.Vector2(*other_plays[self.id][0])
            if other_plays[self.id][1]:
                self.color = RED_COLOR
            else:
                self.color = BLUE_COLOR


class Hero:
    def __init__(self, x, y, width, height, name, skin):
        self.position = pygame.Vector2(x, y)
        self.velocity = pygame.Vector2(0, 0)

        self.skin = skin
        self.width = width
        self.height = height
        self.color = (0, 255, 0)

        self.name = name

    def draw(self, surface_to_draw):
        # collide_with_wall = collide_with(self.get_hit_box(self.position), level1_map, wall_codes)
        if self.skin == "default":
            pygame.draw.rect(surface_to_draw, self.color, self.get_bbox(), 2)
        else:
            scale = pygame.transform.scale(
                surf_skins[
                    self.skin if self.color == GREEN_COLOR else "r_" + self.skin
                ],
                (24, 24),
            )
            screen.blit(scale, (self.position.x, self.position.y))
        draw_text(self.position.x, self.position.y - 20, self.name)

    def get_bbox(self, position=None):  # -> pygame.Rect
        if position is None:
            return pygame.Rect(
                self.position.x, self.position.y, self.width, self.height
            )
        else:
            return pygame.Rect(position.x, position.y, self.width, self.height)

    def get_hit_box(self, position=None):  # -> pygame.Rect
        if position is None:
            return pygame.Rect(
                self.position.x + 2,
                self.position.y + 2,
                self.width - 4,
                self.height - 4,
            )
        else:
            return pygame.Rect(
                position.x + 2, position.y + 2, self.width - 4, self.height - 4
            )

    def update(self, events=None):
        global old_pos_x, old_pos_y
        acceleration = pygame.Vector2(0, 0.4)
        old_pos = self.position
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            # print('left')
            acceleration.x = -0.1
        if keys[pygame.K_RIGHT]:
            # print('right')
            acceleration.x = 0.1
        if (
                keys[pygame.K_UP]
                and collide_with(
            self.get_bbox(pygame.Vector2(self.position.x + 2, self.position.y)),
            level1_map,
            wall_codes,
        )
                and collide_with(
            self.get_bbox(pygame.Vector2(self.position.x - 2, self.position.y)),
            level1_map,
            wall_codes,
        )
        ):
            # print('up')
            acceleration.y = -5

        if collide_with(self.get_bbox(), level1_map, ladder_codes):
            if keys[pygame.K_UP]:
                # print('up on ladder')
                self.velocity.y = -1
                acceleration.y = 0
                self.velocity.x = 0
                acceleration.x = 0
            elif keys[pygame.K_DOWN]:
                # print('down on ladder')
                self.velocity.y = 1
                acceleration.y = 0
                self.velocity.x = 0
                acceleration.x = 0
            else:
                # print('stay on ladder')
                self.velocity.y = 0
                acceleration.y = 0

        acceleration.x = acceleration.x - self.velocity.x * 0.05
        acceleration.y = acceleration.y - self.velocity.y * 0.05
        self.velocity = self.velocity + acceleration
        pos_delta = self.velocity + 0.5 * acceleration

        new_pos_dx = pygame.Vector2(self.position.x + pos_delta.x, self.position.y)
        new_pos_dy = pygame.Vector2(self.position.x, self.position.y + pos_delta.y)
        collide_with_wall_by_x = collide_with(
            self.get_hit_box(new_pos_dx), level1_map, wall_codes
        )
        collide_with_wall_by_y = collide_with(
            self.get_hit_box(new_pos_dy), level1_map, wall_codes
        )

        if collide_with_wall_by_x and collide_with_wall_by_y:
            # print("hit to wall by x and y")
            self.velocity.y = 0
            self.velocity.x = 0
        elif collide_with_wall_by_x:
            # print("hit to wall by x")
            self.position.y += pos_delta.y
            self.velocity.x = 0
        elif collide_with_wall_by_y:
            # print("hit to wall by y")
            self.position.x += pos_delta.x
            self.velocity.y = 0
        else:
            self.position += pos_delta
        if my_addr in other_plays and other_plays[my_addr][1]:
            self.color = RED_COLOR
        else:
            self.color = GREEN_COLOR
        if int(self.position.x) != old_pos_x or int(self.position.y) != old_pos_x:
            sock.sendall(str(self.position)[1:-1].encode("utf-8"))
            old_pos_x = int(self.position.x)

            old_pos_x = int(self.position.y)

    def __str__(self):
        return f"pos: {self.position}, vel: {self.velocity}"


def main(name, skin, _screen=None, new=True):
    global sock, my_addr, screen, level1_map, spritesheet, start_x, start_y, surf_skins
    if new:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect(server)
        time.sleep(1)
        sock.sendall(f"{name}, {skin}".encode("utf-8"))
    threading.Thread(target=listen).start()
    my_addr = sock.getsockname()
    print(f"your addr: {my_addr}")
    if _screen is None:
        pygame.init()
        pygame.display.set_caption("Test")
        screen = pygame.display.set_mode(SCREEN_SIZE)
    else:
        screen = _screen

    spritesheet = Spritesheet(
        "assets/tileset3b.png",
        tile_width=24,
        tile_height=24,
        colorkey=pygame.Color(255, 0, 255),
    )
    level1_map = []
    with open("assets/4.csv") as f:
        reader = csv.reader(f, delimiter=",", quotechar='"')
        for row in reader:
            ints_row = [int(i) for i in row]
            level1_map.append(ints_row)

    start_x = (screen.get_width() - len(level1_map[0]) * 24) // 2
    start_y = (screen.get_height() - len(level1_map) * 24) // 2

    surf_skins = {}
    skins = ["default", "lol", 'wall', "circle"]
    for i in skins[1:].copy():
        skins.append("r_" + i)
    for i in skins:
        surf_skins[i] = load_image(i + (".png" if i != "lsd" else ".gif"))

    map_height_px = len(level1_map) * 24
    # hero = Hero(screen.get_width() // 2, start_y + map_height_px - 24 * 2 , 24, 24)
    hero = Hero(screen.get_width() // 2, start_y + 24 * 3, 24, 24, name, skin)
    # screen = pygame.display.set_mode(SCREEN_SIZE, flags=pygame.FULLSCREEN)

    clock = pygame.time.Clock()

    is_running = True
    while is_running:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                is_running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    is_running = False

        screen.fill(BLACK_COLOR)

        for c, row in enumerate(level1_map):
            for r, item_code in enumerate(row):
                if item_code != -1:
                    rect = pygame.Rect(
                        start_x + r * spritesheet.tile_width,
                        start_y + c * spritesheet.tile_height,
                        spritesheet.tile_width,
                        spritesheet.tile_height,
                    )

                    tile_col = item_code % 20
                    tile_row = item_code // 20
                    tile_img = spritesheet.image_at(
                        tile_col=tile_col, tile_row=tile_row
                    )
                    screen.blit(tile_img, rect.topleft)

        hero.update(events)
        hero.draw(screen)
        for i in other_plays:
            if i not in other_plays_classes and i != my_addr:
                if other_plays[i][1]:
                    other_plays_classes[i] = OtherHero(
                        *other_plays[i][0], (255, 0, 0), i
                    )
                else:
                    other_plays_classes[i] = OtherHero(
                        *other_plays[i][0], (0, 0, 255), i
                    )
            elif i != my_addr:
                other_plays_classes[i].update()
                other_plays_classes[i].draw(screen)
            else:
                if other_plays[i][1]:
                    hero.color = (255, 0, 0)

        draw_text(1, 1, str(hero))

        pygame.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    main("artem", "lol")
