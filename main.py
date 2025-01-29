from tkinter import Tk, BOTH, Canvas

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


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Line:
    def __init__(self, point1, point2):
        self.point1 = point1
        self.point2 = point2

    def draw(self, canvas, fill_color):
        canvas.create_line(self.point1.x, self.point1.y, self.point2.x, self.point2.y, fill=fill_color, width=2)

class Cell:
    def __init__(self, _x1, _x2, _y1, _y2, _win, left_wall = True, right_wall = True, top_wall = True, bottom_wall = True):
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

    def draw(self):
        if self.top_wall:
            top_line = Line(self.top_left, self.top_right)
            self._win.draw_line(top_line, "black")
        if self.bottom_wall:
            bottom_line = Line(self.bottom_left, self.bottom_right)
            self._win.draw_line(bottom_line, "black")
        if self.left_wall:
            left_line = Line(self.top_left, self.bottom_left)
            self._win.draw_line(left_line, "black")
        if self.right_wall:
            right_line = Line(self.top_right, self.bottom_right)
            self._win.draw_line(right_line, "black")
    
    def draw_move(self, target_cell, undo=False):
        self_center = Point((self._x1 + self._x2) / 2, (self._y1 + self._y2) /2)
        target_center = Point((target_cell._x1 + target_cell._x2) / 2, (target_cell._y1 + target_cell._y2) /2)
        new_line = Line(self_center, target_center)
        if undo:
            new_line.draw(self._win, "gray")
        else:
            new_line.draw(self._win, "red")

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