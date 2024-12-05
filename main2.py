import pygame
import os
import random

# Initialize Pygame and Mixer
pygame.init()
pygame.mixer.init()

# Load Background Music
pygame.mixer.music.load('star.mp3')
pygame.mixer.music.play(-1)  # Play music in a loop

# Game Configuration
gameWidth, gameHeight = 840, 640
picSize = 128
padding = 10
leftMargin, topMargin = 75, 70
WHITE, BLACK, GRAY = (255, 255, 255), (0, 0, 0), (200, 200, 200)
nemPics = []  # List to store card images
nemPicsRect = []  # List to store card rectangles
hiddenImages = []  # List to store card visibility status


screen = pygame.display.set_mode((gameWidth, gameHeight))
pygame.display.set_caption("Memory Card Game")
font = pygame.font.Font(None, 74)
button_font = pygame.font.Font(None, 50)

# Load assets
bgImage = pygame.image.load("bgo.png")
bgImage = pygame.transform.scale(bgImage, (gameWidth, gameHeight))
bombImage = pygame.image.load("images/bomb.png")
bombImage = pygame.transform.scale(bombImage, (picSize, picSize))

# Load memory pictures
memoryPictures = [os.path.splitext(file)[0] for file in os.listdir("images")]
memoryPictures = memoryPictures[:13]  # Limit to 13 pairs for consistency


