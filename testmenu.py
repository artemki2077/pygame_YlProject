import json
import os
import pygame
import main as game
import bank_login


def draw_text(x, y, text, size=20, color=(255, 255, 255)):
    font_name = "assets/Pixeboy-z8XGD.ttf"
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.topleft = (x, y)
    screen.blit(text_surface, text_rect)
    return text_surface


def stat_main_menu(_screen=None):
    global screen
    SCREEN_SIZE = width, height = 850, 550
    if _screen is None:
        pygame.init()
        pygame.display.set_caption("Menu")
        screen = pygame.display.set_mode(SCREEN_SIZE)
    else:
        screen = _screen
    menu_is_running = True
    index = 0
    poss = [(380, 260), (370, 310), (380, 360)]
    name = ""
    new = True
    while menu_is_running:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                menu_is_running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    menu_is_running = False
                elif event.key == pygame.K_DOWN:
                    index += 1
                    if index == 3:
                        index = 0
                elif event.key == pygame.K_UP:
                    index -= 1
                    if index == -1:
                        index = 2
                elif event.key == pygame.K_RETURN:
                    if index == 0:
                        if os.path.exists("config.json"):
                            with open("config.json", "r") as f:
                                conf = json.load(f)
                            if "skin" not in conf:
                                conf["skins"] = "default"
                            game.main(name, conf["skin"], screen, new)
                            new = False
                        else:
                            game.main(name, "default", screen)
                            new = False
                    elif index == 1:
                        bank_login.main(screen)
                    elif index == 2:
                        pygame.quit()
                elif event.key == pygame.K_BACKSPACE:
                    name = name[:-1]
                else:
                    name += event.unicode

        screen.fill((0, 0, 0))
        inp = pygame.Rect(360, 180, 140, 40)
        draw_text(280, 100, "Main menu", 80)
        name_text = draw_text(370 - (((len(name) - 7) * 10) if len(name) > 7 else 0), 190, name, 40)
        draw_text(poss[0][0] + 20, poss[0][1] - 10, "play", 40)
        draw_text(poss[1][0] + 20, poss[1][1] - 10, "skins", 40)
        draw_text(poss[2][0] + 20, poss[2][1] - 10, "exit", 40)
        inp.w = max(150, name_text.get_width() + 20)
        if inp.w != 150:
            inp = inp.move(-((len(name) - 7) * 10), 0)
        # if inp.w > 150:
        #     inp.x -= name_text.get_width() / 2
        pygame.draw.circle(screen, (255, 255, 255), poss[index], 10)
        pygame.draw.rect(screen, (255, 255, 255), inp, 2)
        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    stat_main_menu()
