
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
gameIcon = pygame.image.load('backg.png')
pygame.display.set_icon(gameIcon)
bgImage = pygame.image.load('backg.png')  # Background photo
bgImage = pygame.transform.scale(bgImage, (gameWidth, gameHeight))  # Scale to screen size
congratsBgImage = pygame.image.load('backg.png')
congratsBgImage = pygame.transform.scale(congratsBgImage, (gameWidth, gameHeight))  # Scale to screen size

bgImage = pygame.image.load("bgo.png")
bgImage = pygame.transform.scale(bgImage, (gameWidth, gameHeight))
bombImage = pygame.image.load("images/bomb.png")
bombImage = pygame.transform.scale(bombImage, (picSize, picSize))


# Load memory pictures
memoryPictures = [os.path.splitext(file)[0] for file in os.listdir("images")]
memoryPictures = memoryPictures[:13]  # Limit to 13 pairs for consistency
