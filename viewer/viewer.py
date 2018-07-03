import os
import tkinter as tk

__dirname = os.path.dirname(__file__)
window_icon = os.path.join(__dirname, '../assets/icon.ico')


class Viewer:
    """
    GUI to display game controls
    """

    def __init__(self, **kwargs):
        (dw, dh) = kwargs.pop('dimensions', (0, 0))
        on_play, on_user_input, on_reset = kwargs.pop(
            'on_play', None), kwargs.pop('on_user_input', None), kwargs.pop('on_reset', None)

        self.__on_user_input = on_user_input
        self.__on_play = on_play
        self.__on_reset = on_reset

        self.__root = tk.Tk()
        self.__root.iconbitmap(default=window_icon)
        self.__root.title('Mari - Maze escape')
        self.__root.bind('<KeyPress>', self.__handle_key_press)

        self.__message = tk.StringVar()

        self.__container = tk.Frame(self.__root)
        self.__container.grid(ipadx=5, ipady=5)

        self.__info = tk.Label(self.__container, text=self._get_info())
        self.__info.grid()

        self.__button_frame = tk.Frame(self.__container)
        self.__button_frame.grid(row=2, column=0, columnspan=4)

        self.__play = tk.Button(self.__button_frame,
                                text="Play", width=25, command=self.play_game, state=tk.DISABLED)
        self.__play.grid(row=0, column=1)

        self.__reset = tk.Button(self.__button_frame, text="Reset",
                                 width=25, command=self.reset_game, state=tk.DISABLED)
        self.__reset.grid(row=0, column=2)

        display_width = (2 * dw) + 1
        display_height = (2 * dh) + 1
        self.__display = tk.Text(
            self.__container, state=tk.DISABLED, width=display_width, height=display_height)
        self.__display.grid(padx=5, pady=5)

        self.__alert = tk.Label(self.__container, textvariable=self.__message)
        self.__alert.grid()

    def start(self):
        print('start')
        self.__root.mainloop()

    def enable_game(self):
        self.__play.configure(state=tk.NORMAL)

    def play_game(self):
        self.__on_play()
        self.__play.configure(state=tk.DISABLED)

    def enable_new_game(self):
        self.__reset.configure(state=tk.NORMAL)

    def reset_game(self):
        self.__on_reset()
        self.__reset.configure(state=tk.DISABLED)
        self.set_alert("")

    def call(self, delay, action, arg=None):
        print('call')
        self.__root.after(delay, action, arg)

    def update(self, text):
        self.__display.configure(state=tk.NORMAL)
        self.__display.delete(0.0, 'end')
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
        if event.keysym != 'Escape':
            if self.__on_user_input:
                self.__on_user_input(event.keysym)
                self.__root.update_idletasks()
            else:
                print(event.keysym)
        else:
            print('Quitting...')
            self.__root.quit()


if __name__ == '__main__':
    import time
    gui = Viewer()
    gui.start()
    # time.sleep(5)
    gui.update("GOGOGOGOG")
    gui.set_alert("this sucks")
