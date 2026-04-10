import tkinter as tk
from queue import PriorityQueue

# Grid size
ROWS, COLS = 20, 20
cells = [[None for _ in range(COLS)] for _ in range(ROWS)]

# Start and End points
start = None
end = None

# Colors
EMPTY_COLOR = "white"
WALL_COLOR = "black"
START_COLOR = "green"
END_COLOR = "red"
PATH_COLOR = "yellow"

# Heuristic function (Manhattan distance)
def h(p1, p2):
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])

# Reset the grid
def reset_grid():
    global start, end
    start = None
    end = None
    for i in range(ROWS):
        for j in range(COLS):
            cells[i][j].config(bg=EMPTY_COLOR)

# Click event to set start, end, or walls
def on_click(event, row, col):
    global start, end
    current_color = cells[row][col].cget("bg")
    
    if start is None and current_color == EMPTY_COLOR:
        start = (row, col)
        cells[row][col].config(bg=START_COLOR)
    elif end is None and current_color == EMPTY_COLOR:
        end = (row, col)
        cells[row][col].config(bg=END_COLOR)
    elif current_color == EMPTY_COLOR:
        cells[row][col].config(bg=WALL_COLOR)
    elif current_color == WALL_COLOR:
        cells[row][col].config(bg=EMPTY_COLOR)

# Reconstruct path after A* finds end
def reconstruct_path(came_from, current):
    while current in came_from:
        current = came_from[current]
        if current != start:
            cells[current[0]][current[1]].config(bg=PATH_COLOR)

# A* Algorithm
def a_star():
    if not start or not end:
        print("Set start and end points first!")
        return
    
    open_set = PriorityQueue()
    open_set.put((0, start))
    came_from = {}
    
    g_score = { (i,j): float("inf") for i in range(ROWS) for j in range(COLS) }
    g_score[start] = 0
    
    f_score = { (i,j): float("inf") for i in range(ROWS) for j in range(COLS) }
    f_score[start] = h(start, end)
    
    open_set_hash = {start}
    
    while not open_set.empty():
        current = open_set.get()[1]
        open_set_hash.remove(current)
        
        if current == end:
            reconstruct_path(came_from, end)
            return
        
        neighbors = get_neighbors(current)
        for neighbor in neighbors:
            temp_g_score = g_score[current] + 1
            
            if temp_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = temp_g_score
                f_score[neighbor] = temp_g_score + h(neighbor, end)
                if neighbor not in open_set_hash:
                    open_set.put((f_score[neighbor], neighbor))
                    open_set_hash.add(neighbor)
                    if neighbor != end:
                        cells[neighbor[0]][neighbor[1]].config(bg="lightblue")

# Get valid neighbors (no walls, inside grid)
def get_neighbors(pos):
    neighbors = []
    row, col = pos
    for d_row, d_col in [(-1,0),(1,0),(0,-1),(0,1)]:
        r, c = row + d_row, col + d_col
        if 0 <= r < ROWS and 0 <= c < COLS:
            if cells[r][c].cget("bg") != WALL_COLOR:
                neighbors.append((r,c))
    return neighbors

# Create GUI
root = tk.Tk()
root.title("A* Pathfinding Visualization")

frame = tk.Frame(root)
frame.pack()

for i in range(ROWS):
    for j in range(COLS):
        cell = tk.Label(frame, width=2, height=1, bg=EMPTY_COLOR, borderwidth=1, relief="solid")
        cell.grid(row=i, column=j)
        cell.bind("<Button-1>", lambda e, r=i, c=j: on_click(e, r, c))
        cells[i][j] = cell

# Buttons
button_frame = tk.Frame(root)
button_frame.pack(pady=10)

start_button = tk.Button(button_frame, text="Run A*", command=a_star)
start_button.pack(side="left", padx=5)

reset_button = tk.Button(button_frame, text="Reset Grid", command=reset_grid)
reset_button.pack(side="left", padx=5)

root.mainloop()