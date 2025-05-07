import customtkinter as ctk
import tkinter as tk
import WOM_MAZE_LOGIC as logic

# Configure CustomTkinter theme
ctk.set_appearance_mode('light')
ctk.set_default_color_theme('green')  # Use default theme

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

        # Main container
        main_container = ctk.CTkFrame(self)
        main_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Header
        header = ctk.CTkFrame(main_container, fg_color='#8B4513')  # Brown color
        header.pack(fill=tk.X, pady=(0, 10))
        ctk.CTkLabel(header, text='Mud Maze', 
                    font=('Arial', 24, 'bold'), 
                    text_color='white').pack(pady=10)

        # Content area
        content = ctk.CTkFrame(main_container)
        content.pack(fill=tk.BOTH, expand=True)

        # Left control panel
        control = ctk.CTkFrame(content, width=300, fg_color='#8B4513')  # Brown color
        control.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
        control.pack_propagate(False)

        # Control panel title
        ctk.CTkLabel(control, text='Control Panel', 
                    font=('Arial', 18, 'bold'),
                    text_color='white').pack(pady=(20, 10))

        # Grid size control
        ctk.CTkLabel(control, text='Grid Size', 
                    text_color='white').pack(pady=(10, 2))
        self.size_slider = ctk.CTkSlider(control, from_=20, to=100, 
                                       command=self.update_grid_size)
        self.size_slider.set(self.grid_size)
        self.size_slider.pack(pady=(0, 5))
        self.size_label = ctk.CTkLabel(control, text=str(self.grid_size),
                                     text_color='white')
        self.size_label.pack()

        # Maze generation options
        ctk.CTkLabel(control, text='Maze Generation', 
                    text_color='white').pack(pady=(20, 2))
        self.maze_type = ctk.CTkComboBox(control, 
                                       values=['Recursive Backtracking', 'Prim', 'Kruskal'],
                                       width=200)
        self.maze_type.set('Recursive Backtracking')
        self.maze_type.pack(pady=(0, 10))

        # Generate button
        self.generate_btn = ctk.CTkButton(control, text='Generate Maze',
                                        command=self.generate_maze,
                                        width=200)
        self.generate_btn.pack(pady=5)

        # Canvas area
        canvas_frame = ctk.CTkFrame(content, fg_color='white')
        canvas_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        self.canvas = tk.Canvas(canvas_frame, bg='white')
        self.canvas.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Bind events
        self.canvas.bind('<Configure>', lambda e: self.draw_grid(self.grid_size))
        self.canvas.bind('<Button-1>', self.on_canvas_left_click)
        self.canvas.bind('<Button-3>', self.on_canvas_right_click)

        # Initialize grid
        self.draw_grid(self.grid_size)

    def update_grid_size(self, value):
        """Update grid size from slider."""
        self.grid_size = int(value)
        self.size_label.configure(text=str(self.grid_size))
        self.draw_grid(self.grid_size)

    def draw_grid(self, n):
        """Draw n x n grid with square cells."""
        self.canvas.delete('all')
        w, h = self.canvas.winfo_width(), self.canvas.winfo_height()
        
        # Calculate cell size and padding
        cell = min(w / n, h / n)
        total = cell * n
        pad_x = (w - total) / 2
        pad_y = (h - total) / 2
        
        # Store grid metrics
        self.cell_size = cell
        self.pad_x = pad_x
        self.pad_y = pad_y
        
        # Create cells
        self.cells = {}
        for row in range(n):
            for col in range(n):
                x1 = pad_x + col * cell
                y1 = pad_y + row * cell
                x2 = x1 + cell
                y2 = y1 + cell
                # Set initial color based on grid_data if it exists
                fill_color = 'black' if (self.grid_data is not None and 
                                       self.grid_data[row][col] == 1) else 'white'
                rect = self.canvas.create_rectangle(x1, y1, x2, y2, 
                                                 fill=fill_color, outline='gray')
                self.cells[(row, col)] = rect

        # Set default start/end if not set
        if self.start not in self.cells:
            self.start = (0, 0)
        if self.end not in self.cells:
            self.end = (n-1, n-1)

        # Draw start/end icons
        self.draw_start_end_icons()

    def draw_start_end_icons(self):
        """Draw start and end icons on the grid."""
        if not hasattr(self, 'cells'):
            return

        # Clear any existing icons first
        for item in self.canvas.find_all():
            if item not in self.cells.values():  # Keep only the grid cells
                self.canvas.delete(item)

        # Draw start icon (flag)
        if self.start in self.cells:
            x = self.pad_x + self.start[1] * self.cell_size
            y = self.pad_y + self.start[0] * self.cell_size
            # Draw flag pole
            self.canvas.create_line(x + self.cell_size*0.2, y + self.cell_size*0.2,
                                  x + self.cell_size*0.2, y + self.cell_size*0.8,
                                  fill='black', width=2)
            # Draw flag
            points = [
                x + self.cell_size*0.2, y + self.cell_size*0.2,  # pole top
                x + self.cell_size*0.7, y + self.cell_size*0.4,  # flag tip
                x + self.cell_size*0.2, y + self.cell_size*0.6   # pole middle
            ]
            self.canvas.create_polygon(points, fill='brown', outline='black')

        # Draw end icon (target)
        if self.end in self.cells:
            x = self.pad_x + self.end[1] * self.cell_size
            y = self.pad_y + self.end[0] * self.cell_size
            center_x = x + self.cell_size/2
            center_y = y + self.cell_size/2
            # Draw concentric circles with fixed step size
            max_radius = int(self.cell_size * 0.4)
            step = max(1, int(self.cell_size * 0.1))  # Ensure step is at least 1
            for r in range(max_radius, 0, -step):
                self.canvas.create_oval(center_x-r, center_y-r,
                                     center_x+r, center_y+r,
                                     outline='brown', width=2)
            # Draw center dot
            dot_radius = max(1, int(self.cell_size * 0.1))
            self.canvas.create_oval(center_x-dot_radius,
                                  center_y-dot_radius,
                                  center_x+dot_radius,
                                  center_y+dot_radius,
                                  fill='brown', outline='brown')

    def pixel_to_cell(self, x, y):
        """Convert canvas coordinates to grid cell indices."""
        if self.cell_size is None:
            return None, None
        col = int((x - self.pad_x) / self.cell_size)
        row = int((y - self.pad_y) / self.cell_size)
        return row, col

    def on_canvas_left_click(self, event):
        """Handle left-click to set start point."""
        r, c = self.pixel_to_cell(event.x, event.y)
        if r is None or not (0 <= r < self.grid_size and 0 <= c < self.grid_size):
            return
        # Check if clicked on wall
        if self.grid_data is not None and self.grid_data[r][c] == 1:
            return
        # Check if clicked on end point
        if self.end == (r, c):
            return
        # Remove old start point
        if self.start is not None:
            # Restore original color of previous start cell
            if self.grid_data is not None:
                color = 'black' if self.grid_data[self.start[0]][self.start[1]] == 1 else 'white'
            else:
                color = 'white'
            self.canvas.itemconfig(self.cells[self.start], fill=color)
        # Set new start point
        self.start = (r, c)
        self.draw_start_end_icons()

    def on_canvas_right_click(self, event):
        """Handle right-click to set end point."""
        r, c = self.pixel_to_cell(event.x, event.y)
        if r is None or not (0 <= r < self.grid_size and 0 <= c < self.grid_size):
            return
        # Check if clicked on wall
        if self.grid_data is not None and self.grid_data[r][c] == 1:
            return
        # Check if clicked on start point
        if self.start == (r, c):
            return
        # Remove old end point
        if self.end is not None:
            # Restore original color of previous end cell
            if self.grid_data is not None:
                color = 'black' if self.grid_data[self.end[0]][self.end[1]] == 1 else 'white'
            else:
                color = 'white'
            self.canvas.itemconfig(self.cells[self.end], fill=color)
        # Set new end point
        self.end = (r, c)
        self.draw_start_end_icons()

    def generate_maze(self):
        """Generate a new maze."""
        n = self.grid_size
        self.grid_data = logic.generate_maze(n, self.maze_type.get(), 'Mud Maze')
        # Add loops for alternative paths
        if self.start is not None and self.end is not None:
            self.grid_data = logic.add_targeted_loops(self.grid_data, self.start, self.end, loops=3)
        # Draw walls
        for (r, c), rect in self.cells.items():
            color = 'black' if self.grid_data[r][c] == 1 else 'white'
            self.canvas.itemconfig(rect, fill=color)
        # Reset start/end if they are on walls
        if self.start is not None and self.grid_data[self.start[0]][self.start[1]] == 1:
            self.start = None
        if self.end is not None and self.grid_data[self.end[0]][self.end[1]] == 1:
            self.end = None
        # Set default start/end if needed
        if self.start is None:
            self.start = (0, 0)
        if self.end is None:
            self.end = (n-1, n-1)
        # Redraw start/end icons
        self.draw_start_end_icons()

if __name__ == '__main__':
    app = MudMazeApp()
    app.mainloop() 