import pygame
import os.path
from sqlalchemy import MetaData, create_engine, Table, Column, Integer, String, ForeignKey, DateTime, select, or_, and_
import datetime
import json
from hashlib import sha256
import skins_menu

metadata = MetaData()

engine = create_engine(
    "postgresql+psycopg2://vwkpsapgezatjo:0707b3f5b76e2dcc9cb997d24e99eaa3332d7b160736f6ae6f56456ec103aa0e@ec2-52-213-119-221.eu-west-1.compute.amazonaws.com:5432/dbfhqn219nh3ea")

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
                 Column("account_id", Integer(), ForeignKey('Accounts.id'),
                        nullable=False),
                 )

Skins = Table("Skins", metadata,
              Column("id", Integer(), primary_key=True),
              Column("skin_Name", String(100), nullable=False),
              Column("user_id", Integer(), ForeignKey('Users.id'), nullable=False))

metadata.create_all(engine)


def draw_text(x, y, text, size=20, color=(255, 255, 255)):
    font_name = "assets/Pixeboy-z8XGD.ttf"
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.topleft = (x, y)
    screen.blit(text_surface, text_rect)
    return text_surface


SCREEN_SIZE = WIDTH, HEIGHT = 850, 550


def main(_screen=None):
    global screen
    is_raning = True
    index = 0
    if _screen is None:
        pygame.init()
        pygame.display.set_caption("Test")
        screen = pygame.display.set_mode(SCREEN_SIZE)
    else:
        screen = _screen
    user_date = ["", ""]
    max_index = 3
    if os.path.exists("config.json"):
        print(type(engine))
        skins_menu.start(screen)
    error = ''

    while is_raning:
        poss = [[305, 250], [305, 350], [380, 410], [365, 465]]
        screen.fill((0, 0, 0))
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
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
                elif event.key == pygame.K_BACKSPACE:
                    user_date[index] = user_date[index][:-1]
                elif index <= 1:
                    user_date[index] += event.unicode
                elif event.key == pygame.K_RETURN:
                    if index == 3:
                        is_raning = False
                    elif index == 2:
                        conn = engine.connect()
                        r = conn.execute(select([Users.c.login, Users.c.password, Users.c.id, Users.c.account_id]).where(and_(Users.c.login == user_date[0], Users.c.password == sha256(user_date[1].encode('utf-8')).hexdigest())))
                        pp = r.first()
                        if pp:
                            with open("config.json", "w") as f:
                                json.dump({"password": pp[0], "login": pp[1], "id": pp[2], "account_id": pp[3]}, f)
                            skins_menu.start(screen)

                        else:
                            error = "incorrect password or login!!!"

        draw_text(260, 50, "Bank", 180)

        draw_text(poss[0][0] + 70, poss[0][1] - 50, "Login", 40)
        login = pygame.Rect(poss[0][0] + 20, poss[0][1] - 20, 200, 40)
        login_text = draw_text(335 - (((len(user_date[0]) - 9) * 10) if len(user_date[0]) > 9 else 0), 240, user_date[0], 40)
        login.w = max(200, login_text.get_width() + 20)
        if login.w != 200:
            login = login.move(-((len(user_date[0]) - 9) * 10), 0)
            poss[0][0] = poss[0][0] - ((len(user_date[0]) - 9) * 10)
        pygame.draw.rect(screen, (255, 255, 255), login, 2)

        draw_text(poss[1][0] + 50, poss[1][1] - 50, "Password", 40)
        password = pygame.Rect(poss[1][0] + 20, poss[1][1] - 20, 200, 40)
        password_text = draw_text(335 - (((len(user_date[1]) - 9) * 10) if len(user_date[1]) > 9 else 0), 340, user_date[1], 40)
        password.w = max(200, password_text.get_width() + 20)
        if password.w != 200:
            password = password.move(-((len(user_date[1]) - 9) * 10), 0)
            poss[1][0] = poss[1][0] - ((len(user_date[1]) - 9) * 10)
        pygame.draw.rect(screen, (255, 255, 255), password, 2)

        draw_text(poss[2][0] + 20, poss[2][1] - 10, "go", 40)

        draw_text(poss[3][0] + 20, poss[3][1] - 10, "back", 40)

        draw_text(280, 500, error, 30, color=(255, 0, 0))

        pygame.draw.circle(screen, (255, 255, 255), poss[index], 10)
        pygame.display.flip()


if __name__ == "__main__":
    main()
