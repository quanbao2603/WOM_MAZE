import customtkinter as ctk
import tkinter as tk
import WOM_MAZE_LOGIC as logic

# Configure CustomTkinter theme
ctk.set_appearance_mode('light')
ctk.set_default_color_theme('brown')

class MudMazeApp(ctk.CTk):
    """Window for Mud Maze variant solver."""
    def __init__(self):
        super().__init__()
        self.title('Mud Maze')
        self.state('zoomed')
        self.grid_size = 20  # Default grid size
        self.grid_data = None
        self.start = None
        self.end = None
        self.cell_size = None
        self.pad_x = None
        self.pad_y = None

        # Main cont