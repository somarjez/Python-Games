import tkinter as tk
from tkinter import messagebox, font
import random

# Game Configuration
WINDOW_SIZE = 600
CELL_SIZE = 20
FOOD_POINTS = 25
BACKGROUND_COLOR = "#1A1A2E"
SNAKE_COLOR = "#4A6FA5"
FOOD_COLOR = "#E94560"
TEXT_COLOR = "#0F3460"

class SnakeGame:
    def __init__(self, root):
        # Create game window with improved styling
        self.root = root
        self.snake_window = tk.Toplevel(root)
        self.snake_window.title("Snake Adventure")
        self.snake_window.configure(bg=BACKGROUND_COLOR)
        self.snake_window.resizable(False, False)

        # Create custom fonts
        self.title_font = font.Font(family="Helvetica", size=24, weight="bold")
        self.button_font = font.Font(family="Helvetica", size=14, weight="bold")

        # Create canvas with improved background
        self.canvas = tk.Canvas(
            self.snake_window, 
            width=WINDOW_SIZE, 
            height=WINDOW_SIZE, 
            bg=BACKGROUND_COLOR, 
            highlightthickness=0
        )
        self.canvas.pack(padx=20, pady=20)

        # Game state variables
        self.high_score = 0
        self.custom_font = font.Font(family="Helvetica", size=16)

        self.ready_to_play()

    def create_styled_button(self, text, command):
        """Create a styled button with hover effects"""
        button = tk.Button(
            self.snake_window, 
            text=text, 
            command=command,
            font=self.button_font,
            bg=TEXT_COLOR,
            fg="white",
            activebackground="#0F3460",
            activeforeground="white",
            relief=tk.FLAT,
            padx=10,
            pady=5
        )
        return button

    def ready_to_play(self):
        self.canvas.delete("all")
        
        # Title with gradient-like effect
        self.canvas.create_text(
            WINDOW_SIZE / 2, 
            WINDOW_SIZE / 3, 
            text="Snake Adventure", 
            fill=FOOD_COLOR, 
            font=self.title_font
        )
        
        # Create buttons with improved styling
        yes_button = self.create_styled_button("Start", self.start_game)
        exit_button = self.create_styled_button("Exit", self.snake_window.destroy)
        
        # Position buttons
        self.canvas.create_window(WINDOW_SIZE / 2 - 70, WINDOW_SIZE / 2, window=yes_button)
        self.canvas.create_window(WINDOW_SIZE / 2 + 70, WINDOW_SIZE / 2, window=exit_button)

        # Display high score
        self.canvas.create_text(
            WINDOW_SIZE / 2, 
            WINDOW_SIZE / 1.5, 
            text=f"High Score: {self.high_score}", 
            fill="white", 
            font=self.custom_font
        )

    def start_game(self):
        self.canvas.delete("all")
        self.snake = [(100, 100), (80, 100), (60, 100)]  # Initial snake
        self.food = None
        self.direction = "Right"
        self.food_count = 0
        self.speed = 200

        # Create snake body with improved coloring
        self.snake_squares = [
            self.canvas.create_rectangle(
                x, y, x + CELL_SIZE, y + CELL_SIZE, 
                fill=SNAKE_COLOR, 
                outline=BACKGROUND_COLOR
            ) for x, y in self.snake
        ]

        self.create_food()

        # Bind arrow keys to movement
        self.snake_window.bind("<Up>", lambda event: self.change_direction("Up"))
        self.snake_window.bind("<Down>", lambda event: self.change_direction("Down"))
        self.snake_window.bind("<Left>", lambda event: self.change_direction("Left"))
        self.snake_window.bind("<Right>", lambda event: self.change_direction("Right"))

        # Set focus to the snake window to capture key events
        self.snake_window.focus_set()

        # Display score
        self.score_text = self.canvas.create_text(
            50, 20, 
            text=f"Score: {self.food_count}", 
            fill="white", 
            font=self.custom_font, 
            anchor="w"
        )

        self.game_running = True
        self.move_snake()

    def create_food(self):
        # Create food with gradient-like effect
        x = random.randint(0, (WINDOW_SIZE // CELL_SIZE) - 1) * CELL_SIZE
        y = random.randint(0, (WINDOW_SIZE // CELL_SIZE) - 1) * CELL_SIZE
        self.food = self.canvas.create_oval(
            x, y, x + CELL_SIZE, y + CELL_SIZE, 
            fill=FOOD_COLOR, 
            outline=BACKGROUND_COLOR
        )
        self.food_position = (x, y)

    def move_snake(self):
        if not self.game_running:
            return

        head_x, head_y = self.snake[0]

        # Move head in the current direction
        if self.direction == "Up":
            head_y -= CELL_SIZE
        elif self.direction == "Down":
            head_y += CELL_SIZE
        elif self.direction == "Left":
            head_x -= CELL_SIZE
        elif self.direction == "Right":
            head_x += CELL_SIZE

        new_head = (head_x, head_y)

        # Check for game over (collision with walls or self)
        if self.check_collision(new_head):
            self.game_over()
            return

        # Check if snake eats food
        if new_head == self.food_position:
            self.snake.append(self.snake[-1])  # Grow the snake
            self.canvas.delete(self.food)  # Remove the eaten food
            self.create_food()  # Create new food
            self.food_count += 1
            
            # Update score display
            self.canvas.itemconfig(
                self.score_text, 
                text=f"Score: {self.food_count}"
            )
            
            # Increase speed
            self.speed = max(50, self.speed - 10)

        else:
            self.snake = [new_head] + self.snake[:-1]

        self.update_snake_squares()

        self.snake_window.after(self.speed, self.move_snake)

    def update_snake_squares(self):
        for i, (x, y) in enumerate(self.snake):
            if i >= len(self.snake_squares):
                self.snake_squares.append(
                    self.canvas.create_rectangle(
                        x, y, x + CELL_SIZE, y + CELL_SIZE, 
                        fill=SNAKE_COLOR, 
                        outline=BACKGROUND_COLOR
                    )
                )
            else:
                self.canvas.coords(
                    self.snake_squares[i], 
                    x, y, x + CELL_SIZE, y + CELL_SIZE
                )

        while len(self.snake_squares) > len(self.snake):
            self.canvas.delete(self.snake_squares.pop())

    def change_direction(self, new_direction):
        opposite_directions = {"Up": "Down", "Down": "Up", "Left": "Right", "Right": "Left"}
        if self.direction != opposite_directions.get(new_direction):
            self.direction = new_direction

    def check_collision(self, head):
        x, y = head
        if x < 0 or x >= WINDOW_SIZE or y < 0 or y >= WINDOW_SIZE:
            return True
        if head in self.snake[1:]:
            return True
        return False

    def game_over(self):
        self.game_running = False
        points = self.food_count * FOOD_POINTS
        
        # Update high score
        self.high_score = max(self.high_score, points)

        self.canvas.delete("all")
        
        # Game over text with improved styling
        self.canvas.create_text(
            WINDOW_SIZE / 2, 
            WINDOW_SIZE / 3, 
            text=f"Game Over!", 
            fill=FOOD_COLOR, 
            font=self.title_font
        )
        self.canvas.create_text(
            WINDOW_SIZE / 2, 
            WINDOW_SIZE / 2, 
            text=f"You ate {self.food_count} food(s)\nTotal Points: {points}", 
            fill="white", 
            font=self.custom_font
        )
        
        # Styled buttons
        play_again_button = self.create_styled_button("Play Again", self.reset_game)
        exit_button = self.create_styled_button("Exit", self.snake_window.destroy)
        
        self.canvas.create_window(WINDOW_SIZE / 2 - 70, WINDOW_SIZE / 2 + 100, window=play_again_button)
        self.canvas.create_window(WINDOW_SIZE / 2 + 70, WINDOW_SIZE / 2 + 100, window=exit_button)

    def reset_game(self):
        self.canvas.delete("all")
        self.snake = [(100, 100), (80, 100), (60, 100)]
        self.food_count = 0
        self.direction = "Right"
        self.speed = 200
        self.snake_squares = [
            self.canvas.create_rectangle(
                x, y, x + CELL_SIZE, y + CELL_SIZE, 
                fill=SNAKE_COLOR, 
                outline=BACKGROUND_COLOR
            ) for x, y in self.snake
        ]
        self.create_food()
        self.game_running = True
        self.move_snake()

if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    game = SnakeGame(root)
    root.mainloop()