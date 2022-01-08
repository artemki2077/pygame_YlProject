import pygame
import pygame_menu



pygame.init()
surface = pygame.display.set_mode((600, 400))


def set_difficulty(value, difficulty):
    # Do the job here !
    print(value)
    pass


def start_the_game():
    # Do the job here !
    import main
    main.main(1,0)
    pass


menu = pygame_menu.Menu('Приветствую лошара', 450, 350, theme=pygame_menu.themes.THEME_BLUE)

menu.add.text_input('Имя: ', default='Artem loh')
menu.add.selector('Скины :', [('фиолетовый',1), ('зеленый', 2), ('розовый', 3)],
                  onchange=set_difficulty)
menu.add.button('Play', start_the_game)
menu.add.button('Quit', pygame_menu.events.EXIT)

menu.mainloop(surface)
