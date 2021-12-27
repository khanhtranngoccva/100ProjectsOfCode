import eel
from tkinter import Tk
from tkinter import filedialog
import os

root = Tk()
root.withdraw()

supported_filetypes = (
    ("Text files", "*.txt"),
    ("Log files", "*.log"),
    ("All files", "*")
)


@eel.expose
def open_file():
    filename = filedialog.askopenfilename(title="Select a text file", initialdir=".", filetypes=supported_filetypes,
                                          parent=root)
    if not filename:
        return
    with open(filename, "r", encoding="utf-8") as file:
        a = file.read()
    return a, filename, os.path.basename(filename)


@eel.expose
def save_file(data):
    filename = filedialog.asksaveasfilename(title="Save text as", initialdir=".", filetypes=supported_filetypes)
    if not filename:
        return
    with open(filename, "w", encoding="utf-8") as file:
        file.write(data)
    return data, filename, os.path.basename(filename)


@eel.expose
def auto_save(data, fn):
    with open(fn, "w", encoding="utf-8") as file:
        file.write(data)


if __name__ == '__main__':
    eel.init("web")
    eel.start("/index.html")
