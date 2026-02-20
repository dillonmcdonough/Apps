import tkinter as tk
from tkinter import font as tkfont


class RoundedPanel(tk.Canvas):
    def __init__(
        self,
        parent,
        bg,
        border_color=None,
        radius=14,
        pad_x=12,
        pad_y=10,
        stretch_content=False,
    ):
        super().__init__(
            parent,
            bg=parent.cget("bg"),
            highlightthickness=0,
            bd=0,
        )
        self._fill = bg
        self._border = border_color if border_color else bg
        self._radius = max(4, radius)
        self._pad_x = max(0, pad_x)
        self._pad_y = max(0, pad_y)
        self._stretch_content = stretch_content

        self.content = tk.Frame(self, bg=bg, bd=0, highlightthickness=0)
        self._window_id = self.create_window(
            self._pad_x,
            self._pad_y,
            anchor="nw",
            window=self.content,
        )

        self.bind("<Configure>", self._on_configure)
        self.content.bind("<Configure>", self._on_content_configure)
        self._draw(10, 10)

    def _rounded_points(self, x1, y1, x2, y2, radius):
        return [
            x1 + radius,
            y1,
            x2 - radius,
            y1,
            x2,
            y1,
            x2,
            y1 + radius,
            x2,
            y2 - radius,
            x2,
            y2,
            x2 - radius,
            y2,
            x1 + radius,
            y2,
            x1,
            y2,
            x1,
            y2 - radius,
            x1,
            y1 + radius,
            x1,
            y1,
        ]

    def _draw(self, width, height):
        self.delete("bg_shape")
        r = max(4, min(self._radius, width // 2, height // 2))
        points = self._rounded_points(1, 1, width - 1, height - 1, r)
        self.create_polygon(
            points,
            smooth=True,
            fill=self._fill,
            outline=self._border,
            width=1,
            tags="bg_shape",
        )
        self.tag_lower("bg_shape")

    def _on_configure(self, event):
        width = max(8, event.width)
        height = max(8, event.height)
        self._draw(width, height)

        self.coords(self._window_id, self._pad_x, self._pad_y)
        inner_w = max(1, width - (self._pad_x * 2))
        if self._stretch_content:
            inner_h = max(1, height - (self._pad_y * 2))
            self.itemconfigure(self._window_id, width=inner_w, height=inner_h)
        else:
            self.itemconfigure(self._window_id, width=inner_w)

    def _on_content_configure(self, _event):
        if self._stretch_content:
            return

        desired_h = self.content.winfo_reqheight() + (self._pad_y * 2)
        desired_w = self.content.winfo_reqwidth() + (self._pad_x * 2)

        current_w = max(1, self.winfo_width())
        target_w = max(current_w, desired_w)
        self.configure(width=target_w, height=desired_h)


class RoundedButton(tk.Canvas):
    def __init__(
        self,
        parent,
        text,
        command,
        bg,
        fg,
        hover_bg=None,
        active_bg=None,
        radius=12,
        pad_x=16,
        pad_y=8,
        font=("Segoe UI", 10, "bold"),
        text_anchor="center",
        width=None,
        cursor="hand2",
    ):
        self._font = tkfont.Font(font=font)
        text_width = self._font.measure(text)
        text_height = self._font.metrics("linespace")

        self._height = (pad_y * 2) + text_height
        self._width = width if width is not None else (pad_x * 2) + text_width

        super().__init__(
            parent,
            width=self._width,
            height=self._height,
            bg=parent.cget("bg"),
            highlightthickness=0,
            bd=0,
            cursor=cursor,
        )

        self._command = command
        self._radius = max(4, min(radius, self._height // 2, self._width // 2))
        self._normal_bg = bg
        self._hover_bg = hover_bg if hover_bg else bg
        self._active_bg = active_bg if active_bg else self._hover_bg
        self._fg = fg
        self._text = text
        self._text_anchor = text_anchor
        self._pressed_inside = False
        self._disabled = False
        self._current_bg = bg

        self._shape_id = None
        self._text_id = None

        self._draw(self._normal_bg)

        self.bind("<Enter>", self._on_enter)
        self.bind("<Leave>", self._on_leave)
        self.bind("<ButtonPress-1>", self._on_press)
        self.bind("<ButtonRelease-1>", self._on_release)
        self.bind("<Configure>", self._on_configure)

    def _rounded_points(self, x1, y1, x2, y2, radius):
        return [
            x1 + radius,
            y1,
            x2 - radius,
            y1,
            x2,
            y1,
            x2,
            y1 + radius,
            x2,
            y2 - radius,
            x2,
            y2,
            x2 - radius,
            y2,
            x1 + radius,
            y2,
            x1,
            y2,
            x1,
            y2 - radius,
            x1,
            y1 + radius,
            x1,
            y1,
        ]

    def _draw(self, fill_color):
        self._current_bg = fill_color
        self.delete("all")

        points = self._rounded_points(1, 1, self._width - 1, self._height - 1, self._radius)
        self._shape_id = self.create_polygon(points, smooth=True, fill=fill_color, outline=fill_color)

        if self._text_anchor == "w":
            text_x = 14
            anchor = "w"
        else:
            text_x = self._width // 2
            anchor = "center"

        self._text_id = self.create_text(
            text_x,
            self._height // 2,
            text=self._text,
            fill=self._fg,
            font=self._font,
            anchor=anchor,
        )

    def _on_configure(self, event):
        if event.width <= 2 or event.height <= 2:
            return
        self._width = event.width
        self._height = event.height
        self._radius = max(4, min(self._radius, self._height // 2, self._width // 2))
        self._draw(self._current_bg)

    def set_colors(self, bg=None, fg=None, hover_bg=None, active_bg=None):
        if bg is not None:
            self._normal_bg = bg
        if fg is not None:
            self._fg = fg
        if hover_bg is not None:
            self._hover_bg = hover_bg
        if active_bg is not None:
            self._active_bg = active_bg
        self._draw(self._normal_bg)

    def set_text(self, text):
        self._text = text
        self.itemconfigure(self._text_id, text=text)

    def set_font(self, font):
        self._font = tkfont.Font(font=font)
        self.itemconfigure(self._text_id, font=self._font)

    def set_disabled(self, disabled=True):
        self._disabled = disabled
        self.configure(cursor="arrow" if disabled else "hand2")
        if disabled:
            self._draw(self._normal_bg)

    def _on_enter(self, _event):
        if self._disabled:
            return
        self._draw(self._hover_bg)

    def _on_leave(self, _event):
        if self._disabled:
            return
        self._pressed_inside = False
        self._draw(self._normal_bg)

    def _on_press(self, _event):
        if self._disabled:
            return
        self._pressed_inside = True
        self._draw(self._active_bg)

    def _on_release(self, event):
        if self._disabled:
            return
        inside = 0 <= event.x <= self._width and 0 <= event.y <= self._height
        self._draw(self._hover_bg if inside else self._normal_bg)
        if inside and self._pressed_inside and self._command:
            self._command()
        self._pressed_inside = False
