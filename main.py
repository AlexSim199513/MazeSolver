from tkinter import Tk, BOTH, Canvas

class Window:
    def __init__(self, width, height):
        self.__root = Tk()
        self.__root.title("Your title here!")
        self.__canvas = Canvas(self.__root, expand=BOTH)
        self.__canvas.pack()
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

def main():
    win = Window(800, 600)
    win.wait_for_close()

# This ensures main() only runs if this file is run directly
if __name__ == "__main__":
    main() 