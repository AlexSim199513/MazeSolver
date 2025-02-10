from tkinter import Tk, BOTH, Canvas
import time, random

# Class creating the window that the maze is drawn to
class Window:
    def __init__(self, width, height):
        self.__root = Tk()
        self.__root.title("Your title here!")
        self.__root.geometry(f"{width}x{height}")
        self.__canvas = Canvas(self.__root, width=width, height=height)
        self.__canvas.pack(fill=BOTH, expand=True)
        self.__running = False
        self.__root.protocol("WM_DELETE_WINDOW", self.close)

    def redraw(self):
        self.__root.update_idletasks()
        self.__root.update()

    def wait_for_close(self):
        self.__running = True
        while self.__running:
            self.redraw()

    def close(self):
        self.__running = False

    def draw_line(self, line, fill_color):
        line.draw(self.__canvas, fill_color)

# Class for (x, y) coordinates to create lines, cells , etc
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

# Class for the individual lines drawn while solving maze or the walls of individual cells
class Line:
    def __init__(self, point1, point2):
        self.point1 = point1
        self.point2 = point2

    def draw(self, canvas, fill_color):
        canvas.create_line(self.point1.x, self.point1.y, self.point2.x, self.point2.y, fill=fill_color, width=2)

# Class for the individual squares creating the maze
class Cell:
    def __init__(self, _x1, _x2, _y1, _y2, _win, left_wall = True, right_wall = True, top_wall = True, bottom_wall = True, visited = False):
        self._x1 = _x1
        self._x2 = _x2
        self._y1 = _y1
        self._y2 = _y2
        self._win = _win
        self.left_wall = left_wall
        self.right_wall = right_wall
        self.top_wall = top_wall
        self.bottom_wall = bottom_wall
        self.top_left = Point(self._x1, self._y1)
        self.top_right = Point(self._x2, self._y1)
        self.bottom_left = Point(self._x1, self._y2)
        self.bottom_right = Point(self._x2, self._y2)
        self.visited = visited

    # Draws the individual Cells of the Maze
    def draw(self):
        if self._win is not None:
            color = "black" if self.top_wall else "white"
            top_line = Line(self.top_left, self.top_right)
            self._win.draw_line(top_line, color)

            color = "black" if self.bottom_wall else "white"
            bottom_line = Line(self.bottom_left, self.bottom_right)
            self._win.draw_line(bottom_line, color)

            color = "black" if self.left_wall else "white"
            left_line = Line(self.top_left, self.bottom_left)
            self._win.draw_line(left_line, color)

            color = "black" if self.right_wall else "white"
            right_line = Line(self.top_right, self.bottom_right)
            self._win.draw_line(right_line, color)
            

    # Draws the line between Cells during the solving
    def draw_move(self, target_cell, undo=False):
        self_center = Point((self._x1 + self._x2) / 2, (self._y1 + self._y2) /2)
        target_center = Point((target_cell._x1 + target_cell._x2) / 2, (target_cell._y1 + target_cell._y2) /2)
        new_line = Line(self_center, target_center)
        if undo:
            new_line.draw(self._win, "gray")
        else:
            new_line.draw(self._win, "red")
            
class Maze:
    def __init__(self, x1, y1, num_rows, num_cols, cell_size_x, cell_size_y, win = None, seed = None):
        self.x1 = x1
        self.y1 = y1
        self.num_rows = num_rows
        self.num_cols = num_cols
        self.cell_size_x = cell_size_x
        self.cell_size_y = cell_size_y
        self.win = win
        self._create_cells()

        if seed is not None:
            self.seed = seed
            random.seed(seed)

# initiates and fills the self._cells as well as drawing them to the board.
    def _create_cells(self):
        self._cells = []
        for i in range(self.num_cols):
            cell_col = []
            for j in range(self.num_rows):
                new_x1 = (self.cell_size_x * i) + self.x1
                new_x2 = (self.cell_size_x * (i + 1)) + self.x1
                new_y1 = (self.cell_size_y * j) + self.y1
                new_y2 = (self.cell_size_y * (j + 1)) + self.y1
                new_cell = Cell(new_x1, new_x2, new_y1, new_y2, self.win)
                cell_col.append(new_cell)
            self._cells.append(cell_col)

        for i in range(self.num_cols):
            for j in range(self.num_rows):
                self._draw_cell(i, j)
                
    # Loops through the cells array and calls the draw method on each one individually
    def _draw_cell(self, i, j):
        if self.win is not None:
            self._cells[i][j].draw()
            self._animate()

    #Pauses the _draw_cell method to make it easier to follow to maze drawing process
    def _animate(self):
        self.win.redraw()
        time.sleep(0.05)

    #always ensures there is an entry and exit it the top left and bottom right cells respectively
    def _break_entrance_and_exit(self):
        self._cells[0][0].top_wall = False
        #Redraws the entry cell after changing the top wall to an entrance
        self._draw_cell(self._cells[0][0])

        self._cells[self.num_cols - 1][self.num_rows - 1].bottom_wall = False
        #Redraws the exit cell after changing the bottom wall to an exit
        self._draw_cell(self._cells[self.num_cols - 1][self.num_rows - 1])

    def _break_Walls_r(self, i, j):
        
        self._cells[i][j].visited = True
        self._cells[i][j].draw()

        while True:
            directions = []

            # Check the Cell above
            if i - 1 >= 0:
                if not self._cells[i -1][j].visited:
                    directions.append((i - 1, j))

            # Check the Cell Below
            if (i +1) < len(self._cells):
                if not self._cells[i + 1][j].visited:
                    directions.append((i + 1, j))

            #Checks to the left
            if j - 1 >= 0:
                if not self._cells[i][j -1].visited:
                    directions.append((i, j - 1))

            # Checks to the right
            if j + 1 < len(self._cells[0]):
                if not self._cells[i][j + 1].visited:
                    directions.append((i, j + 1))

            # Breaks the recursion if no route is found
            if len(directions) == 0:
                self._cells[i][j].draw()
                return

            next_i, next_j = random.choice(directions)

            # Checks if the next cell is above 
            if next_i < i:
                self._cells[i][j].top_wall = False
                self._cells[next_i][j].bottom_wall = False

            # Checks if the next cell is below
            if next_i > i:
                self._cells[i][j].bottom_wall = False
                self._cells[next_i][j].top_wall = False

            # Checks if next cell is to the left
            if next_j < j:
                self._cells[i][j].left_wall = False
                self._cells[next_i][next_j].right_wall = False

            # Checks if next cell is to the right
            if next_j > j:
                self._cells[i][j].right_wall = False
                self._cells[next_i][next_j].left_wall = False

            # Recursively calls the next layer of the function
            self._break_Walls_r(next_i, next_j)


def main():
    win = Window(800, 600)
    first_cell = Cell(200, 240, 200, 240, win, True, True, True, True)
    first_cell.draw()
    second_cell = Cell(400, 440, 400 , 440, win, False, False, True, True)
    second_cell.draw()
    win.wait_for_close()

# This ensures main() only runs if this file is run directly
if __name__ == "__main__":
    main() 