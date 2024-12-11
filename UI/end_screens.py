import pygame
from UI.button import Button

def end_screen(screen, result, start_game, main_menu, get_font):
    while True:
        if result == "win":
            screen.blit(pygame.image.load("Assets/win_screen.png"), (0, 0))
        else:
            screen.blit(pygame.image.load("Assets/lose_screen.png"), (0, 0))

        END_MOUSE_POS = pygame.mouse.get_pos()

        playagain_button = Button(
            image=None,
            pos=(375, 430),
            text_input="PLAY AGAIN",
            font=get_font(45),
            base_color="black",
            hovering_color="green",
        )
        playagain_button.changeColor(END_MOUSE_POS)
        playagain_button.update(screen)

        back_button = Button(
            image=None,
            pos=(310, 520),
            text_input="BACK TO MAIN MENU",
            font=get_font(45),
            base_color="black",
            hovering_color="blue",
        )
        back_button.changeColor(END_MOUSE_POS)
        back_button.update(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if playagain_button.checkForInput(END_MOUSE_POS):
                    start_game()
                if back_button.checkForInput(END_MOUSE_POS):
                    main_menu()

        pygame.display.update()