def setup_game(level):
    global memoryPictures, nemPics, nemPicsRect, hiddenImages
    memoryPictures = []
    for item in os.listdir('images'):
        memoryPictures.append(item.split('.')[0])

    # Define grid and bomb configuration
    rows, cols, num_bombs = {
        "easy": (3, 3, 1),  # 3x3 grid with 1 bomb
        "medium": (4, 4, 2),  # 4x4 grid with 2 bombs
        "hard": (5, 5, 3),  # 5x5 grid with 3 bombs
    }[level]

    num_pairs = (rows * cols - num_bombs) // 2

    # Ensure there are enough unique images for the selected level
    if num_pairs > len(memoryPictures):
        raise ValueError("Not enough unique images for the selected level.")

    # Dynamic card size and padding calculation
    global picSize, padding, leftMargin, topMargin
    grid_width = gameWidth - 2 * leftMargin
    grid_height = gameHeight - 2 * topMargin
    picSize = min(grid_width // cols, grid_height // rows) - 10  # Adjust with padding
    padding = 10
    leftMargin = (gameWidth - (picSize + padding) * cols + padding) // 2
    topMargin = (gameHeight - (picSize + padding) * rows + padding) // 2

    # Select images for the game
    selected_images = random.sample(memoryPictures, num_pairs)
    selected_images *= 2  # Duplicate to make pairs
    selected_images += ["bomb"] * num_bombs
    random.shuffle(selected_images)

    # Reset global variables
    nemPics.clear()
    nemPicsRect.clear()
    hiddenImages.clear()

    # Load images and set positions
    for item in selected_images:
        picture = pygame.image.load(f'images/{item}.png')
        picture = pygame.transform.scale(picture, (picSize, picSize))
        nemPics.append(picture)
        pictureRect = picture.get_rect()
        nemPicsRect.append(pictureRect)

    for i in range(len(nemPicsRect)):
        nemPicsRect[i][0] = leftMargin + ((picSize + padding) * (i % cols))
        nemPicsRect[i][1] = topMargin + ((picSize + padding) * (i // cols))
        hiddenImages.append(False)

    return nemPics, nemPicsRect, selected_images, hiddenImages, rows, cols, num_bombs

def shuffle_unmatched_cards(memoryPictures, hiddenImages, nemPics, nemPicsRect, rows, cols):
    # Get the indices of all unmatched (hidden) and non-bomb cards
    unmatched_indices = [
        i for i, (pic, hidden) in enumerate(zip(memoryPictures, hiddenImages)) 
        if not hidden and pic != "bomb"  # Only shuffle cards that are not bombs
    ]
    unmatched_pictures = [memoryPictures[idx] for idx in unmatched_indices]
    random.shuffle(unmatched_pictures)  # Shuffle the unmatched cards

    # Update the memoryPictures array with the shuffled unmatched cards
    for i, idx in enumerate(unmatched_indices):
        memoryPictures[idx] = unmatched_pictures[i]
        if unmatched_pictures[i] != "bomb":
            nemPics[idx] = pygame.image.load(f"images/{unmatched_pictures[i]}.png")
            nemPics[idx] = pygame.transform.scale(nemPics[idx], (picSize, picSize))

    # Update the card positions in nemPicsRect (no need to shuffle positions)
    for idx, rect in enumerate(nemPicsRect):
        rect.update(
            leftMargin + (idx % cols) * (picSize + padding),
            topMargin + (idx // cols) * (picSize + padding),
            picSize, picSize,
        )


def display_menu():
    menu_running = True
    while menu_running:
        screen.blit(bgImage, (0, 0))
        title_text = font.render("Memory Card Game", True, WHITE)
        screen.blit(title_text, (gameWidth // 2 - title_text.get_width() // 2, 100))

        button_texts = ["Easy", "Medium", "Hard", "Exit"]
        buttons = []

        for i, text in enumerate(button_texts):
            button_rect = pygame.Rect(
                gameWidth // 2 - 100, 200 + i * 100, 200, 80
            )
            buttons.append(button_rect)
            pygame.draw.rect(screen, GRAY, button_rect)
            text_render = button_font.render(text, True, BLACK)
            screen.blit(
                text_render,
                (
                    button_rect.x + (button_rect.width - text_render.get_width()) // 2,
                    button_rect.y + (button_rect.height - text_render.get_height()) // 2,
                ),
            )

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for i, rect in enumerate(buttons):
                    if rect.collidepoint(event.pos):
                        if button_texts[i] == "Exit":
                            pygame.quit()
                            exit()
                        return button_texts[i].lower()


def game_loop(level):
    nemPics, nemPicsRect, memoryPictures, hiddenImages, rows, cols, num_bombs = setup_game(level)
    selection1, selection2 = None, None
    flip_back_time = None
    start_time = pygame.time.get_ticks()
    matched_cards = set()

    gameLoop = True
    clock = pygame.time.Clock()

    while gameLoop:
        clock.tick(30)
        elapsed_time = (pygame.time.get_ticks() - start_time) / 1000

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameLoop = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for idx, rect in enumerate(nemPicsRect):
                    if hiddenImages[idx] or idx in matched_cards:
                        continue
                    if rect.collidepoint(event.pos):
                        if memoryPictures[idx] == "bomb":
                            # Show bomb and shuffle unmatched cards
                            hiddenImages[idx] = True
                            shuffle_unmatched_cards(memoryPictures, hiddenImages, nemPics, nemPicsRect, rows, cols)
                        elif selection1 is None:
                            selection1 = idx
                            hiddenImages[selection1] = True
                        elif selection2 is None and idx != selection1:
                            selection2 = idx
                            hiddenImages[selection2] = True
                            flip_back_time = pygame.time.get_ticks() + 1000

        if flip_back_time and pygame.time.get_ticks() >= flip_back_time:
            if memoryPictures[selection1] != memoryPictures[selection2]:
                hiddenImages[selection1] = False
                hiddenImages[selection2] = False
            else:
                matched_cards.update([selection1, selection2])
            selection1, selection2, flip_back_time = None, None, None

        screen.blit(bgImage, (0, 0))  # Main game background

        for idx in range(len(memoryPictures)):
            if hiddenImages[idx] or idx in matched_cards:
                screen.blit(nemPics[idx], nemPicsRect[idx])
            else:
                pygame.draw.rect(screen, GRAY, nemPicsRect[idx], border_radius=15)

        timer_text = font.render(f"Time: {elapsed_time:.2f}s", True, WHITE)
        screen.blit(timer_text, (10, 10))

        if len(matched_cards) == len(memoryPictures) - num_bombs:
            # Display the win screen with background
            win_screen = True
            while win_screen:
                screen.blit(bgImage, (0, 0))  # Display background in win screen
                win_text = font.render("Congratulations!", True, BLACK)
                screen.blit(win_text, (gameWidth // 2 - win_text.get_width() // 2, gameHeight // 2 - 50))
                time_text = font.render(f"Time: {elapsed_time:.2f}s", True, BLACK)
                screen.blit(time_text, (gameWidth // 2 - time_text.get_width() // 2, gameHeight // 2 + 50))
                pygame.display.update()

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        exit()
                    elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        win_screen = False

            gameLoop = False

        pygame.display.update()


while True:
    level = display_menu()
    game_loop(level)