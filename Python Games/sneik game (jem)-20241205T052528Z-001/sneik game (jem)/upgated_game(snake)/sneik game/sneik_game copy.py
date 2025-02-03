import pygame
import random
from pygame.math import Vector2

# Initialize pygame
pygame.init()

# Screen dimensions and color definitions
width = 600
height = 400
dis = pygame.display.set_mode((width, height))
pygame.display.set_caption("Snake Game")
black = (0, 0, 0)
white = (255, 255, 255)
red = (213, 50, 80)
green = (0, 255, 0)
blue = (50, 153, 213)

# Snake block size
snake_block = 20

# Frame rate
clock = pygame.time.Clock()
snake_speed = 15

# Images for the snake parts (head, body, tail)
head_up = pygame.image.load('../assets/graphics/head_up.png')  # Replace with your image file paths
head_down = pygame.image.load('../assets/graphics/head_down.png')
head_left = pygame.image.load('../assets/graphics/head_left.png')
head_right = pygame.image.load('../assets/graphics/head_right.png')
body_vertical = pygame.image.load('../assets/graphics/body_vertical.png')
body_horizontal = pygame.image.load('../assets/graphics/body_horizontal.png')
tail_up = pygame.image.load('../assets/graphics/tail_up.png')
tail_down = pygame.image.load('../assets/graphics/tail_down.png')
tail_left = pygame.image.load('../assets/graphics/tail_left.png')
tail_right = pygame.image.load('../assets/graphics/tail_right.png')

# Snake class
class Snake:
    def __init__(self):
        self.body = [Vector2(5, 5), Vector2(4, 5), Vector2(3, 5)]  # Initial snake body
        self.direction = Vector2(1, 0)  # Initial direction (right)
    
    def move(self):
        new_head = self.body[0] + self.direction
        self.body.insert(0, new_head)
        self.body.pop()
    
    def grow(self):
        new_head = self.body[0] + self.direction
        self.body.insert(0, new_head)
    
    def draw(self):
        for index, block in enumerate(self.body):
            x_pos = int(block.x * snake_block)
            y_pos = int(block.y * snake_block)
            block_rect = pygame.Rect(x_pos, y_pos, snake_block, snake_block)

            # Draw the head
            if index == 0:
                if self.direction == Vector2(0, -1):  # Moving Up
                    dis.blit(head_up, block_rect)
                elif self.direction == Vector2(0, 1):  # Moving Down
                    dis.blit(head_down, block_rect)
                elif self.direction == Vector2(1, 0):  # Moving Right
                    dis.blit(head_right, block_rect)
                elif self.direction == Vector2(-1, 0):  # Moving Left
                    dis.blit(head_left, block_rect)
            
            # Draw the tail
            elif index == len(self.body) - 1:
                tail_relation = self.body[-2] - self.body[-1]
                if tail_relation == Vector2(0, -1):
                    dis.blit(tail_up, block_rect)
                elif tail_relation == Vector2(0, 1):
                    dis.blit(tail_down, block_rect)
                elif tail_relation == Vector2(1, 0):
                    dis.blit(tail_right, block_rect)
                elif tail_relation == Vector2(-1, 0):
                    dis.blit(tail_left, block_rect)

            # Draw the body
            else:
                previous_block = self.body[index + 1] - self.body[index]
                next_block = self.body[index - 1] - self.body[index]
                if previous_block.x == next_block.x:
                    dis.blit(body_vertical, block_rect)
                elif previous_block.y == next_block.y:
                    dis.blit(body_horizontal, block_rect)
                else:
                    if previous_block.x == -1 and next_block.y == -1 or previous_block.y == -1 and next_block.x == -1:
                        dis.blit(body_vertical, block_rect)
                    elif previous_block.y == 1 and next_block.x == -1 or previous_block.x == -1 and next_block.y == 1:
                        dis.blit(body_horizontal, block_rect)
                    elif previous_block.y == -1 and next_block.x == 1 or previous_block.x == 1 and next_block.y == -1:
                        dis.blit(body_vertical, block_rect)
                    elif previous_block.x == 1 and next_block.y == 1 or previous_block.y == 1 and next_block.x == 1:
                        dis.blit(body_horizontal, block_rect)

# Game loop
def gameLoop():
    game_over = False
    snake = Snake()
    
    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and snake.direction != Vector2(0, 1):
                    snake.direction = Vector2(0, -1)
                elif event.key == pygame.K_DOWN and snake.direction != Vector2(0, -1):
                    snake.direction = Vector2(0, 1)
                elif event.key == pygame.K_LEFT and snake.direction != Vector2(1, 0):
                    snake.direction = Vector2(-1, 0)
                elif event.key == pygame.K_RIGHT and snake.direction != Vector2(-1, 0):
                    snake.direction = Vector2(1, 0)

        snake.move()
        
        # Check for collisions (e.g., snake hitting itself or walls)
        if snake.body[0].x >= width // snake_block or snake.body[0].x < 0 or snake.body[0].y >= height // snake_block or snake.body[0].y < 0:
            game_over = True

        for block in snake.body[1:]:
            if snake.body[0] == block:
                game_over = True

        dis.fill(blue)  # Clear screen
        snake.draw()  # Draw the snake
        pygame.display.update()
        
        clock.tick(snake_speed)

    pygame.quit()

# Run the game
gameLoop()
