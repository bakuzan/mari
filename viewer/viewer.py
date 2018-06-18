import tkinter


class Container(tkinter.Frame):
    def __init__(self):
        self.display = tkinter.Text()
        self.display.pack()
        self.alert = tkinter.Text()
        self.alert.pack()


class Viewer(tkinter.Tk):
    def __init__(self):
        self.title = 'Maze escape'


if __name__ == '__main__':
    gui = Viewer()
    gui.mainloop()
