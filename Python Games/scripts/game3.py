import pygame
import random
import math
import os
import sys

pygame.init()
pygame.mixer.init()  # Initialize the mixer module

# Determine the base path for resources
if getattr(sys, 'frozen', False):
    # If the application is run as a bundle, use sys._MEIPASS
    BASE_PATH = sys._MEIPASS
else:
    BASE_PATH = os.path.dirname(os.path.abspath(__file__))

FPS = 60
WIDTH, HEIGHT = 800, 800
ROWS = 4
COLS = 4

RECT_HEIGHT = HEIGHT // ROWS
RECT_WIDTH = WIDTH // COLS

OUTLINE_COLOR = (187, 173, 160)
OUTLINE_THICKNESS = 10
BACKGROUND_COLOR = (205, 192, 180)
FONT_COLOR = (119, 110, 101)

FONT = pygame.font.SysFont("comicsans", 60, bold=True)
MOVE_VEL = 20

WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tile Twister")

music_path = os.path.join(BASE_PATH, "ALICE.mp3")
if os.path.exists(music_path):
    try:
        pygame.mixer.music.load(music_path)
        pygame.mixer.music.set_volume(1.0)
        pygame.mixer.music.play(-1, 0.0)
    except pygame.error:
        print(f"Could not load music file: {music_path}")

# Load the background image with error handling
try:
    background_image_path = os.path.join(BASE_PATH, "2048.jpg")
    BACKGROUND_IMAGE = pygame.image.load(background_image_path)
    BACKGROUND_IMAGE = pygame.transform.scale(BACKGROUND_IMAGE, (WIDTH, HEIGHT))
except (pygame.error, FileNotFoundError):
    print(f"Could not load background image: {background_image_path}")
    # Create a fallback background surface
    BACKGROUND_IMAGE = pygame.Surface((WIDTH, HEIGHT))
    BACKGROUND_IMAGE.fill(BACKGROUND_COLOR)

class Tile:
    COLORS = [
        (237, 229, 218),
        (238, 225, 201),
        (243, 178, 122),
        (246, 150, 101),
        (247, 124, 95),
        (247, 95, 59),
        (237, 208, 115),
        (237, 204, 99),
        (236, 202, 80),
    ]

    def __init__(self, value, row, col):
        self.value = value
        self.row = row
        self.col = col
        self.x = col * RECT_WIDTH
        self.y = row * RECT_HEIGHT

    def get_color(self):
        color_index = int(math.log2(self.value)) - 1
        color = self.COLORS[color_index]
        return color

    def draw(self, window):
        color = self.get_color()
        pygame.draw.rect(window, color, (self.x, self.y, RECT_WIDTH, RECT_HEIGHT))

        text = FONT.render(str(self.value), 1, FONT_COLOR)
        window.blit(
            text,
            (
                self.x + (RECT_WIDTH / 2 - text.get_width() / 2),
                self.y + (RECT_HEIGHT / 2 - text.get_height() / 2),
            ),
        )

    def set_pos(self, ceil=False):
        if ceil:
            self.row = math.ceil(self.y / RECT_HEIGHT)
            self.col = math.ceil(self.x / RECT_WIDTH)
        else:
            self.row = math.floor(self.y / RECT_HEIGHT)
            self.col = math.floor(self.x / RECT_WIDTH)

    def move(self, delta):
        self.x += delta[0]
        self.y += delta[1]


def draw_grid(window):
    for row in range(1, ROWS):
        y = row * RECT_HEIGHT
        pygame.draw.line(window, OUTLINE_COLOR, (0, y), (WIDTH, y), OUTLINE_THICKNESS)

    for col in range(1, COLS):
        x = col * RECT_WIDTH
        pygame.draw.line(window, OUTLINE_COLOR, (x, 0), (x, HEIGHT), OUTLINE_THICKNESS)

    pygame.draw.rect(window, OUTLINE_COLOR, (0, 0, WIDTH, HEIGHT), OUTLINE_THICKNESS)


