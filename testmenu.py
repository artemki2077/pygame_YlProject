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
    main.main(1, 0)
    pass


def start_the_skins():
    # Do the job here !
    menu2.mainloop(surface)


def start_vzad():

    menu.mainloop(surface)


menu = pygame_menu.Menu('Приветствую лошара', 450, 350, theme=pygame_menu.themes.THEME_BLUE)

menu.add.text_input('Имя: ', default='Artem loh')
menu2 = pygame_menu.Menu('Скины из кс украли', 450, 350, theme=pygame_menu.themes.THEME_BLUE)
menu2.add.selector('Скины :', [('фиолетовый', 1), ('зеленый', 2), ('розовый', 3)],
                   onchange=set_difficulty)
menu2.add.button('В зад', start_vzad)
menu.add.button('Скины', start_the_skins)
menu.add.button('Play', start_the_game)
menu.add.button('Quit', pygame_menu.events.EXIT)

menu.mainloop(surface)
