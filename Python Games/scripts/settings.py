width = 899
height = 902
grid_size = 6
cell_count = grid_size ** 2
mines_count = (cell_count) // 4 # FORMULA -> 6^2 FLOOR DIVIDED BY 4 = 9

# Theme colors
current_theme = "System"  # Can be "light", "Dark", or "System"

themes = {
    "Light": {
        "background": "SystemButtonFace",
        "cell_bg": "SystemButtonFace",
        "frame_bg": "#969696",
        "text": "SystemButtonText",
        "mine": "#FF0000",
        "flag": "#FFA500"
    },
    "Dark": {
        "background": "#1E1E1E",
        "cell_bg": "#2D2D2D",
        "frame_bg": "#404040",
        "text": "#FFFFFF",
        "mine": "#FF4444",
        "flag": "#FFB86C"
    },
    "System": {
        "background": "SystemButtonFace",
        "cell_bg": "SystemButtonFace",
        "frame_bg": "#969696",
        "text": "SystemButtonText",
        "mine": "#FF0000",
        "flag": "#FFA500"
    }
}
