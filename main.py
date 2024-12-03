import pygame, os, random

# Initialize Pygame and Mixer
pygame.init()
pygame.mixer.init()

# Load Background Music
pygame.mixer.music.load('OneDrive/Documents/Python Assignment/games/star.mp3')
pygame.mixer.music.play(-1)  # Play the music in a loop

# Game Configuration
gameWidth = 840
gameHeight = 640
picSize = 128
gameColumns = 5
gameRows = 4
padding = 10
leftMargin = 75
topMargin = (gameHeight - ((picSize + padding) * gameRows)) // 2
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)

screen = pygame.display.set_mode((gameWidth, gameHeight))
pygame.display.set_caption('Memory Game')
font = pygame.font.Font(None, 74)
button_font = pygame.font.Font(None, 50)

# Define button properties for the menu
button_width = 200
button_height = 80
button_spacing = 40
start_button_rect = pygame.Rect((gameWidth // 2 - button_width - button_spacing // 2, gameHeight // 2),
                                (button_width, button_height))
exit_button_rect = pygame.Rect((gameWidth // 2 + button_spacing // 2, gameHeight // 2),
                               (button_width, button_height))

# Load assets
gameIcon = pygame.image.load('OneDrive/Documents/Python Assignment/games/bgo.png')
pygame.display.set_icon(gameIcon)
bgImage = pygame.image.load('OneDrive/Documents/Python Assignment/games/bgo.png')  # Background photo
bgImage = pygame.transform.scale(bgImage, (gameWidth, gameHeight))  # Scale to screen size

# Prepare memory pictures
memoryPictures = []
for item in os.listdir('OneDrive/Documents/Python Assignment/games/images/'):
    memoryPictures.append(item.split('.')[0])
memoryPicturesCopy = memoryPictures.copy()
memoryPictures.extend(memoryPicturesCopy)
memoryPicturesCopy.clear()
random.shuffle(memoryPictures)

# Load and prepare images
nemPics = []
nemPicsRect = []
hiddenImages = []

for item in memoryPictures:
    picture = pygame.image.load(f'OneDrive/Documents/Python Assignment/games/images/{item}.png')
    picture = pygame.transform.scale(picture, (picSize, picSize))
    nemPics.append(picture)
    pictureRect = picture.get_rect()
    nemPicsRect.append(pictureRect)

for i in range(len(nemPicsRect)):
    nemPicsRect[i][0] = leftMargin + ((picSize + padding) * (i % gameColumns))
    nemPicsRect[i][1] = topMargin + ((picSize + padding) * (i // gameColumns))
    hiddenImages.append(False)

# Helper function to draw images with rounded corners
def draw_rounded_image(surface, image, rect, radius):
    mask = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
    pygame.draw.rect(mask, (255, 255, 255, 255), (0, 0, rect.width, rect.height), border_radius=radius)
    image = pygame.transform.scale(image, (rect.width, rect.height))
    surface.blit(image, (rect.x, rect.y), special_flags=pygame.BLEND_RGBA_MIN)
    surface.blit(mask, (rect.x, rect.y), special_flags=pygame.BLEND_RGBA_MULT)

# Display the menu
def display_menu():
    menu_running = True
    while menu_running:
        # Draw background
        screen.blit(bgImage, (0, 0))

        # Display title
        title_text = font.render("Memory Card Game", True, WHITE)
        screen.blit(title_text, (gameWidth // 2 - title_text.get_width() // 2, gameHeight // 4 - title_text.get_height()))

        # Draw Start button
        pygame.draw.rect(screen, GRAY, start_button_rect, border_radius=15)
        start_text = button_font.render("Start", True, BLACK)
        screen.blit(start_text, (start_button_rect.x + (button_width - start_text.get_width()) // 2,
                                 start_button_rect.y + (button_height - start_text.get_height()) // 2))

        # Draw Exit button
        pygame.draw.rect(screen, GRAY, exit_button_rect, border_radius=15)
        exit_text = button_font.render("Exit", True, BLACK)
        screen.blit(exit_text, (exit_button_rect.x + (button_width - exit_text.get_width()) // 2,
                                exit_button_rect.y + (button_height - exit_text.get_height()) // 2))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if start_button_rect.collidepoint(event.pos):
                    menu_running = False  # Start the game
                elif exit_button_rect.collidepoint(event.pos):
                    pygame.quit()
                    exit()

# Call the menu before the game
display_menu()

# Initialize game variables
selection1 = None
selection2 = None
flip_back_time = None  # Timer for flipping back cards
start_time = pygame.time.get_ticks()

# Main Game Loop
gameLoop = True
clock = pygame.time.Clock()

while gameLoop:
    # Limit the frame rate
    clock.tick(30)

    # Input events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gameLoop = False
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for idx, item in enumerate(nemPicsRect):
                if item.collidepoint(event.pos):
                    if selection1 is None:
                        selection1 = idx
                        hiddenImages[selection1] = True
                    elif selection2 is None and idx != selection1:
                        selection2 = idx
                        hiddenImages[selection2] = True
                        flip_back_time = pygame.time.get_ticks() + 1000  # 1 second delay

    # Flip back cards if they don't match
    if flip_back_time and pygame.time.get_ticks() >= flip_back_time:
        if memoryPictures[selection1] != memoryPictures[selection2]:
            hiddenImages[selection1] = False
            hiddenImages[selection2] = False
        selection1, selection2 = None, None
        flip_back_time = None

    # Draw the background
    screen.blit(bgImage, (0, 0))

    # Draw cards with rounded corners
    for i in range(len(memoryPictures)):
        if hiddenImages[i]:
            draw_rounded_image(screen, nemPics[i], nemPicsRect[i], radius=15)
        else:
            pygame.draw.rect(
                screen, 
                WHITE, 
                (nemPicsRect[i][0], nemPicsRect[i][1], picSize, picSize), 
                border_radius=15
            )

    # Check for win condition
    if all(hiddenImages):
        end_time = pygame.time.get_ticks()
        play_time = (end_time - start_time) / 1000
        screen.fill(BLACK)
        win_message = font.render("Congratulations!", True, WHITE)
        time_message = font.render(f"Time: {play_time:.2f}s", True, WHITE)
        screen.blit(win_message, (gameWidth // 2 - win_message.get_width() // 2, gameHeight // 2 - 100))
        screen.blit(time_message, (gameWidth // 2 - time_message.get_width() // 2, gameHeight // 2))
        pygame.display.update()
        pygame.time.delay(3000)
        gameLoop = False

    # Update display
    pygame.display.update()

pygame.quit()