def draw(window, tiles):
    window.fill(BACKGROUND_COLOR)

    for tile in tiles.values():
        tile.draw(window)

    draw_grid(window)

    pygame.display.update()


def get_random_pos(tiles):
    row = None
    col = None
    while True:
        row = random.randrange(0, ROWS)
        col = random.randrange(0, COLS)

        if f"{row}{col}" not in tiles:
            break

    return row, col


def move_tiles(window, tiles, clock, direction, game_mode):
    """
    Processes the movement of tiles and merges them based on the direction and game mode.
    """
    updated = True
    blocks = set()

    if direction == "left":
        sort_func = lambda x: x.col
        reverse = False
        delta = (-MOVE_VEL, 0)
        boundary_check = lambda tile: tile.col == 0
        get_next_tile = lambda tile: tiles.get(f"{tile.row}{tile.col - 1}")
        merge_check = lambda tile, next_tile: tile.x > next_tile.x + MOVE_VEL
        move_check = lambda tile, next_tile: tile.x > next_tile.x + RECT_WIDTH + MOVE_VEL
        ceil = True
    elif direction == "right":
        sort_func = lambda x: x.col
        reverse = True
        delta = (MOVE_VEL, 0)
        boundary_check = lambda tile: tile.col == COLS - 1
        get_next_tile = lambda tile: tiles.get(f"{tile.row}{tile.col + 1}")
        merge_check = lambda tile, next_tile: tile.x < next_tile.x - MOVE_VEL
        move_check = lambda tile, next_tile: tile.x + RECT_WIDTH + MOVE_VEL < next_tile.x
        ceil = False
    elif direction == "up":
        sort_func = lambda x: x.row
        reverse = False
        delta = (0, -MOVE_VEL)
        boundary_check = lambda tile: tile.row == 0
        get_next_tile = lambda tile: tiles.get(f"{tile.row - 1}{tile.col}")
        merge_check = lambda tile, next_tile: tile.y > next_tile.y + MOVE_VEL
        move_check = lambda tile, next_tile: tile.y > next_tile.y + RECT_HEIGHT + MOVE_VEL
        ceil = True
    elif direction == "down":
        sort_func = lambda x: x.row
        reverse = True
        delta = (0, MOVE_VEL)
        boundary_check = lambda tile: tile.row == ROWS - 1
        get_next_tile = lambda tile: tiles.get(f"{tile.row + 1}{tile.col}")
        merge_check = lambda tile, next_tile: tile.y < next_tile.y - MOVE_VEL
        move_check = lambda tile, next_tile: tile.y + RECT_HEIGHT + MOVE_VEL < next_tile.y
        ceil = False

    while updated:
        clock.tick(FPS)
        updated = False
        sorted_tiles = sorted(tiles.values(), key=sort_func, reverse=reverse)

        for i, tile in enumerate(sorted_tiles):
            if boundary_check(tile):
                continue

            next_tile = get_next_tile(tile)
            if not next_tile:
                tile.move(delta)
            elif (
                tile.value == next_tile.value
                and tile not in blocks
                and next_tile not in blocks
            ):
                if merge_check(tile, next_tile):
                    tile.move(delta)
                else:
                    next_tile.value *= 2
                    sorted_tiles.pop(i)
                    blocks.add(next_tile)
            elif move_check(tile, next_tile):
                tile.move(delta)
            else:
                continue

            tile.set_pos(ceil)
            updated = True

        update_tiles(window, tiles, sorted_tiles)

    return end_move(tiles, game_mode)

def end_move(tiles, game_mode):
    """
    Adds a new tile after each move based on the game mode.
    """
    if len(tiles) == 16:
        return "lost"

    row, col = get_random_pos(tiles)
    if game_mode == 2048:
        tiles[f"{row}{col}"] = Tile(random.choice([2, 4]), row, col)
    elif game_mode == 3072:
        tiles[f"{row}{col}"] = Tile(random.choice([3, 6]), row, col)  # Always add 3 or 6
    return "continue"


