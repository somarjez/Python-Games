from tkinter import Button, Label, PhotoImage
import random
import settings
import tkinter as tk
import sys

def rgb_to_hex(rgb):
        return '#%02x%02x%02x' % rgb

class Cell:
    all = []
    cell_count = settings.cell_count
    cell_count_label_object = None
    def __init__(self, x, y, is_mine = False):
        self.is_mine = is_mine
        self.is_opened = False
        self.is_mine_candidate = False
        self.cell_btn_object = None
        self.x = x
        self.y = y

        # APPEND OBJECTS TO THE CELL.ALL LIST
        Cell.all.append(self)
    
    def create_btn_object(self, location):
        btn = Button(
            location,
            width = 20, # BTN WIDTH
            height = 8, # BTN HEIGHT
            bg=settings.themes[settings.current_theme]["cell_bg"],
            fg=settings.themes[settings.current_theme]["text"]
        )
        btn.bind('<Button-1>', self.left_click_actions)
        btn.bind('<Button-3>', self.right_click_actions)
        self.cell_btn_object = btn

    @staticmethod
    def create_cell_count_label(location):
        Cell.cell_count = settings.grid_size ** 2
        lbl = Label(
            location,
            bg=settings.themes[settings.current_theme]["frame_bg"],
            fg=settings.themes[settings.current_theme]["text"],
            text=f'Cells Left:{Cell.cell_count}',
            font=("Lucida Console", 12)
        )
        Cell.cell_count_label_object = lbl

    @staticmethod
    def create_mines_left_label(location):
        lbl = Label(
            location,
            bg=settings.themes[settings.current_theme]["frame_bg"],
            fg=settings.themes[settings.current_theme]["text"],
            text=f'Mines Left:{settings.mines_count}',
            font=("Lucida Console", 12)
        )
        Cell.mines_left_label_object = lbl

    def left_click_actions(self, event): # LEFT CLICK
        if self.is_mine:
            self.show_mine()
            Cell.mines_left_label_object.configure(text=f'Mines Left:{settings.mines_count - 1}') # DECREASE MINES LEFT COUNT
            game_window = self.cell_btn_object.winfo_toplevel()
            x = game_window.winfo_x() + (game_window.winfo_width() / 2) - 200
            y = game_window.winfo_y() + (game_window.winfo_height() / 2) - 100
            root = tk.Tk()
            root.title("Game Over")
            root.iconbitmap("videogame.ico")
            label = tk.Label(root, text="Game Over! You hit a mine!", font=("Lucida Console", 12))
            label.pack(padx=20, pady=20)
            def on_closing():
                root.destroy()
                sys.exit()
            button = tk.Button(root, text="OK", width=8, height=2, font=("Arial", 7), command=on_closing)
            button.pack(pady=2)
            root.geometry(f'450x125+{int(x)}+{int(y)}')
            root.resizable(False, False)

            root.mainloop()
        else:
            if self.surrounded_cells_mines_amount == 0:
                for cell_object in self.surrounded_cells:
                    cell_object.show_cell()
            self.show_cell()
            if Cell.cell_count == settings.mines_count:
                game_window = self.cell_btn_object.winfo_toplevel()
                x = game_window.winfo_x() + (game_window.winfo_width() / 2) - 200
                y = game_window.winfo_y() + (game_window.winfo_height() / 2) - 100
                root = tk.Tk()
                root.title("Game Over")
                root.iconbitmap("videogame.ico")
                label = tk.Label(root, text="Congratulations! You beat the game!", font=("Lucida Console", 12))
                label.pack(padx=20, pady=20)
                def on_closing():
                    root.destroy()
                    sys.exit()
                button = tk.Button(root, text="OK", width=8, height=2, font=("Arial", 7), command=on_closing)
                button.pack(pady=2)
                root.geometry(f'450x125+{int(x)}+{int(y)}')
                root.resizable(False, False)
                root.mainloop()
            
        self.cell_btn_object.unbind('<Button-1>')
        self.cell_btn_object.unbind('<Button-3>')

    def get_cell_by_axis(self, x, y):
        for cell in Cell.all:
            if cell.x == x and cell.y == y:
                return cell
            

    # THIS IS A LOGIC TO EXAMINE THE SURROUNDING CELLS TO COUNT ALL THE MINES SURROUNDING IT
    @property
    def surrounded_cells(self):
        cells = [
            self.get_cell_by_axis(self.x - 1, self.y - 1),
            self.get_cell_by_axis(self.x - 1, self.y),
            self.get_cell_by_axis(self.x - 1, self.y + 1),
            self.get_cell_by_axis(self.x, self.y - 1),
            self.get_cell_by_axis(self.x + 1, self.y - 1),
            self.get_cell_by_axis(self.x + 1, self.y),
            self.get_cell_by_axis(self.x + 1, self.y + 1),
            self.get_cell_by_axis(self.x, self.y + 1)
        ]

        cells = [cell for cell in cells if cell is not None]
        return cells
    
    @property
    def surrounded_cells_mines_amount(self):
        counter = 0
        for cell in self.surrounded_cells:
            if cell.is_mine:
                counter += 1
        
        return counter

    def show_cell(self):
        if not self.is_opened:
            Cell.cell_count -= 1
            self.cell_btn_object.configure(
                text=self.surrounded_cells_mines_amount,
                bg=settings.themes[settings.current_theme]["cell_bg"],
                fg=settings.themes[settings.current_theme]["text"]
            )
            # REPLACE / REDUCE CELL COUNT LABEL ONCE A CELL IS CLICKED
            if Cell.cell_count_label_object:
                Cell.cell_count_label_object.configure(
                    text = f'Cells Left:{Cell.cell_count}'
                )
            self.cell_btn_object.configure(bg=settings.themes[settings.current_theme]["cell_bg"])
        self.is_opened = True

    def show_mine(self):
        if Cell.mines_left_label_object:
            Cell.mines_left_label_object.configure(
                text=f'Mines Left:{settings.mines_count - self.surrounded_cells_mines_amount}')
        self.cell_btn_object.configure(bg=settings.themes[settings.current_theme]["mine"]) # CHANGE THE CELL COLOR TO RED WHEN THE CELL IS GENERATED AS MINE
        if settings.mines_count - self.surrounded_cells_mines_amount == 0:
            game_window = self.cell_btn_object.winfo_toplevel()
            x = game_window.winfo_x() + (game_window.winfo_width() / 2) - 200
            y = game_window.winfo_y() + (game_window.winfo_height() / 2) - 100
            root = tk.Tk()
            root.title("Game Over")
            root.iconbitmap("videogame.ico")
            label = tk.Label(root, text="Game Over! You hit a mine!", font=("Lucida Console", 12))
            label.pack(padx=20, pady=20)
            def on_closing():
                root.destroy()
                sys.exit()
            button = tk.Button(root, text="OK", width=8, height=2, font=("Arial", 7), command=on_closing)
            button.pack(pady=2)
            root.geometry(f'450x125+{int(x)}+{int(y)}')
            root.resizable(False, False)
            root.mainloop()

    def right_click_actions(self, event): # RIGHT CLICK
        if not self.is_opened:
            if not self.is_mine_candidate:
                self.is_mine_candidate = True
                settings.mines_count -= 1
                self.cell_btn_object.configure(
                    bg=settings.themes[settings.current_theme]["flag"]
                )
                if Cell.mines_left_label_object:
                    Cell.mines_left_label_object.configure(
                        text=f'Mines Left:{settings.mines_count}'
                    )
                if settings.mines_count == 0:
                    game_window = self.cell_btn_object.winfo_toplevel()
                    x = game_window.winfo_x() + (game_window.winfo_width() / 2) - 200
                    y = game_window.winfo_y() + (game_window.winfo_height() / 2) - 100
                    root = tk.Tk()
                    root.title("Game Over")
                    root.iconbitmap("videogame.ico")
                    label = tk.Label(root, text="Congratulations! You cleared all the mines!", font=("Lucida Console", 12))
                    label.pack(padx=20, pady=20)
                    def on_closing():
                        root.destroy()
                        sys.exit()
                    button = tk.Button(root, text="OK", width=8, height=2, font=("Arial", 7), command=on_closing)
                    button.pack(pady=2)
                    root.geometry(f'470x125+{int(x)}+{int(y)}')
                    root.resizable(False, False)
                    root.mainloop()
            else:
                self.is_mine_candidate = False
                settings.mines_count += 1
                self.cell_btn_object.configure(
                    bg=settings.themes[settings.current_theme]["cell_bg"]
                )
                if Cell.mines_left_label_object:
                    Cell.mines_left_label_object.configure(
                        text=f'Mines Left:{settings.mines_count}'
                    )

    @staticmethod
    def randomize_mines(): # FUNCTION TO GENERATE RANDOM MINES
        picked_cells = random.sample(
            Cell.all,
            settings.mines_count # AMOUNT OF RANDOM GENERATED MINES PER GAME
            )
        for picked_cell in picked_cells:
            picked_cell.is_mine = True

    def __repr__(self):
        return f"Cell({self.x}, {self.y})"