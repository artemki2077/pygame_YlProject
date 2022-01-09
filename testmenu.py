import pygame
import main


def draw_text(x, y, text, size=20, color=(255, 255, 255)):
    font_name = "assets/Pixeboy-z8XGD.ttf"
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.topleft = (x, y)
    screen.blit(text_surface, text_rect)
    return text_surface


SCREEN_SIZE = width, height = 850, 550
pygame.init()
pygame.display.set_caption("Menu")
screen = pygame.display.set_mode(SCREEN_SIZE)
is_running = True
index = 0
poss = [(380, 260), (370, 310), (380, 360)]
name = ""

while is_running:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            is_running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                is_running = False
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
                    main.main(name, "lolick", screen)
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
