from tkinter import *
import tkinter.ttk as ttk


class VerticalScrolledFrame(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        v_scrollbar = ttk.Scrollbar(self, orient=VERTICAL)
        v_scrollbar.pack(fill=Y, side=RIGHT, expand=FALSE)
        self.canvas = Canvas(self, bd=0, highlightthickness=0, width=500, height=750, yscrollcommand=v_scrollbar.set)
        self.canvas.pack(side=LEFT, fill=BOTH, expand=TRUE)
        v_scrollbar.config(command=self.canvas.yview)

        self.canvas.xview_moveto(0)
        self.canvas.yview_moveto(0)

        self.interior = ttk.Frame(self.canvas)
        self.interior.bind('<Configure>', self._configure_interior)
        self.canvas.bind('<Configure>', self._configure_canvas)
        self.interior_id = self.canvas.create_window(0, 0, window=self.interior, anchor=NW)

    def _configure_interior(self, event):
        size = (self.interior.winfo_reqwidth(), self.interior.winfo_reqheight())
        self.canvas.config(scrollregion=(0, 0, size[0], size[1]))
        if self.interior.winfo_reqwidth() != self.canvas.winfo_width():
            self.canvas.config(width=self.interior.winfo_reqwidth())

    def _configure_canvas(self, event):
        for x in self.get_all_widgets(self):
            x.bind('<MouseWheel>', self._on_mousewheel)

        if self.interior.winfo_reqwidth() != self.canvas.winfo_width():
            self.canvas.itemconfigure(self.interior_id, width=self.canvas.winfo_width())

    def get_all_widgets(self, parent):
        all_widgets = [parent]
        for child in parent.winfo_children():
            all_widgets.extend(self.get_all_widgets(child))
        return all_widgets

    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
