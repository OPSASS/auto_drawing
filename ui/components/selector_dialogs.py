import tkinter as tk
from utils.helpers import calculate_aspect_ratio


class ScreenSelector(tk.Toplevel):

    def __init__(self, callback, title="Chọn vùng"):
        super().__init__()
        self.callback = callback
        self.title_text = title

        self.attributes("-fullscreen", True)
        self.attributes("-alpha", 0.3)
        self.config(bg="black")
        self.lift()

        self.canvas = tk.Canvas(
            self,
            highlightthickness=0,
            cursor="cross",
            bg="black"
        )
        self.canvas.pack(fill="both", expand=True)

        self.title_label = self.canvas.create_text(
            self.winfo_screenwidth() // 2, 30,
            text=title,
            fill="yellow",
            font=("Arial", 20, "bold")
        )

        self.start_x = None
        self.start_y = None
        self.rect = None
        self.text = None

        self.canvas.bind("<ButtonPress-1>", self.on_press)
        self.canvas.bind("<B1-Motion>", self.on_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_release)

    def on_press(self, event):
        self.start_x = event.x
        self.start_y = event.y

        self.rect = self.canvas.create_rectangle(
            self.start_x, self.start_y, event.x, event.y,
            outline="red", width=2
        )

        self.text = self.canvas.create_text(
            self.start_x + 10, self.start_y + 10,
            anchor="nw",
            fill="yellow",
            font=("Arial", 14, "bold"),
            text=f"{self.start_x}, {self.start_y}"
        )

    def on_drag(self, event):
        self.canvas.coords(self.rect, self.start_x,
                           self.start_y, event.x, event.y)

        w = abs(event.x - self.start_x)
        h = abs(event.y - self.start_y)

        ratio_text = calculate_aspect_ratio(w, h)

        self.canvas.coords(self.text, event.x + 10, event.y + 10)
        self.canvas.itemconfig(
            self.text,
            text=f"w: {w}px, h: {h}px, ratio: {ratio_text}"
        )

    def on_release(self, event):
        x1, y1 = self.start_x, self.start_y
        x2, y2 = event.x, event.y

        if x1 > x2:
            x1, x2 = x2, x1
        if y1 > y2:
            y1, y2 = y2, y1

        self.callback(x1, y1, x2, y2)
        self.destroy()


class PointSelector(tk.Toplevel):
    def __init__(self, callback, title="Chọn điểm"):
        super().__init__()
        self.callback = callback

        self.attributes("-fullscreen", True)
        self.attributes("-alpha", 0.3)
        self.config(bg="black")
        self.lift()

        self.canvas = tk.Canvas(
            self,
            highlightthickness=0,
            cursor="crosshair",
            bg="black"
        )
        self.canvas.pack(fill="both", expand=True)

        self.canvas.create_text(
            self.winfo_screenwidth() // 2, 30,
            text=title,
            fill="yellow",
            font=("Arial", 20, "bold")
        )

        self.canvas.bind("<Button-1>", self.on_click)

    def on_click(self, event):
        self.callback(event.x, event.y)
        self.destroy()
