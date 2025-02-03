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
    def __init__(self, game, vs_computer=False):
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

        self.line_indices_array = [[(0, 0), (0, 1), (0, 2)],
                                   [(1, 0), (1, 1), (1, 2)],
                                   [(2, 0), (2, 1), (2, 2)],
                                   [(0, 0), (1, 0), (2, 0)],
                                   [(0, 1), (1, 1), (2, 1)],
                                   [(0, 2), (1, 2), (2, 2)],
                                   [(0, 0), (1, 1), (2, 2)],
                                   [(0, 2), (1, 1), (2, 0)]]
        self.winner = None
        self.game_steps = 0
        self.font = pg.font.SysFont('Verdana', CELL_SIZE // 6, True)

        self.win_sound_played = False
        self.draw_sound_played = False

    def check_winner(self):
        for line_indices in self.line_indices_array:
            sum_line = sum([self.game_array[i][j] for i, j in line_indices])
            if sum_line in {0, 3}:
                self.winner = 'XO'[sum_line == 0]
                self.winner_line = [vec2(line_indices[0][::-1]) * CELL_SIZE + CELL_CENTER,
                                    vec2(line_indices[2][::-1]) * CELL_SIZE + CELL_CENTER]

    def get_available_cells(self):
        return [(row, col) for row in range(3) for col in range(3) if self.game_array[row][col] == INF]

    def computer_move(self):
        if not self.winner and self.game_steps < 9:
            available_cells = self.get_available_cells()
            if available_cells:
                row, col = choice(available_cells)
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

        if self.player == 0 and self.vs_computer:
            pg.time.delay(500)
            self.computer_move()

    def draw_objects(self):
        for y, row in enumerate(self.game_array):
            for x, obj in enumerate(row):
                if obj != INF:
                    self.game.screen.blit(self.X_image if obj else self.O_image, vec2(x, y) * CELL_SIZE)

    def draw_winner(self):
        if self.winner:
            pg.draw.line(self.game.screen, 'red', *self.winner_line, CELL_SIZE // 8)
            self.animate_message(f'Player "{self.winner}" wins!')
            self.confetti_effect()
            if not self.win_sound_played:
                self.win_sound.play()
                self.win_sound_played = True
        elif self.game_steps == 9 and not self.winner:
            self.animate_message("Game Draw!")
            if not self.draw_sound_played:
                self.draw_sound.play()
                self.draw_sound_played = True

    def draw(self):
        self.game.screen.blit(self.field_image, (0, 0))
        self.draw_objects()
        self.draw_winner()

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

    def animate_message(self, message):
        font = pg.font.SysFont('Verdana', CELL_SIZE // 4, True)
        label = font.render(message, True, 'white')
        self.game.screen.blit(label, (WIN_SIZE // 2 - label.get_width() // 2, WIN_SIZE // 4))

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
        self.tic_tac_toe = TicTacToe(self, vs_computer=self.vs_computer)
        self.running = False
        self.paused = False

        self.background_image = pg.image.load('./resources/background.jpg')
        self.background_image = pg.transform.scale(self.background_image, (WIN_SIZE, WIN_SIZE))

        pg.mixer.music.load('./resources/background.mp3')
        pg.mixer.music.set_volume(0.5)
        pg.mixer.music.play(-1)

    def new_game(self):
        self.tic_tac_toe = TicTacToe(self, vs_computer=self.vs_computer)
        # Let the computer make the first move if it's Player vs Computer and the computer starts
        if self.tic_tac_toe.vs_computer and self.tic_tac_toe.player == 0:
            self.tic_tac_toe.computer_move()


    def show_mode_selection(self):
        self.screen.blit(self.background_image, (0, 0))
        font = pg.font.SysFont('Verdana', CELL_SIZE // 6, True)
        label1 = font.render("Press 1 for Player vs Player", True, 'white')
        label2 = font.render("Press 2 for Player vs Computer", True, 'white')
        self.screen.blit(label1, (WIN_SIZE // 2 - label1.get_width() // 2, WIN_SIZE // 3))
        self.screen.blit(label2, (WIN_SIZE // 2 - label2.get_width() // 2, WIN_SIZE // 2))
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
                    elif event.key == pg.K_2:
                        self.vs_computer = True
                        self.running = True

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
                elif event.key == pg.K_q and (self.tic_tac_toe.winner or self.tic_tac_toe.game_steps == 9):
                    pg.quit()
                    sys.exit()

    def run(self):
        self.show_mode_selection()
        while True:
            self.check_events()
            if not self.paused:
                self.tic_tac_toe.run()
            pg.display.update()
            self.clock.tick(60)

game = Game()
game.run()
