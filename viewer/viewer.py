import tkinter as tk


class Viewer:
    def __init__(self, on_user_input=None):
        self.__on_user_input = on_user_input
        self.__root = tk.Tk()
        self.__root.title('Maze escape')
        self.__root.bind('<KeyPress>', self.__handle_key_press)

        self.__message = tk.StringVar()

        self.__container = tk.Frame(self.__root)
        self.__container.pack()

        self.__info = tk.Label(self.__container, text=self._get_info())
        self.__info.pack()

        self.__display = tk.Text(self.__container, state=tk.DISABLED)
        self.__display.pack()

        self.__alert = tk.Label(self.__container, textvariable=self.__message)
        self.__alert.pack()

    def start(self):
        self.__root.mainloop()

    def call(self, delay, action):
        self.__root.after(delay, action)

    def update(self, text):
        self.__display.configure(state=tk.NORMAL)
        self.__display.delete(1.0, 'end')
        self.__display.insert(0.0, text)
        self.__display.configure(state=tk.DISABLED)
        self.__root.update_idletasks()

    def set_alert(self, text):
        self.__message.set(text)
        self.__root.update_idletasks()

    """
    internals
    """

    def _get_info(self):
        return "Help Mari escape the maze!\nUse the WASD or the arrow keys to move Mari"

    def __handle_key_press(self, event):
        print(event.keysym)
        if event.keysym != 'Escape':
            if self.__on_user_input:
                self.__on_user_input(event.keysym)
            else:
                print(event.keysym)
        else:
            self.__root.quit()


if __name__ == '__main__':
    import time
    gui = Viewer()
    gui.start()
    # time.sleep(5)
    gui.update("GOGOGOGOG")
    gui.set_alert("this sucks")