def update_tiles(window, tiles, sorted_tiles):
    tiles.clear()
    for tile in sorted_tiles:
        tiles[f"{tile.row}{tile.col}"] = tile

    draw(window, tiles)


def generate_tiles(game_mode):
    """
    Generates the initial tiles for the game based on the selected game mode.
    """
    tiles = {}
    for _ in range(2):  # Generate 2 tiles at the start
        row, col = get_random_pos(tiles)
        if game_mode == 2048:
            tiles[f"{row}{col}"] = Tile(random.choice([2, 4]), row, col)
        elif game_mode == 3072:
            tiles[f"{row}{col}"] = Tile(random.choice([3, 6]), row, col)  # Always start with 3 or 6
    return tiles

def show_start_screen(window):
    window.fill(BACKGROUND_COLOR)

    # Define the button sizes
    button_width = WIDTH // 2
    button_height = 50

    # Define the button positions
    button_2048 = pygame.Rect(WIDTH // 4, HEIGHT // 2 - 50, button_width, button_height)
    button_3072 = pygame.Rect(WIDTH // 4, HEIGHT // 2 + 20, button_width, button_height)

    # Draw the buttons
    pygame.draw.rect(window, (187, 173, 160), button_2048)
    pygame.draw.rect(window, (187, 173, 160), button_3072)

    # Text for the buttons
    small_font = pygame.font.SysFont("comicsans", 30, bold=True)
    text_2048 = small_font.render("2048", True, FONT_COLOR)
    text_3072 = small_font.render("3072", True, FONT_COLOR)

    # Draw the text in the center of the buttons
    window.blit(
        text_2048,
        (button_2048.centerx - text_2048.get_width() / 2, button_2048.centery - text_2048.get_height() / 2)
    )
    window.blit(
        text_3072,
        (button_3072.centerx - text_3072.get_width() / 2, button_3072.centery - text_3072.get_height() / 2)
    )

    pygame.display.update()

    # Wait for user click on one of the buttons
    selected_mode = None
    while selected_mode is None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return None

            if event.type == pygame.MOUSEBUTTONDOWN:
                # Check if mouse click is within button bounds
                if button_2048.collidepoint(event.pos):
                    selected_mode = [2, 4]  # Select 2048 mode (2 and 4)
                elif button_3072.collidepoint(event.pos):
                    selected_mode = [3, 6]  # Select 3072 mode (3 and 6)

    return selected_mode

def show_start_screen(window):
    """
    Displays the start screen with a "Start" button. Clicking "Start" reveals the game mode options.
    """
    window.fill(BACKGROUND_COLOR)

    # Position "Tile Twister" at the top
    title_text = FONT.render("Tile Twister", True, FONT_COLOR)
    title_x = WIDTH / 2 - title_text.get_width() / 2
    title_y = 50  # Position the title near the top
    window.blit(title_text, (title_x, title_y))

    # Create a smaller font for the subtitle
    subtitle_font = pygame.font.SysFont("comicsans", 20, bold=False)
    subtitle_text = subtitle_font.render("Select a game mode to start", True, FONT_COLOR)
    subtitle_x = WIDTH / 2 - subtitle_text.get_width() / 2
    subtitle_y = title_y + title_text.get_height() + 10  # Add padding below the title
    window.blit(subtitle_text, (subtitle_x, subtitle_y))

    # Button dimensions
    button_width = 200
    button_height = 50

    # "Start" button
    start_button = pygame.Rect(WIDTH / 2 - button_width / 2, HEIGHT / 2 - button_height / 2, button_width, button_height)
    pygame.draw.rect(window, (187, 173, 160), start_button)

    # Text for the "Start" button
    small_font = pygame.font.SysFont("comicsans", 30, bold=True)
    start_text = small_font.render("Start", True, FONT_COLOR)
    window.blit(
        start_text,
        (start_button.centerx - start_text.get_width() / 2, start_button.centery - start_text.get_height() / 2),
    )

    pygame.display.update()

    # Wait for the user to click "Start"
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return None

            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_button.collidepoint(event.pos):
                    # Show game mode buttons
                    return show_game_over_window(window)
                
def show_start_screen(window):
    """
    Displays the start screen with a single "Start" button. Upon clicking, it shows the game mode selection buttons.
    """
    while True:
        # Draw the background image
        window.blit(BACKGROUND_IMAGE, (0, 0))

        # "Tile Twister" title
        title_text = FONT.render("Tile Twister", True, FONT_COLOR)
        title_x = WIDTH / 2 - title_text.get_width() / 2
        title_y = HEIGHT / 4  # Position title near the top
        window.blit(title_text, (title_x, title_y))

        # Start Button
        button_width = WIDTH // 3
        button_height = 60
        start_button = pygame.Rect(
            WIDTH / 2 - button_width / 2, HEIGHT / 2, button_width, button_height
        )

        pygame.draw.rect(window, (187, 173, 160), start_button)
        small_font = pygame.font.SysFont("comicsans", 25, bold=True)
        start_text = small_font.render("Start", True, FONT_COLOR)
        window.blit(
            start_text,
            (
                start_button.centerx - start_text.get_width() / 2,
                start_button.centery - start_text.get_height() / 2,
            ),
        )

        # Exit Button (Added)
        button_exit = pygame.Rect(
            WIDTH / 2 - button_width / 2, HEIGHT / 2 + 80, button_width, button_height
        )
        pygame.draw.rect(window, (187, 173, 160), button_exit)
        exit_text = small_font.render("Exit", True, FONT_COLOR)
        window.blit(
            exit_text,
            (
                button_exit.centerx - exit_text.get_width() / 2,
                button_exit.centery - exit_text.get_height() / 2,
            ),
        )

        pygame.display.update()

        # Wait for user click on the "Start" button or "Exit" button
        start_clicked = False
        while not start_clicked:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return None

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if start_button.collidepoint(event.pos):
                        start_clicked = True
                    elif button_exit.collidepoint(event.pos):
                        pygame.quit()
                        return None

        # Clear the screen for mode selection
        window.blit(BACKGROUND_IMAGE, (0, 0))

        # Display the "Tile Twister" title and subtitle again
        title_text = FONT.render("Tile Twister", True, FONT_COLOR)
        title_x = WIDTH / 2 - title_text.get_width() / 2
        title_y = HEIGHT / 4  # Position title near the top
        window.blit(title_text, (title_x, title_y))

        # Subtitle for mode selection screen
        subtitle_font = pygame.font.SysFont("comicsans", 30)
        subtitle_text = subtitle_font.render("Select the game mode", True, FONT_COLOR)
        subtitle_x = WIDTH / 2 - subtitle_text.get_width() / 2
        subtitle_y = title_y + title_text.get_height() + 10
        window.blit(subtitle_text, (subtitle_x, subtitle_y))

        # Display the mode selection buttons
        button_width = 200
        button_height = 60

        # Adjust the positioning to reduce the space between the buttons
        button_2048 = pygame.Rect(WIDTH / 2 - button_width / 2, HEIGHT / 2 + 50, button_width, button_height)
        button_3072 = pygame.Rect(WIDTH / 2 - button_width / 2, HEIGHT / 2 + 120, button_width, button_height)  # Reduced space here

        pygame.draw.rect(window, (187, 173, 160), button_2048)
        pygame.draw.rect(window, (187, 173, 160), button_3072)

        text_2048 = small_font.render("Play 2048", True, FONT_COLOR)
        text_3072 = small_font.render("Play 3072", True, FONT_COLOR)

        window.blit(
            text_2048,
            (
                button_2048.centerx - text_2048.get_width() / 2,
                button_2048.centery - text_2048.get_height() / 2,
            ),
        )
        window.blit(
            text_3072,
            (
                button_3072.centerx - text_3072.get_width() / 2,
                button_3072.centery - text_3072.get_height() / 2,
            ),
        )

        pygame.display.update()

        # Wait for user selection or exit
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return None

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if button_2048.collidepoint(event.pos):
                        return 2048
                    if button_3072.collidepoint(event.pos):
                        return 3072
def show_game_over_window(window):
    """
    Displays the Game Over screen with Retry, Exit, and Home options.
    """
    window.blit(BACKGROUND_IMAGE, (0, 0))

    # Game Over Text
    game_over_text = FONT.render("Game Over!", True, FONT_COLOR)

    # Button dimensions
    button_width = WIDTH // 4
    button_height = 50

    # Define buttons
    retry_button = pygame.Rect(WIDTH // 2 - button_width // 2, HEIGHT // 2 - 80, button_width, button_height)
    home_button = pygame.Rect(WIDTH // 2 - button_width // 2, HEIGHT // 2, button_width, button_height)
    exit_button = pygame.Rect(WIDTH // 2 - button_width // 2, HEIGHT // 2 + 80, button_width, button_height)

    # Draw buttons
    pygame.draw.rect(window, (187, 173, 160), retry_button)
    pygame.draw.rect(window, (187, 173, 160), home_button)
    pygame.draw.rect(window, (187, 173, 160), exit_button)

    # Button labels
    small_font = pygame.font.SysFont("comicsans", 15, bold=True)
    retry_text = small_font.render("Retry", True, FONT_COLOR)
    home_text = small_font.render("Home", True, FONT_COLOR)
    exit_text = small_font.render("Exit", True, FONT_COLOR)

    # Adjust the position of the "Game Over" text higher
    game_over_text_y = retry_button.top - game_over_text.get_height() - 40  # Move higher by setting more negative value

    # Draw the "Game Over" text
    window.blit(game_over_text, (WIDTH / 2 - game_over_text.get_width() / 2, game_over_text_y))

    # Draw labels on buttons
    window.blit(retry_text, (retry_button.centerx - retry_text.get_width() / 2, retry_button.centery - retry_text.get_height() / 2))
    window.blit(home_text, (home_button.centerx - home_text.get_width() / 2, home_button.centery - home_text.get_height() / 2))
    window.blit(exit_text, (exit_button.centerx - exit_text.get_width() / 2, exit_button.centery - exit_text.get_height() / 2))

    pygame.display.update()

    # Wait for User Input
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return "exit"

            if event.type == pygame.MOUSEBUTTONDOWN:
                if retry_button.collidepoint(event.pos):
                    return "retry"
                if home_button.collidepoint(event.pos):
                    return "home"
                if exit_button.collidepoint(event.pos):
                    return "exit"

def main(window):
    clock = pygame.time.Clock()
    run = True

    while run:
        # Show the start screen and get the selected game mode
        game_mode = show_start_screen(window)
        if not game_mode:
            return  # Exit if the user closes the window

        # Start a new game session
        tiles = generate_tiles(game_mode)

        while run:
            clock.tick(FPS)
            status = "continue"

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    break

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        status = move_tiles(window, tiles, clock, "left", game_mode)
                    if event.key == pygame.K_RIGHT:
                        status = move_tiles(window, tiles, clock, "right", game_mode)
                    if event.key == pygame.K_UP:
                        status = move_tiles(window, tiles, clock, "up", game_mode)
                    if event.key == pygame.K_DOWN:
                        status = move_tiles(window, tiles, clock, "down", game_mode)

            draw(window, tiles)

            if status == "lost":
                choice = show_game_over_window(window)
                if choice == "retry":
                    break  # Restart the game with the same game mode
                elif choice == "home":
                    # Go back to the start screen
                    break  # Exit the current game loop to show start screen again
                elif choice == "exit":
                    run = False  # Exit the application
                    break

    pygame.quit()



if __name__ == "__main__":
    main(WINDOW) 