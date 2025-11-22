import tkinter as tk
from ui.main_window import AutoDrawApp


def main():
    root = tk.Tk()
    AutoDrawApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
