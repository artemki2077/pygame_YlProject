import testmenu
import pygame
import os
import sys
from sqlalchemy import select, insert, Table, Column, Integer, String, ForeignKey, MetaData, create_engine, DateTime, update
import datetime
import json

metadata = MetaData()

engine = create_engine(
    "postgresql+psycopg2://egerxqhtcwcnti:c2de0ab971d2e36317f9ab03d097191edd79d154f032d86efdce83e6f56232b7@ec2-52-208"
    "-221-89.eu-west-1.compute.amazonaws.com:5432/dagdtfhhmkkc6u")

# Ниже объекты для управления базой данных и каждый отвечает за свою таблицу

Accounts = Table("Accounts", metadata,
                 Column('id', Integer(), primary_key=True),
                 Column('balance', Integer(), nullable=False), )

Users = Table("Users", metadata,
              Column('id', Integer(), primary_key=True),
              Column('login', String(100), unique=True, nullable=False),
              Column("password", String(100), nullable=False),
              Column("account_id", Integer(), ForeignKey('Accounts.id'),
                     nullable=False),
              )

Transactions = Table("Transactions", metadata,
                     Column("id", Integer(), primary_key=True),
                     Column("account_id_from", Integer(),
                            ForeignKey('Accounts.id'),
                            nullable=False),
                     Column("account_id_to", Integer(),
                            ForeignKey('Accounts.id'),
                            nullable=False),
                     Column("amount", Integer(),
                            nullable=False),
                     Column("comment", String(100)),
                     Column("time", DateTime(), default=datetime.datetime.utcnow)
                     )

Projects = Table("Projects", metadata,
                 Column('id', Integer(), primary_key=True),
                 Column('name', String(100), unique=True, nullable=False),
                 Column("password", String(100), nullable=False),
                 Column("User", Integer(), ForeignKey('Users.id'), unique=True, nullable=False),
                 Column("account_id", Integer(), ForeignKey('Accounts.id'), nullable=False), )

Skins = Table("Skins", metadata,
              Column("id", Integer(), primary_key=True),
              Column("skin_Name", String(100), nullable=False),
              Column("user_id", Integer(), ForeignKey('Users.id'), nullable=False))

metadata.create_all(engine)


def load_image(name, colorkey=None):
    fullname = os.path.join('skins', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


def draw_text(x, y, text, size=20, color=(255, 255, 255)):
    font_name = "assets/Pixeboy-z8XGD.ttf"
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.topleft = (x, y)
    screen.blit(text_surface, text_rect)
    return text_surface


def update_conf(conf, skin):
    conf["skin"] = skin
    with open("config.json", "w") as f:
        json.dump(conf, f)


def inventory(config):
    conn = engine.connect()
    r = conn.execute(select([Skins.c.skin_Name]).where(Skins.c.user_id == config["id"]))
    return r.first()


SCREEN_SIZE = WIDTH, HEIGHT = 850, 550


def start(_screen=None):
    global screen
    with open("config.json", "r") as f:
        config = json.loads(f.read())
    skin_size = (100, 100)
    skins = ["default", "lol"]
    skin_index = 0
    is_raning = True
    index = 0
    max_index = 1
    if _screen is None:
        pygame.init()
        pygame.display.set_caption("Test")
        screen = pygame.display.set_mode(SCREEN_SIZE)
    else:
        screen = _screen
    surf_skins = []
    for i in skins:
        surf_skins.append(load_image(i + ".png"))
    buy_or_use = ["buy", "use"]
    invent = inventory(config)
    invent = [] if invent is None else list(invent)
    invent.append("default")
    error_color = (255, 0, 0)
    print(invent)
    error = ""
    while is_raning:
        img_skin = surf_skins[skin_index]
        screen.fill((0, 0, 0))
        poss = [[390, 380], [375, 435]]
        # all_sprites.draw(surface=screen)
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    is_running = False
                elif event.key == pygame.K_DOWN:
                    index += 1
                    if index == max_index + 1:
                        index = 0
                elif event.key == pygame.K_UP:
                    index -= 1
                    if index == -1:
                        index = max_index
                elif event.key == pygame.K_RIGHT:
                    skin_index += 1
                    if skin_index == len(skins):
                        skin_index = 0
                elif event.key == pygame.K_LEFT:
                    skin_index -= 1
                    if skin_index == -1:
                        skin_index = len(skins) - 1
                elif event.key == pygame.K_RETURN:
                    if index == 1:
                        testmenu.stat_main_menu(screen)
                    elif index == 0:
                        if skins[skin_index] not in invent:
                            conn = engine.connect()
                            r = conn.execute(select([Accounts.c.balance]).where(Accounts.c.id == config["account_id"]))
                            balance = r.first()[0]
                            if balance >= 100:
                                ins = conn.execute(insert(Skins).values(skin_Name=skins[skin_index], user_id=config["id"]))
                                invent.append(skins[skin_index])
                                conn.execute(update(Accounts).where(Accounts.c.id == config["account_id"]).values(balance=balance - 100))
                                error = ""
                            else:
                                error_color = (255, 0, 0)
                                error = "you don't have enough money, the skin costs 100"
                        else:
                            update_conf(config, skins[skin_index])
                            error_color = (0, 255, 0)
                            error = "success"

        scale = pygame.transform.scale(img_skin, skin_size)

        screen.blit(scale, ((WIDTH // 2) - (skin_size[0] // 2), (HEIGHT // 3.5) - (skin_size[1] // 2)))
        draw_text(*((WIDTH // 2) - len(skins[skin_index]) * 8, (HEIGHT // 2)), skins[skin_index], size=40)
        pygame.draw.lines(screen, (255, 255, 255), True,
                          [[(WIDTH // 3), (HEIGHT // 3.5) - 20], [(WIDTH // 3), (HEIGHT // 3.5) + 20],
                           [(WIDTH // 3) - 20, (HEIGHT // 3.5)]], 10)
        pygame.draw.lines(screen, (255, 255, 255), True,
                          [[WIDTH - (WIDTH // 3), (HEIGHT // 3.5) - 20], [WIDTH - (WIDTH // 3), (HEIGHT // 3.5) + 20],
                           [WIDTH - (WIDTH // 3) + 20, (HEIGHT // 3.5)]], 10)

        draw_text(poss[0][0] + 20, poss[0][1] - 10, buy_or_use[skins[skin_index] in invent], 40)
        draw_text(poss[1][0] + 20, poss[1][1] - 10, "back", 40)

        draw_text((WIDTH // 2) - len(error) * 8, 500, error, 30, color=error_color)
        pygame.draw.circle(screen, (255, 255, 255), poss[index], 10)
        pygame.display.flip()


if __name__ == "__main__":
    start()
