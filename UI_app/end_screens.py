import pygame
from UI_app.button import Button

def end_screen(screen, result, restart_game, main_menu, get_font):
    """End screen logic."""
    while True:
        if result == "win":
            screen.blit(pygame.image.load("win_screen.png"), (0, 0))
            button_base_colour = "black"
        else:
            screen.blit(pygame.image.load("lose_screen.png"), (0, 0))
            button_base_colour = "light blue"

        END_MOUSE_POS = pygame.mouse.get_pos()

        # Create buttons (Play Again, Back to Menu)
        playagain_button = Button(
            image=None,
            pos=(410, 470),
            text_input="play again",
            font=get_font(45),
            base_color=button_base_colour,
            hovering_color="green",
        )
        playagain_button.changeColor(END_MOUSE_POS)
        playagain_button.update(screen)

        back_button = Button(
            image=None,
            pos=(440, 550),
            text_input="back to menu",
            font=get_font(45),
            base_color=button_base_colour,
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
                    restart_game()  # Calls the restart_game method
                if back_button.checkForInput(END_MOUSE_POS):
                    main_menu()  # Calls the main_menu method

        pygame.display.update()
