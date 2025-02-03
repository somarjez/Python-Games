import pygame
import random
import sys
import time
import os
from pygame.math import Vector2

pygame.init()

script_dir = os.path.dirname(os.path.abspath(__file__))
font_path = os.path.join(script_dir, "assets", "fonts", "GRAND9K PIXEL.TTF")

white = (255, 255, 255)
yellow = (255, 255, 102)
black = (0, 0, 0)
red = (213, 50, 80)
green = (0, 255, 0)
blue = (50, 153, 213)
pink = (255, 105, 180)
dark_green = (0, 100, 0)
light_gray = (200, 200, 200)
dark_gray = (100, 100, 100)
grass1 = (181, 229, 80)
grass2 = (144, 224, 72)

# Set display dimensions
dis_width = 800
dis_height = 600

# Initialize display
dis = pygame.display.set_mode((dis_width, dis_height))
pygame.display.set_caption('sneik for snakes')

clock = pygame.time.Clock()
snake_block = 30  # Increased size of the snake block
initial_snake_speed =  10# Initial snake speed

font_style = pygame.font.Font(font_path, 25)
score_font = pygame.font.Font(font_path, 25) # Smaller font size for score

high_score = 0  # Initialize high score variable

current_snake_color = pink
full_screen = False  # Track full-screen state

menu_background = pygame.image.load(os.path.join(script_dir, 'assets', 'images', 'game_menu.jpg')).convert()
menu_background = pygame.transform.scale(menu_background, (dis_width, dis_height))

game_over_screen_background = pygame.image.load(os.path.join(script_dir, 'assets', 'images', 'game_over.jpg')).convert()
game_over_screen_background = pygame.transform.scale(game_over_screen_background, (dis_width, dis_height))

you_lost_background = pygame.image.load(os.path.join(script_dir, 'assets', 'images', 'you_lost.jpg')).convert()
you_lost_background = pygame.transform.scale(you_lost_background, (dis_width, dis_height))

pause_menu_background = pygame.image.load(os.path.join(script_dir, 'assets', 'images', 'pause_menu.jpg')).convert()
pause_menu_background = pygame.transform.scale(pause_menu_background, (dis_width, dis_height))

def toggle_full_screen():
    global full_screen, dis
    if full_screen:
        dis = pygame.display.set_mode((dis_width, dis_height))
        full_screen = False
    else:
        dis = pygame.display.set_mode((dis_width, dis_height), pygame.FULLSCREEN)
        full_screen = True

