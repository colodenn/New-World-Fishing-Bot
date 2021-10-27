
# Standard Library
from tkinter import *
from typing import Callable, Any
import sys


def close(_):
    sys.exit()


class Overlay:
    """
    Creates an overlay window using tkinter
    Uses the "-topmost" property to always stay on top of other Windows
    """

    def __init__(self):
        self.root = Tk()
        self.test = "test"

        self.test = StringVar()

        self.exit_button = Label(
            self.root,
            text=' X |',
            font=('Consolas', '14'),
            fg='green3',
            bg='grey19'
        )
        self.exit_button.bind("<Button-1>", close)
        self.exit_button.grid(row=0, column=0)

        self.ping_label = Label(
            self.root,
            text="New World Fishing Bot ",
            font=('Consolas', '14'),
            fg='green3',
            bg='grey19'
        )
        self.ping_label.grid(row=0, column=1)

        self.ping_label = Label(
            self.root,
            textvariable=self.test,
            font=('Consolas', '14'),
            fg='green3',
            bg='grey19'
        )
        self.root.overrideredirect(True)
        self.root.geometry("+5+5")
        self.root.lift()
        self.root.wm_attributes("-topmost", True)

    def update_label(self, test) -> None:
        update_text = test
        self.test.set(update_text)
        self.root.after(100, self.update_label)

    def run(self) -> None:
        self.root.mainloop()


gui = Overlay()
gui.run()
