import pygame
import random
import os
pygame.init()

screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Fruits Basket")

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

catcher_width = 150
catcher_height = 120
catcher_x = screen_width // 2 - catcher_width // 2
catcher_y = screen_height - catcher_height - 20
catcher_speed = 10

fruit_width = 85
fruit_height = 85
fruit_speed = 5

score = 0
lives = 3

clock = pygame.time.Clock()
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Improved music loading with error handling
def load_music(filename):
    try:
        music_path = os.path.join(BASE_DIR, filename)
        if os.path.exists(music_path):
            pygame.mixer.music.load(music_path)
            print(f"Loaded music from {music_path}")
        else:
            print(f"Music file not found: {music_path}")
            # Optionally, you can comment out the music loading or use a fallback
    except pygame.error as e:
        print(f"Error loading music: {e}")

# Initial music load (you can modify the filename as needed)
load_music("a.mp3")  # Replace with your actual music file name

catcher_image = pygame.image.load(os.path.join(BASE_DIR, "basket.png"))
catcher_image = pygame.transform.scale(catcher_image, (catcher_width, catcher_height))

fruit_images = [
    pygame.image.load(os.path.join(BASE_DIR, "01.png")),
    pygame.image.load(os.path.join(BASE_DIR, "03.png")),
    pygame.image.load(os.path.join(BASE_DIR, "05.png")),
    pygame.image.load(os.path.join(BASE_DIR, "11.png")),
    pygame.image.load(os.path.join(BASE_DIR, "08.png"))
]

non_fruit_images = [
    pygame.image.load(os.path.join(BASE_DIR, "22_cheesecake.png")),
    pygame.image.load(os.path.join(BASE_DIR, "46_fruitcake.png")),
    pygame.image.load(os.path.join(BASE_DIR, "73_omlet.png")),
    pygame.image.load(os.path.join(BASE_DIR, "81_pizza.png"))
]

fruit_catch_sound = pygame.mixer.Sound(os.path.join(BASE_DIR, "sound5.wav"))
non_fruit_sound = pygame.mixer.Sound(os.path.join(BASE_DIR, "sound4.wav"))

font_path = os.path.join(BASE_DIR, "Super Shiny.ttf")
score_lives_font_path = os.path.join(BASE_DIR, "sprout.ttf")

# Scale background images to match screen size
menu_background = pygame.transform.scale(pygame.image.load(os.path.join(BASE_DIR, "menu.jpg")), (screen_width, screen_height))
game_background = pygame.transform.scale(pygame.image.load(os.path.join(BASE_DIR, "bg3.jpg")), (screen_width, screen_height))
gameover_background = pygame.transform.scale(pygame.image.load(os.path.join(BASE_DIR, "gobg.jpg")), (screen_width, screen_height))

def draw_catcher(x, y):
    screen.blit(catcher_image, (x, y))

def draw_fruit(fruit_img, x, y):
    scaled_fruit = pygame.transform.scale(fruit_img, (fruit_width, fruit_height))
    screen.blit(scaled_fruit, (x, y))

def display_score_and_lives(score, lives):
    # Use score_lives_font with appropriate error handling
    score_lives_font = pygame.font.Font(score_lives_font_path, 36)
    
    try:
        label_score_text = score_lives_font.render("Score: ", True, BLACK)
        label_lives_text = score_lives_font.render("Lives: ", True, BLACK)
        score_text = score_lives_font.render(str(score), True, (255, 105, 180))
        lives_text = score_lives_font.render(str(lives), True, (255, 105, 180))
    except Exception as e:
        # Fallback to default system font if custom font fails
        print(f"Error loading custom font: {e}")
        score_lives_font = pygame.font.Font(None, 36)  # Use default system font
    
    # Re-render with fallback font
    label_score_text = score_lives_font.render("Score: ", True, BLACK)
    label_lives_text = score_lives_font.render("Lives: ", True, BLACK)
    score_text = score_lives_font.render(str(score), True, (255, 105, 180))
    lives_text = score_lives_font.render(str(lives), True, (255, 105, 180))

    screen.blit(label_score_text, (10, 10))
    screen.blit(label_lives_text, (10, 40))
    screen.blit(score_text, (label_score_text.get_width() + 10, 10))
    screen.blit(lives_text, (label_lives_text.get_width() + 10, 40))