def draw_background(color1, color2, opacity):
    color2_surface = pygame.Surface((snake_block, snake_block))
    color2_surface.fill(color2)
    # color2_surface.set_alpha(opacity)

    # Draw the background in a grid pattern using both colors
    for y in range(0, dis_height, snake_block):
        for x in range(0, dis_width, snake_block):
            if (x // snake_block + y // snake_block) % 2 == 0:
                pygame.draw.rect(dis, color1, [x, y, snake_block, snake_block])
            else:
                dis.blit(color2_surface, (x, y))

# class SNAKE:
#     def __init__(self):
#         # self.body = [Vector2(5, 10), Vector2(4, 10), Vector2(3, 10)]
#         self.body = [Vector2(100, 50)]  # Snake starts at position (100, 50)
#         self.direction = Vector2(1, 0)
#         self.new_block = False

#         self.head_up = pygame.image.load(os.path.join(script_dir, 'assets', 'graphics', 'head_up.png')).convert_alpha()
#         self.head_down = pygame.image.load(os.path.join(script_dir, 'assets', 'graphics', 'head_down.png')).convert_alpha()
#         self.head_right = pygame.image.load(os.path.join(script_dir, 'assets', 'graphics', 'head_right.png')).convert_alpha()
#         self.head_left = pygame.image.load(os.path.join(script_dir, 'assets', 'graphics', 'head_left.png')).convert_alpha()

#         self.tail_up = pygame.image.load(os.path.join(script_dir, 'assets', 'graphics', 'tail_up.png')).convert_alpha()
#         self.tail_down = pygame.image.load(os.path.join(script_dir, 'assets', 'graphics', 'tail_down.png')).convert_alpha()
#         self.tail_right = pygame.image.load(os.path.join(script_dir, 'assets', 'graphics', 'tail_right.png')).convert_alpha()
#         self.tail_left = pygame.image.load(os.path.join(script_dir, 'assets', 'graphics', 'tail_left.png')).convert_alpha()

#         self.body_vertical = pygame.image.load(os.path.join(script_dir, 'assets', 'graphics', 'body_vertical.png')).convert_alpha()
#         self.body_horizontal = pygame.image.load(os.path.join(script_dir, 'assets', 'graphics', 'body_horizontal.png')).convert_alpha()

#         self.body_tr = pygame.image.load(os.path.join(script_dir, 'assets', 'graphics', 'body_tr.png')).convert_alpha()
#         self.body_tl = pygame.image.load(os.path.join(script_dir, 'assets', 'graphics', 'body_tl.png')).convert_alpha()
#         self.body_br = pygame.image.load(os.path.join(script_dir, 'assets', 'graphics', 'body_br.png')).convert_alpha()
#         self.body_bl = pygame.image.load(os.path.join(script_dir, 'assets', 'graphics', 'body_bl.png')).convert_alpha()

#     # def draw_snake(self):
#     #     for index, block in enumerate(self.body):
#     #         x_pos = int(block.x * snake_block)
#     #         y_pos = int(block.y * snake_block)
#     #         block_rect = pygame.Rect(x_pos, y_pos, snake_block, snake_block)

#     #         if index == 0:
#     #             if self.direction == Vector2(0, -1):
#     #                 dis.blit(self.head_up, block_rect)
#     #             elif self.direction == Vector2(0, 1):
#     #                 dis.blit(self.head_down, block_rect)
#     #             elif self.direction == Vector2(1, 0):
#     #                 dis.blit(self.head_right, block_rect)
#     #             elif self.direction == Vector2(-1, 0):
#     #                 dis.blit(self.head_left, block_rect)
#     #         elif index == len(self.body) - 1:
#     #             tail_relation = self.body[-2] - self.body[-1]
#     #             if tail_relation == Vector2(0, -1):
#     #                 dis.blit(self.tail_up, block_rect)
#     #             elif tail_relation == Vector2(0, 1):
#     #                 dis.blit(self.tail_down, block_rect)
#     #             elif tail_relation == Vector2(1, 0):
#     #                 dis.blit(self.tail_right, block_rect)
#     #             elif tail_relation == Vector2(-1, 0):
#     #                 dis.blit(self.tail_left, block_rect)
#     #         else:
#     #             previous_block = self.body[index + 1] - block
#     #             next_block = self.body[index - 1] - block
#     #             if previous_block.x == next_block.x:
#     #                 dis.blit(self.body_vertical, block_rect)
#     #             elif previous_block.y == next_block.y:
#     #                 dis.blit(self.body_horizontal, block_rect)
#     #             else:
#     #                 if previous_block.x == -1 and next_block.y == -1 or previous_block.y == -1 and next_block.x == -1:
#     #                     dis.blit(self.body_tl, block_rect)
#     #                 elif previous_block.y == 1 and next_block.x == -1 or previous_block.x == -1 and next_block.y == 1:
#     #                     dis.blit(self.body_bl, block_rect)
#     #                 elif previous_block.y == -1 and next_block.x == 1 or previous_block.x == 1 and next_block.y == -1:
#     #                     dis.blit(self.body_tr, block_rect)
#     #                 elif previous_block.x == 1 and next_block.y == 1 or previous_block.y == 1 and next_block.x == 1:
#     #                     dis.blit(self.body_br, block_rect)

#     def draw_snake(self):
#         for index, block in enumerate(self.body):
#             # Convert grid positions to pixel positions
#             x_pos = int(block.x)  # If block.x and block.y are already in pixel coordinates, no need to multiply by snake_block
#             y_pos = int(block.y)

#             block_rect = pygame.Rect(x_pos, y_pos, snake_block, snake_block)

#             # Drawing the head
#             if index == 0:  # Head
#                 if self.direction == Vector2(0, -1):  # Moving Up
#                     dis.blit(self.head_up, block_rect)
#                 elif self.direction == Vector2(0, 1):  # Moving Down
#                     dis.blit(self.head_down, block_rect)
#                 elif self.direction == Vector2(1, 0):  # Moving Right
#                     dis.blit(self.head_right, block_rect)
#                 elif self.direction == Vector2(-1, 0):  # Moving Left
#                     dis.blit(self.head_left, block_rect)

#             # Drawing the tail
#             elif index == len(self.body) - 1:  # Tail
#                 tail_relation = self.body[-2] - self.body[-1]  # The difference between last and second last segment
#                 if tail_relation == Vector2(0, -1):  # Tail facing up
#                     dis.blit(self.tail_up, block_rect)
#                 elif tail_relation == Vector2(0, 1):  # Tail facing down
#                     dis.blit(self.tail_down, block_rect)
#                 elif tail_relation == Vector2(1, 0):  # Tail facing right
#                     dis.blit(self.tail_right, block_rect)
#                 elif tail_relation == Vector2(-1, 0):  # Tail facing left
#                     dis.blit(self.tail_left, block_rect)

#             # Drawing the body
#             else:  # Body segments
#                 previous_block = self.body[index + 1] - block
#                 next_block = self.body[index - 1] - block
#                 if previous_block.x == next_block.x:  # Vertical body segment
#                     dis.blit(self.body_vertical, block_rect)
#                 elif previous_block.y == next_block.y:  # Horizontal body segment
#                     dis.blit(self.body_horizontal, block_rect)
#                 else:
#                     if previous_block.x == -1 and next_block.y == -1 or previous_block.y == -1 and next_block.x == -1:
#                         dis.blit(self.body_tl, block_rect)  # Top-left corner of body
#                     elif previous_block.y == 1 and next_block.x == -1 or previous_block.x == -1 and next_block.y == 1:
#                         dis.blit(self.body_bl, block_rect)  # Bottom-left corner of body
#                     elif previous_block.y == -1 and next_block.x == 1 or previous_block.x == 1 and next_block.y == -1:
#                         dis.blit(self.body_tr, block_rect)  # Top-right corner of body
#                     elif previous_block.x == 1 and next_block.y == 1 or previous_block.y == 1 and next_block.x == 1:
#                         dis.blit(self.body_br, block_rect)  # Bottom-right corner of body

class FRUIT:
    def __init__(self):
        self.image = pygame.image.load(os.path.join(script_dir, 'assets', 'graphics', 'apple.png')).convert_alpha()
        self.randomize_position()

    def randomize_position(self):
        self.position = Vector2(random.randint(0, (dis_width // snake_block) - 1), random.randint(0, (dis_height // snake_block) - 1))
        # self.position = Vector2(random.randrange(0, dis_width) * snake_block, random.randrange(0, dis_height) * snake_block)

    def draw_fruit(self):
        fruit_rect = pygame.Rect(int(self.position.x * snake_block), int(self.position.y * snake_block), snake_block, snake_block)
        dis.blit(self.image, fruit_rect)

def our_snake(snake_block, snake_list):
    for x in snake_list:
        pygame.draw.rect(dis, current_snake_color, [x[0], x[1], snake_block, snake_block])

def message(msg, color, y_displace=0, center=False):
    mesg = font_style.render(msg, True, color)
    if center:
        text_rect = mesg.get_rect(center=(dis_width / 2, dis_height / 2 + y_displace))
        dis.blit(mesg, text_rect)
    else:
        dis.blit(mesg, [dis_width / 6, dis_height / 3 + y_displace])

def your_score(score, high_score, level):
    # Render the score, high score, and level
    value = score_font.render("Score: " + str(score), True, black)
    high_score_value = score_font.render("High Score: " + str(high_score), True, black)
    level_value = score_font.render("Level: " + str(level + 1), True, black)

    # dis.blit(value, [10, 10])  # Position the score at the top-left corner
    # dis.blit(high_score_value, [10, 40])  # Position the high score below the score
    # dis.blit(level_value, [10, 70])  # Position the level below the high score
    
    # Create surfaces for transparency
    value_surface = pygame.Surface(value.get_size(), pygame.SRCALPHA)
    high_score_surface = pygame.Surface(high_score_value.get_size(), pygame.SRCALPHA)
    level_surface = pygame.Surface(level_value.get_size(), pygame.SRCALPHA)
    
    # Blit the text onto the surfaces
    value_surface.blit(value, (0, 0))
    high_score_surface.blit(high_score_value, (0, 0))
    level_surface.blit(level_value, (0, 0))
    
    # Set transparency
    value_surface.set_alpha(150)  # Adjust the alpha value for transparency
    high_score_surface.set_alpha(150)  # Adjust the alpha value for transparency
    level_surface.set_alpha(150)  # Adjust the alpha value for transparency
    
    # Blit the surfaces onto the display
    dis.blit(value_surface, [10, 10])  # Adjusted position
    dis.blit(high_score_surface, [10, 30])  # Adjusted position
    dis.blit(level_surface, [10, 50])  # Adjusted position

def game_over_screen():
    global high_score
    game_over = True
    while game_over:
        dis.blit(game_over_screen_background, (0, 0))
        message("GAME OVER", red, -50, center=True)
        message("Press R to Replay or Q to Quit", white, 50, center=True)
        message(f"High Score: {high_score}", yellow, 100, center=True)  # Display high score on game over screen
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    gameLoop()
                if event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()

def pause_menu():
    paused = True
    while paused:
        dis.blit(pause_menu_background, (0, 0))
        message("Paused", red, -50, center=True)
        message("Press P to Resume or M to Main Menu", black, 50, center=True)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    paused = False
                if event.key == pygame.K_m:
                    gameMenu()
                if event.key == pygame.K_f:
                    toggle_full_screen()

def settings_menu():
    settings = True
    while settings:
        dis.blit(menu_background, (0, 0)) 
            
        message("Settings", red, -150, center=True)  # Move the title further up
              
        # Display instructions with smaller font size
        small_font_style = pygame.font.SysFont("bahnschrift", 20)
        instructions = small_font_style.render("Press M to return to menu", True, black)
        instructions_rect = instructions.get_rect(center=(dis_width / 2, dis_height / 2))
        dis.blit(instructions, instructions_rect)
        
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_m:
                    settings = False
                if event.key == pygame.K_f:
                    toggle_full_screen()

def generate_food():
    return round(random.randrange(0, dis_width - snake_block) / 20.0) * 20.0, round(random.randrange(0, dis_height - snake_block) / 20.0) * 20.0

def gameLoop():
    global high_score  # Ensure high_score can be modified globally

    snake_speed = initial_snake_speed
    level = 0
    score = 0  # Initialize score to 0

    game_over = False
    game_close = False

    # Initialize snake position in the middle of the screen
    x1 = dis_width // 2
    y1 = dis_height // 2
    x1_change = 0
    y1_change = 0

    # Initialize snake body
    Length_of_snake = 5
    snake_List = [[x1 - i * snake_block, y1] for i in range(Length_of_snake)]

    fruit =  FRUIT()

    # Generate food position
    foodx, foody = generate_food()

    print(f"Initial snake position: {snake_List}")
    print(f"Initial food position: ({foodx}, {foody})")

    while not game_over:
        while game_close:
            dis.blit(you_lost_background, (0, 0))
            message("You Lost! Press Q-Quit or C-Play Again", red, center=True)
            message(f"High Score: {high_score}", white, 50, center=True)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        gameLoop()
                        return  # Exit gameLoop and let the main menu handle restart

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and x1_change == 0:
                    x1_change = -snake_block
                    y1_change = 0
                elif event.key == pygame.K_RIGHT and x1_change == 0:
                    x1_change = snake_block
                    y1_change = 0
                elif event.key == pygame.K_UP and y1_change == 0:
                    y1_change = -snake_block
                    x1_change = 0
                elif event.key == pygame.K_DOWN and y1_change == 0:
                    y1_change = snake_block
                    x1_change = 0
                elif event.key == pygame.K_p:
                    pause_menu()
                elif event.key == pygame.K_f:
                    toggle_full_screen()

        # Update snake head position
        x1 += x1_change
        y1 += y1_change

        # Boundary collision check
        if x1 >= dis_width or x1 < 0 or y1 >= dis_height or y1 < 0:
            print("Collision with boundary detected")
            game_close = True

        # Update snake body
        snake_Head = [x1, y1]
        snake_List.append(snake_Head)
        if len(snake_List) > Length_of_snake:
            del snake_List[0]

        # Check for self-collision only after the first movement
        if x1_change != 0 or y1_change != 0:
            if snake_Head in snake_List[:-1]:
                print("Collision with self detected")
                game_close = True

        draw_background(grass1, grass2, 50)  # Draw the background
        # pygame.draw.rect(dis, green, [foodx, foody, snake_block, snake_block])
        fruit.draw_fruit()

        our_snake(snake_block, snake_List)
        your_score(score, high_score, level)

        pygame.display.update()

        # Check if snake eats food
        # if abs(x1 - foodx) < snake_block and abs(y1 - foody) < snake_block:
        #     foodx, foody = generate_food()
        #     Length_of_snake += 1
        #     score += 1
        #     if score % 3 == 0:
        #         level += 1
        #         snake_speed += 5

        if abs(x1 - fruit.position.x * snake_block) < snake_block and abs(y1 - fruit.position.y * snake_block) < snake_block:
            fruit.randomize_position()
            Length_of_snake += 1
            score += 1
            if score % 3 == 0:
                level += 1
                snake_speed += 5

        clock.tick(snake_speed)

    # Update high score if the current score is higher
    if score > high_score:
        high_score = score

    game_over_screen()  # Call the game over screen when the game ends


# def gameLoop():
#     global high_score  # Ensure high_score can be modified globally

#     snake_speed = initial_snake_speed
#     level = 0
#     score = 0  # Initialize score to 0

#     game_over = False
#     game_close = False

#     # x1 = dis_width / 2
#     # y1 = dis_height / 2

#     # x1_change = 0
#     # y1_change = 0

#     snake = SNAKE()  # Initialize the snake object
#     fruit = FRUIT()  # Initialize the fruit object
#     # foodx, foody = generate_food()

#     # Length_of_snake = 1

#     while not game_over:
#         while game_close == True:
#             dis.blit(you_lost_background, (0, 0))
#             message("You Lost! Press Q-Quit or C-Play Again", red, center=True)
#             message(f"High Score: {high_score}", white, 50, center=True)
#             pygame.display.update()

#             for event in pygame.event.get():
#                 if event.type == pygame.KEYDOWN:
#                     if event.key == pygame.K_q:
#                         game_over = True
#                         game_close = False
#                     if event.key == pygame.K_c:
#                         gameLoop()

#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 game_over = True
#             if event.type == pygame.KEYDOWN:
#                 # if event.key == pygame.K_LEFT and x1_change == 0:
#                 #     x1_change = -snake_block
#                 #     y1_change = 0
#                 # elif event.key == pygame.K_RIGHT and x1_change == 0:
#                 #     x1_change = snake_block
#                 #     y1_change = 0
#                 # elif event.key == pygame.K_UP and y1_change == 0:
#                 #     y1_change = -snake_block
#                 #     x1_change = 0
#                 # elif event.key == pygame.K_DOWN and y1_change == 0:
#                 #     y1_change = snake_block
#                 #     x1_change = 0
#                 # elif event.key == pygame.K_p:
#                 #     pause_menu()
#                 # elif event.key == pygame.K_f:
#                 #     toggle_full_screen()

#                 if event.key == pygame.K_LEFT and snake.direction != Vector2(1, 0):  # Prevent 180-degree turn
#                     snake.direction = Vector2(-1, 0)
#                 elif event.key == pygame.K_RIGHT and snake.direction != Vector2(-1, 0):  # Prevent 180-degree turn
#                     snake.direction = Vector2(1, 0)
#                 elif event.key == pygame.K_UP and snake.direction != Vector2(0, 1):  # Prevent 180-degree turn
#                     snake.direction = Vector2(0, -1)
#                 elif event.key == pygame.K_DOWN and snake.direction != Vector2(0, -1):  # Prevent 180-degree turn
#                     snake.direction = Vector2(0, 1)
#                 elif event.key == pygame.K_p:
#                     pause_menu()
#                 elif event.key == pygame.K_f:
#                     toggle_full_screen()

#         snake.move_snake()

#         if snake.body[0].x >= dis_width or snake.body[0].x < 0 or snake.body[0].y >= dis_height or snake.body[0].y < 0:
#             game_close = True


#         draw_background(grass1, grass2, 100)  # Draw the background with transparency
        
#         fruit.draw_fruit()

#         snake.draw_snake()
#         your_score(score, high_score, level)

#         pygame.display.update()

#         if snake.body[0] == fruit.position:
#             fruit.randomize_position()
#             snake.add_block()
#             score += 1
#             if score % 3 == 0:
#                 level += 1
#                 snake_speed += 5

#         for segment in snake.body[1:]:
#             if segment == snake.body[0]:
#                 game_close = True

#         clock.tick(snake_speed)

#     if score > high_score:
#         high_score = score

#     game_over_screen()

# def gameLoop():
#     global high_score  # Ensure high_score can be modified globally

#     snake_speed = initial_snake_speed
#     level = 0
#     score = 0  # Initialize score to 0

#     game_over = False
#     game_close = False

#     snake = SNAKE()  # Initialize the snake object
#     fruit = FRUIT()  # Initialize the fruit object
#     foodx, foody = generate_food()

#     Length_of_snake = 1

#     while not game_over:
#         while game_close == True:
#             dis.blit(you_lost_background, (0, 0))
#             message("You Lost! Press Q-Quit or C-Play Again", red, center=True)
#             message(f"High Score: {high_score}", white, 50, center=True)
#             pygame.display.update()

#             for event in pygame.event.get():
#                 if event.type == pygame.KEYDOWN:
#                     if event.key == pygame.K_q:
#                         game_over = True
#                         game_close = False
#                     if event.key == pygame.K_c:
#                         gameLoop()

#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 game_over = True
#             if event.type == pygame.KEYDOWN:
                # if event.key == pygame.K_LEFT and snake.direction != Vector2(1, 0):  # Prevent 180-degree turn
                #     snake.direction = Vector2(-1, 0)
                # elif event.key == pygame.K_RIGHT and snake.direction != Vector2(-1, 0):  # Prevent 180-degree turn
                #     snake.direction = Vector2(1, 0)
                # elif event.key == pygame.K_UP and snake.direction != Vector2(0, 1):  # Prevent 180-degree turn
                #     snake.direction = Vector2(0, -1)
                # elif event.key == pygame.K_DOWN and snake.direction != Vector2(0, -1):  # Prevent 180-degree turn
                #     snake.direction = Vector2(0, 1)
                # elif event.key == pygame.K_p:
                #     pause_menu()
                # elif event.key == pygame.K_f:
                #     toggle_full_screen()

#         # Move the snake
#         snake.move_snake()

#         # Check for wall collision
#         if snake.body[0].x >= dis_width or snake.body[0].x < 0 or snake.body[0].y >= dis_height or snake.body[0].y < 0:
#             game_close = True

#         draw_background(grass1, grass2, 100)  # Draw the background with transparency
        
#         fruit.draw_fruit()

#         # Check for self-collision
#         for segment in snake.body[1:]:
#             if segment == snake.body[0]:  # If the head collides with any segment of the body
#                 game_close = True

#         snake.draw_snake()
#         your_score(score, high_score, level)

#         pygame.display.update()

#         # Check for food collision
#         if snake.body[0] == fruit.position:
#             fruit.randomize_position()
#             Length_of_snake += 1  # Increase length of snake when it eats food
#             score += 1
#             if score % 3 == 0:
#                 level += 1
#                 snake_speed += 5

#         clock.tick(snake_speed)

#     if score > high_score:
#         high_score = score

#     game_over_screen()

def gameMenu():
    menu = True
    while menu:
        dis.blit(menu_background, (0, 0)) 
        message("MEDIYO SNAKE GAME", white, -100, center=True)
        message("Press S to Start", yellow, -30, center=True)
        message("Press I for Instructions", black, 10, center=True)
        message("Press Q to Quit", red, 50, center=True)
        message("Press E for Settings", black, 90, center=True)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    menu = False
                if event.key == pygame.K_i:
                    show_instructions()
                if event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()
                if event.key == pygame.K_e:
                    settings_menu()

def show_instructions():
    instructions = True
    while instructions:
        dis.blit(menu_background, (0, 0)) 
        message("INSTRUCTIONS", white, -100, center=True)
        message("Use arrow keys to move the snake", black, -30, center=True)
        message("Eat the green food to grow", black, 10, center=True)
        message("Avoid hitting the walls or yourself", black, 50, center=True)
        message("Press B to go back to the menu", red, 90, center=True)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_b:
                    instructions = False

gameMenu()
gameLoop()