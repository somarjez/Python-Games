from tkinter import *
from cell import Cell  
import settings
import utilities
from tkinter import ttk

def start_game():
    main_menu.withdraw()  # Hide the main menu window
    show_difficulty_options()

def show_difficulty_options():
    difficulty_window.deiconify()  # Show the difficulty window

def set_difficulty(difficulty):
    if difficulty == "easy":
        settings.grid_size = 8
        settings.mines_count = 10
    elif difficulty == "moderate":
        settings.grid_size = 12
        settings.mines_count = 30
    elif difficulty == "hard":
        settings.grid_size = 16
        settings.mines_count = 60

    difficulty_window.withdraw()  # Hide the difficulty window
    create_game_window()

def create_game_window():
    global center_frame
    game_window = Tk()
    game_window.configure(bg='black')
    game_window.title('Minesweeper')
    game_window.iconbitmap(r"C:\Users\jramo\Downloads\PYTHON GAMES\scripts\videogame.ico")

    # Center the game window
    screen_width = game_window.winfo_screenwidth()
    screen_height = game_window.winfo_screenheight()
    window_width = settings.width
    window_height = settings.height
    x = (screen_width - window_width) // 2
    y = (screen_height - window_height) // 2
    game_window.geometry(f'{window_width}x{window_height}')
    game_window.geometry(f'+{x}+{y}')

    # Set minimum and maximum window size
    game_window.minsize(360, 360)
    game_window.maxsize(window_width, window_height)

    # Allow window resizing
    game_window.resizable(True, True)

    top_frame = Frame(
        game_window,
        bg=settings.themes[settings.current_theme]["frame_bg"],
        width=settings.width,
        height=utilities.height_percentage(13)
    )
    top_frame.pack(fill='x', side='top')

    game_title = Label(
        top_frame,
        bg=settings.themes[settings.current_theme]["frame_bg"],
        text='MINESWEEPER',
        font=('Lucida Console', 36, 'bold'),
        fg=settings.themes[settings.current_theme]["text"],
    )
    game_title.pack(expand=True)

    center_frame = Frame(
        game_window,
        bg='gray',
        width=settings.width,
        height=utilities.height_percentage(85)
    )
    center_frame.pack(fill='both', expand=True)

    # Manage cells
    for x in range(settings.grid_size):
        for y in range(settings.grid_size):
            c = Cell(x, y)
            c.create_btn_object(center_frame)
            c.cell_btn_object.grid(
                column=x,
                row=y,
                sticky='nsew'
            )

    # Configure grid to expand
    for x in range(settings.grid_size):
        center_frame.columnconfigure(x, weight=1)
        center_frame.rowconfigure(x, weight=1)

    # Display 'Cells Left' label
    Cell.create_cell_count_label(top_frame)
    Cell.cell_count_label_object.pack(side='left', padx=10)

    # Display 'Mines Left' label
    Cell.create_mines_left_label(top_frame)
    Cell.mines_left_label_object.pack(side='right', padx=10)

    Cell.randomize_mines()

    # Set game over state for testing
    Cell.game_over = True

    game_window.mainloop()

def rgb_to_hex(rgb):
    return '#%02x%02x%02x' % rgb

def center_window(window, width, height):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2
    window.geometry(f'{width}x{height}+{x}+{y}')

def change_theme(theme):
    settings.current_theme = theme
    # Update main menu theme
    main_menu.configure(bg=settings.themes[theme]["background"])
    start_button.configure(bg=settings.themes[theme]["cell_bg"], fg=settings.themes[theme]["text"])
    exit_button.configure(bg=settings.themes[theme]["cell_bg"], fg=settings.themes[theme]["text"])
    theme_label.configure(bg=settings.themes[theme]["background"], fg=settings.themes[theme]["text"])
    
    # Update difficulty window theme
    difficulty_window.configure(bg=settings.themes[theme]["background"])
    easy_button.configure(bg=settings.themes[theme]["cell_bg"], fg=settings.themes[theme]["text"])
    moderate_button.configure(bg=settings.themes[theme]["cell_bg"], fg=settings.themes[theme]["text"])
    hard_button.configure(bg=settings.themes[theme]["cell_bg"], fg=settings.themes[theme]["text"])

def show_main_menu():
    main_menu.deiconify()

# Main menu window
main_menu = Tk()
main_menu.title('Main Menu')
main_menu.iconbitmap(r"C:\Users\jramo\Downloads\PYTHON GAMES\scripts\videogame.ico")
main_menu.geometry('280x130')
center_window(main_menu, 280, 130)  # Center the main menu window

start_button = Button(main_menu, text="Start Game", font=("Lucida Console", 10), command=start_game, width=15, height=2)
start_button.place(x=140, y=58, anchor='center')

exit_button = Button(main_menu, text="Exit", font=("Lucida Console", 10), command=main_menu.quit, width=15, height=2)
exit_button.place(x=140, y=98, anchor='center')

# Difficulty window
difficulty_window = Toplevel(main_menu)
difficulty_window.title('Select Difficulty')
difficulty_window.iconbitmap(r"C:\Users\jramo\Downloads\PYTHON GAMES\scripts\videogame.ico")
difficulty_window.geometry('300x200')
difficulty_window.resizable(False, False)
center_window(difficulty_window, 300, 200)  # Center the difficulty window
difficulty_window.withdraw()  # Hide initially

# Difficulty buttons
easy_button = Button(difficulty_window, text="Easy", font=("Lucida Console", 10), command=lambda: set_difficulty("easy"), width=25, height=2)
easy_button.place(x=150, y=60, anchor='center')

moderate_button = Button(difficulty_window, text="Moderate", font=("Lucida Console", 10), command=lambda: set_difficulty("moderate"), width=25, height=2)
moderate_button.place(x=150, y=100, anchor='center')

hard_button = Button(difficulty_window, text="Hard", font=("Lucida Console", 10), command=lambda: set_difficulty("hard"), width=25, height=2)
hard_button.place(x=150, y=140, anchor='center')

# Allow window resizing
main_menu.resizable(False, False)

# Add this after creating main menu buttons but before mainloop
theme_label = Label(main_menu, text="Theme:", font=("Lucida Console", 10),
                   bg=settings.themes[settings.current_theme]["background"],
                   fg=settings.themes[settings.current_theme]["text"])
theme_label.place(x=100, y=25, anchor='center')

style = ttk.Style()
style.configure('Custom.TCombobox', padding=2, font=('Lucida Console', 10))

theme_var = StringVar(value=settings.current_theme)
theme_combo = ttk.Combobox(main_menu, textvariable=theme_var, values=["Light", "Dark", "System"], 
                          state="readonly", width=9, style='Custom.TCombobox')
theme_combo.place(x=166, y=25, anchor='center')
theme_combo.bind('<<ComboboxSelected>>', lambda e: change_theme(theme_var.get()))

# Run the main menu window
main_menu.mainloop()