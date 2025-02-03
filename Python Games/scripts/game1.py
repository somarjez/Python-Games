import pygame as pg
import sys
from random import choice
import os

os.chdir(os.path.dirname(os.path.abspath(__file__)))

WIN_SIZE = 700
CELL_SIZE = WIN_SIZE // 3
INF = float('inf')
vec2 = pg.math.Vector2
CELL_CENTER = vec2(CELL_SIZE / 2)

class TicTacToe:
    def __init__(self, game, vs_computer=False, difficulty='hard'):
        self.game = game
        self.field_image = self.get_scaled_image(path='./resources/field.png', res=[WIN_SIZE] * 2)
        self.O_image = self.get_scaled_image(path='./resources/o.png', res=[CELL_SIZE] * 2)
        self.X_image = self.get_scaled_image(path='./resources/x.png', res=[CELL_SIZE] * 2)

        self.click_sound = pg.mixer.Sound('./resources/click.wav')
        self.win_sound = pg.mixer.Sound('./resources/win.mp3')
        self.draw_sound = pg.mixer.Sound('./resources/draw.wav')

        self.game_array = [[INF, INF, INF],
                           [INF, INF, INF],
                           [INF, INF, INF]]
        self.player = 1  # Player starts first
        self.vs_computer = vs_computer
        self.difficulty = difficulty

        self.line_indices_array = [[(0, 0), (0, 1), (0, 2)],  # First row
                                   [(1, 0), (1, 1), (1, 2)],  # Second row
                                   [(2, 0), (2, 1), (2, 2)],  # Third row
                                   [(0, 0), (1, 0), (2, 0)],  # First column
                                   [(0, 1), (1, 1), (2, 1)],  # Second column
                                   [(0, 2), (1, 2), (2, 2)],  # Third column
                                   [(0, 0), (1, 1), (2, 2)],  # Diagonal top-left to bottom-right
                                   [(0, 2), (1, 1), (2, 0)]]  # Diagonal top-right to bottom-left
        self.winner = None
        self.game_steps = 0
        self.font = pg.font.SysFont('Verdana', CELL_SIZE // 6, True)

        self.win_sound_played = False
        self.draw_sound_played = False
        self.computer_thinking_timer = 0
        self.computer_thinking_delay = 1000  # 1 second delay

    def check_winner(self):
        for line_indices in self.line_indices_array:
            # Get the values in the line
            line_values = [self.game_array[i][j] for i, j in line_indices]
            
            # Check if all values in the line are the same and not INF
            if len(set(line_values)) == 1 and line_values[0] != INF:
                self.winner = 'XO'[line_values[0] == 0]
                self.winner_line = [vec2(line_indices[0][::-1]) * CELL_SIZE + CELL_CENTER,
                                    vec2(line_indices[2][::-1]) * CELL_SIZE + CELL_CENTER]
                break

    def get_available_cells(self):
        return [(row, col) for row in range(3) for col in range(3) if self.game_array[row][col] == INF]

    def minimax(self, depth, is_maximizing):
        """
        Minimax algorithm to determine the best move for the computer.
        Returns the best score for the current board state.
        """
        # Check for terminal states first
        result = self.check_terminal_state()
        if result is not None:
            return result

        # If maximizing player (computer), try to maximize score
        if is_maximizing:
            best_score = -INF
            for row in range(3):
                for col in range(3):
                    if self.game_array[row][col] == INF:
                        # Try this move
                        self.game_array[row][col] = 0  # Computer is O (0)
                        score = self.minimax(depth + 1, False)
                        # Undo the move
                        self.game_array[row][col] = INF
                        best_score = max(score, best_score)
            return best_score
        # If minimizing player (human), try to minimize score
        else:
            best_score = INF
            for row in range(3):
                for col in range(3):
                    if self.game_array[row][col] == INF:
                        # Try this move
                        self.game_array[row][col] = 1  # Human is X (1)
                        score = self.minimax(depth + 1, True)
                        # Undo the move
                        self.game_array[row][col] = INF
                        best_score = min(score, best_score)
            return best_score

    def find_best_move(self):
        """
        Find the best move for the computer using minimax algorithm.
        """
        best_score = -INF
        best_move = None

        for row in range(3):
            for col in range(3):
                if self.game_array[row][col] == INF:
                    # Try this move
                    self.game_array[row][col] = 0  # Computer is O (0)
                    score = self.minimax(0, False)
                    # Undo the move
                    self.game_array[row][col] = INF

                    # Update best move if this move has a better score
                    if score > best_score:
                        best_score = score
                        best_move = (row, col)

        return best_move

    def check_terminal_state(self):
        """
        Check if the game has reached a terminal state and return a score.
        Returns None if game is not over, otherwise returns score.
        """
        for line_indices in self.line_indices_array:
            line_values = [self.game_array[i][j] for i, j in line_indices]
            
            # Check for computer (O) win
            if len(set(line_values)) == 1 and line_values[0] == 0:
                return 10  # Positive score for computer win
            
            # Check for human (X) win
            if len(set(line_values)) == 1 and line_values[0] == 1:
                return -10  # Negative score for human win

        # Check for draw
        if len(self.get_available_cells()) == 0:
            return 0  # Draw

        # Game not over
        return None

    def computer_move(self):
        if not self.winner and self.game_steps < 9:
            if self.difficulty == 'easy':
                available_cells = self.get_available_cells()
                if available_cells:
                    row, col = choice(available_cells)
                    self.game_array[row][col] = self.player
            else:  # hard difficulty
                best_move = self.find_best_move()
                if best_move:
                    row, col = best_move
                    self.game_array[row][col] = self.player

            self.game_steps += 1
            self.check_winner()
            self.player = not self.player

    def run_game_process(self):
        if self.player == 1 or not self.vs_computer:
            current_cell = vec2(pg.mouse.get_pos()) // CELL_SIZE
            col, row = map(int, current_cell)
            left_click = pg.mouse.get_pressed()[0]

            if left_click and self.game_array[row][col] == INF and not self.winner:
                self.click_sound.play()
                self.game_array[row][col] = self.player
                self.player = not self.player
                self.game_steps += 1
                self.check_winner()
                
                # Added computer thinking timer for computer move
                if self.vs_computer and self.player == 0:
                    self.computer_thinking_timer = pg.time.get_ticks()

        if self.player == 0 and self.vs_computer:
            # Add delay for computer thinking
            if pg.time.get_ticks() - self.computer_thinking_timer > self.computer_thinking_delay:
                self.computer_move()

    def draw_objects(self):
        for y, row in enumerate(self.game_array):
            for x, obj in enumerate(row):
                if obj != INF:
                    self.game.screen.blit(self.X_image if obj else self.O_image, vec2(x, y) * CELL_SIZE)

    def draw_winner(self):
        if self.winner:
            pg.draw.line(self.game.screen, 'red', *self.winner_line, CELL_SIZE // 8)
            self.animate_message(f'Player "{self.winner}" wins!', font_size=CELL_SIZE // 4)
            self.confetti_effect()
            if not self.win_sound_played:
                self.win_sound.play()
                self.win_sound_played = True
        elif self.game_steps == 9 and not self.winner:
            self.animate_message("Game Draw!", font_size=CELL_SIZE // 4)
            if not self.draw_sound_played:
                self.draw_sound.play()
                self.draw_sound_played = True

    def draw(self):
        self.game.screen.blit(self.field_image, (0, 0))
        self.draw_objects()
        self.draw_winner()

        # Add computer thinking message
        if self.vs_computer and self.player == 0 and not self.winner and self.game_steps < 9:
            computer_thinking_font = pg.font.SysFont('Verdana', CELL_SIZE // 6, True)
            thinking_label = computer_thinking_font.render("Computer is thinking...", True, 'white')
            self.game.screen.blit(thinking_label, (WIN_SIZE // 2 - thinking_label.get_width() // 2, WIN_SIZE * 0.9))

    @staticmethod
    def get_scaled_image(path, res):
        img = pg.image.load(path)
        return pg.transform.smoothscale(img, res)

    def print_caption(self):
        if self.winner:
            pg.display.set_caption(f'Player "{self.winner}" wins!')
        elif self.game_steps == 9:
            pg.display.set_caption("It's a draw!")
        else:
            turn = "Computer" if self.vs_computer and self.player == 0 else "Player"
            pg.display.set_caption(f'{turn} "{"OX"[self.player]}" turn!')

    def run(self):
        self.print_caption()
        self.draw()
        if not self.winner and self.game_steps < 9:
            self.run_game_process()

    def animate_message(self, message, font_size=None):
        if font_size is None:
            font_size = CELL_SIZE // 4
        font = pg.font.SysFont('Verdana', font_size, True)
        label = font.render(message, True, 'white')
        # Centered and position adjusted to fit screen
        self.game.screen.blit(label, (WIN_SIZE // 2 - label.get_width() // 2, WIN_SIZE // 3))

    def confetti_effect(self):
        for _ in range(100):
            x, y = choice(range(WIN_SIZE)), choice(range(WIN_SIZE))
            color = choice(['red', 'green', 'blue', 'yellow', 'purple'])
            pg.draw.circle(self.game.screen, color, (x, y), 5)

class Game:
    def __init__(self):
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode([WIN_SIZE] * 2)
        self.clock = pg.time.Clock()
        self.vs_computer = False
        self.difficulty = 'hard'
        self.tic_tac_toe = TicTacToe(self, vs_computer=self.vs_computer, difficulty=self.difficulty)
        self.running = False
        self.paused = False

        self.background_image = pg.image.load('./resources/background.jpg')
        self.background_image = pg.transform.scale(self.background_image, (WIN_SIZE, WIN_SIZE))

        pg.mixer.music.load('./resources/background.mp3')
        pg.mixer.music.set_volume(0.5)
        pg.mixer.music.play(-1)

    def new_game(self):
        self.tic_tac_toe = TicTacToe(self, vs_computer=self.vs_computer, difficulty=self.difficulty)
        if self.tic_tac_toe.vs_computer and self.tic_tac_toe.player == 0:
            self.tic_tac_toe.computer_move()

    def show_mode_selection(self):
        self.screen.blit(self.background_image, (0, 0))
        
        # Dynamically size the title to fit the screen
        title_font_size = CELL_SIZE // 3  # Starting with a smaller size
        title_font = pg.font.SysFont('Verdana', title_font_size, True)
        title_label = title_font.render("TIC-TAC-TOE", True, 'white')
        
        # Reduce font size if the title is too wide
        while title_label.get_width() > WIN_SIZE * 0.9:
            title_font_size -= 5
            title_font = pg.font.SysFont('Verdana', title_font_size, True)
            title_label = title_font.render("TIC-TAC-TOE", True, 'white')
        
        self.screen.blit(title_label, (WIN_SIZE // 2 - title_label.get_width() // 2, WIN_SIZE // 6))

        # Instructions with smaller font
        font = pg.font.SysFont('Verdana', CELL_SIZE // 6, True)
        instructions = [
            "Press 1 to play with a friend",
            "Press 2 to play with a computer",
            "Press P to pause and resume",
            "Press C to continue the game",
            "Press Q to Quit",
            "Press M to go back to Menu"
        ]

        for i, instruction in enumerate(instructions):
            label = font.render(instruction, True, 'white')
            self.screen.blit(label, (WIN_SIZE // 2 - label.get_width() // 2, WIN_SIZE // 3 + (i * CELL_SIZE // 6)))
        
        pg.display.update()

        while not self.running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_1:
                        self.vs_computer = False
                        self.running = True
                        self.new_game()
                    elif event.key == pg.K_2:
                        self.vs_computer = True
                        self.show_difficulty_selection()

    def show_difficulty_selection(self):
        self.screen.blit(self.background_image, (0, 0))
        
        font = pg.font.SysFont('Verdana', CELL_SIZE // 6, True)
        instructions = [
            "Press A for Easy",
            "Press B for Hard"
        ]

        for i, instruction in enumerate(instructions):
            label = font.render(instruction, True, 'white')
            self.screen.blit(label, (WIN_SIZE // 2 - label.get_width() // 2, WIN_SIZE // 3 + (i * CELL_SIZE // 6)))
        
        pg.display.update()

        while not self.running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_a:
                        self.difficulty = 'easy'
                        self.running = True
                        self.new_game()
                    elif event.key == pg.K_b:
                        self.difficulty = 'hard'
                        self.running = True
                        self.new_game()

    def check_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE and not self.running:
                    self.running = True
                elif event.key == pg.K_p:
                    self.paused = not self.paused
                elif event.key == pg.K_c and (self.tic_tac_toe.winner or self.tic_tac_toe.game_steps == 9):
                    self.new_game()
                elif event.key == pg.K_q:
                    pg.quit()
                    sys.exit()
                elif event.key == pg.K_m:
                    self.running = False
                    self.show_mode_selection()

    def run(self):
        self.show_mode_selection()

        while True:
            self.check_events()
            if self.running and not self.paused:
                self.tic_tac_toe.run()
            elif self.paused:
                self.tic_tac_toe.animate_message("Game Paused!", font_size=CELL_SIZE // 3)
            pg.display.update()
            self.clock.tick(30)

if __name__ == '__main__':
    Game().run()