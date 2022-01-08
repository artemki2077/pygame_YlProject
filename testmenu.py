import pygame
import pygame_menu



pygame.init()
surface = pygame.display.set_mode((600, 400))


def set_difficulty(value, difficulty):
    # Do the job here !
    pass


def start_the_game():
    # Do the job here !
    import main
    main.start()
    pass


menu = pygame_menu.Menu('Welcome', 400, 300, theme=pygame_menu.themes.THEME_BLUE)

menu.add.text_input('Имя: ', default='Artem loh')
menu.add.selector('Цвета :', [('фиолетовый', 1), ('зеленый', 2), ('розовый', 3)],
                  onchange=set_difficulty)
menu.add.button('Play', start_the_game)
menu.add.button('Quit', pygame_menu.events.EXIT)

menu.mainloop(surface)