def display_game_over(score):
    screen.blit(gameover_background, (0, 0))
    game_over_font = pygame.font.Font(font_path, 100)
    game_over_text = game_over_font.render("GAME OVER", True, (255, 0, 0))
    final_score_text = pygame.font.Font(font_path, 60).render(f"YOUR SCORE: {score}", True, BLACK)
    replay_text = pygame.font.Font(font_path, 26).render("P = PLAY AGAIN", True, (0, 255, 0))
    menu_text = pygame.font.Font(font_path, 26).render("M = MAIN MENU", True, (0, 128, 255))
    exit_text = pygame.font.Font(font_path, 26).render("G = EXIT", True, (255, 0, 0))
    total_width = replay_text.get_width() + menu_text.get_width() + exit_text.get_width() + 40  
    start_x = (screen_width - total_width) // 2
    option_y = screen_height // 1.5  
    
    screen.blit(game_over_text, ((screen_width - game_over_text.get_width()) // 2, screen_height // 3.5))
    screen.blit(final_score_text, ((screen_width - final_score_text.get_width()) // 2, screen_height // 2.56 + 50))
    screen.blit(replay_text, (start_x, option_y))  
    screen.blit(menu_text, (start_x + replay_text.get_width() + 10, option_y))
    screen.blit(exit_text, (start_x + replay_text.get_width() + menu_text.get_width() + 25, option_y))  

    pygame.display.update()

def handle_game_over(score):
    while True:
        display_game_over(score)  
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return "exit"
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_g:  
                    pygame.quit()
                    exit()
                if event.key == pygame.K_p:  
                    return "replay"
                if event.key == pygame.K_m: 
                    return "menu" 

def show_menu():
    menu_running = True
    title_font = pygame.font.Font(font_path, 70)
    title_text = title_font.render("Fruits Basket", True, (194, 163, 215))
    start_text = pygame.font.Font(font_path, 50).render("Press 'P' to Start", True, BLACK)

    while menu_running:
        screen.blit(menu_background, (0, 0))  
        screen.blit(title_text, ((screen_width - title_text.get_width()) // 2, screen_height // 3))
        screen.blit(start_text, ((screen_width - start_text.get_width()) // 2, screen_height // 2 + 50))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:  
                    menu_running = False
                    game_loop()  
                if event.key == pygame.K_m: 
                    pass

def screen_shake(intensity, duration):
    return [(random.randint(-intensity, intensity), random.randint(-intensity, intensity)) for _ in range(duration)]

def game_loop():
    global score, catcher_x, lives, fruit_speed

    score = 0
    lives = 3
    catcher_x = screen_width // 2 - catcher_width // 2
    fruit_speed = 5

    try:
        pygame.mixer.music.stop()
        pygame.mixer.music.load(os.path.join(BASE_DIR, "kirby.mp3"))
        pygame.mixer.music.play(-1)
    except pygame.error as e:
        print(f"Error loading music: {e}")
        # Optionally, you can skip music loading or use a fallback
        print("Music could not be loaded. Continuing without background music.")

    fruit_x = random.randint(0, screen_width - fruit_width)
    fruit_y = -fruit_height
    all_items = fruit_images + non_fruit_images
    current_item = random.choice(all_items)

    next_speed_increase_score = 6
    running = True
    shake_offsets = None

    while running:
        offset_x, offset_y = (0, 0) if not shake_offsets else shake_offsets.pop(0)
        if not shake_offsets:
            shake_offsets = None  

        screen.blit(game_background, (0, 0))  

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            catcher_x -= catcher_speed
        if keys[pygame.K_RIGHT]:
            catcher_x += catcher_speed
        if catcher_x < 0:
            catcher_x = 0
        elif catcher_x > screen_width - catcher_width:
            catcher_x = screen_width - catcher_width

        if score >= next_speed_increase_score:
            fruit_speed += 1
            next_speed_increase_score += 6

        fruit_y += fruit_speed

        if fruit_y + fruit_height > catcher_y and catcher_x < fruit_x + fruit_width < catcher_x + catcher_width:
            if current_item in fruit_images:
                score += 1
                fruit_catch_sound.play()
            elif current_item in non_fruit_images:
                lives = max(0, lives - 1)
                non_fruit_sound.play()
                shake_offsets = screen_shake(15, 30)  
            fruit_x = random.randint(0, screen_width - fruit_width)
            fruit_y = -fruit_height
            current_item = random.choice(all_items)

        if fruit_y > screen_height:
            if current_item in fruit_images:
                lives = max(0, lives - 1)
                non_fruit_sound.play()
                shake_offsets = screen_shake(10, 20)  
            fruit_x = random.randint(0, screen_width - fruit_width)
            fruit_y = -fruit_height
            current_item = random.choice(all_items)

        if lives == 0:
            pygame.mixer.music.stop()
            choice = handle_game_over(score) 
            if choice == "exit":
                return
            elif choice == "replay":
                game_loop()  
            elif choice == "menu":
                show_menu()  
                
        screen.blit(catcher_image, (catcher_x + offset_x, catcher_y + offset_y))
        draw_fruit(current_item, fruit_x + offset_x, fruit_y + offset_y)
        display_score_and_lives(score, lives)

        pygame.display.update()
        clock.tick(60)

show_menu()
game_loop()
pygame.quit()