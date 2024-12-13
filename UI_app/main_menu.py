import pygame
from UI_app.button import Button

print("main_menu.py is being loaded")

def main_menu(screen, start_game, get_font):
    """Main menu screen."""
    while True:
        screen.fill((0, 0, 0))  # Black background
        screen.blit(pygame.image.load("UI_app/main_menu_bg.png"), (0, 0))  # Background image

        MAIN_MOUSE_POS = pygame.mouse.get_pos()

        play_button = Button(
            image=None,
            pos=(640, 300),
            text_input="PLAY",
            font=get_font(50),
            base_color="white",
            hovering_color="yellow",
        )
        quit_button = Button(
            image=None,
            pos=(640, 500),
            text_input="QUIT",
            font=get_font(50),
            base_color="white",
            hovering_color="yellow",
        )

        play_button.changeColor(MAIN_MOUSE_POS)
        play_button.update(screen)
        quit_button.changeColor(MAIN_MOUSE_POS)
        quit_button.update(screen)

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_button.checkForInput(MAIN_MOUSE_POS):
                    selected_level = difficulty_selection(screen, start_game, get_font)  # Get selected level
                    return selected_level  
                if quit_button.checkForInput(MAIN_MOUSE_POS):
                    pygame.quit()
                    exit()
        pygame.display.update()

def difficulty_selection(screen, start_game, get_font):
    """Difficulty selection screen."""
    while True:
        screen.fill((0, 0, 0))  # Black background
        screen.blit(pygame.image.load("UI_app/difficulty_menu.png"), (0, 0))  # Background image

        DIFF_MOUSE_POS = pygame.mouse.get_pos()

        easy_button = Button(
            image=None,
            pos=(640, 300),
            text_input="EASY",
            font=get_font(50),
            base_color="white",
            hovering_color="green",
        )
        medium_button = Button(
            image=None,
            pos=(640, 400),
            text_input="MEDIUM",
            font=get_font(50),
            base_color="white",
            hovering_color="orange",
        )
        hard_button = Button(
            image=None,
            pos=(640, 500),
            text_input="HARD",
            font=get_font(50),
            base_color="white",
            hovering_color="red",
        )

        easy_button.changeColor(DIFF_MOUSE_POS)
        easy_button.update(screen)
        medium_button.changeColor(DIFF_MOUSE_POS)
        medium_button.update(screen)
        hard_button.changeColor(DIFF_MOUSE_POS)
        hard_button.update(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if easy_button.checkForInput(DIFF_MOUSE_POS):
                    return "easy"  # Return the selected level
                if medium_button.checkForInput(DIFF_MOUSE_POS):
                    return "medium"
                if hard_button.checkForInput(DIFF_MOUSE_POS):
                    return "hard"

        pygame.display.update()

def end_screen(screen, result, start_game, main_menu, get_font):
    while True:
        if result == "win":
            screen.blit(pygame.image.load("win_screen.png"), (0, 0))
            button_base_colour = "black"
        else:
            screen.blit(pygame.image.load("lose_screen.png"), (0, 0))
            button_base_colour = "light blue"

        END_MOUSE_POS = pygame.mouse.get_pos()

        playagain_button = Button(
            image=None,
            pos=(410, 470),
            text_input="Play Again",
            font=get_font(45),
            base_color=button_base_colour,
            hovering_color="green",
        )
        playagain_button.changeColor(END_MOUSE_POS)
        playagain_button.update(screen)

        back_button = Button(
            image=None,
            pos=(440, 550),
            text_input="Back to Menu",
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
                    start_game()  # This should start a new game
                    return  # Return from end screen and restart the game
                if back_button.checkForInput(END_MOUSE_POS):
                    main_menu(screen, start_game, get_font)  # This should take you back to the main menu
                    return  # Exit from the end screen and go back to the main menu

        pygame.display.update()
