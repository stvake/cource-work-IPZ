from tkinter import *
import tkinter.ttk as ttk


class EditableTable(ttk.Treeview):
    def __init__(self, parent, **kw):
        super().__init__(parent, **kw)

        self.bind("<Double-1>", self._on_double_click)
        self.bind("<Delete>", self._on_delete_pressed)

    def _on_double_click(self, event):
        region_clicked = self.identify_region(event.x, event.y)

        if region_clicked == 'heading':
            return

        elif region_clicked == 'nothing':
            new_item = self.insert('', 'end', values=['' for _ in range(len(self['columns']))])
            self.selection_set(new_item)
            self.focus(new_item)

        column = self.identify_column(event.x)
        column_index = int(column[1:]) - 1

        selected_iid = self.focus()
        selected_values = self.item(selected_iid).get('values')
        selected_item = selected_values[column_index]
        item_box = self.bbox(selected_iid, column)

        entry_edit = ttk.Entry(self)
        entry_edit.editing_column_index = column_index
        entry_edit.editing_item_iid = selected_iid
        entry_edit.place(x=item_box[0], y=item_box[1], w=item_box[2], h=item_box[3])
        entry_edit.insert(END, selected_item)
        entry_edit.select_range(0, END)
        entry_edit.focus()

        entry_edit.bind("<FocusOut>", self._on_focus_out)
        entry_edit.bind("<Escape>", self._on_focus_out)
        entry_edit.bind("<Return>", self._on_enter_pressed)

    @staticmethod
    def _on_focus_out(event):
        event.widget.destroy()

    def _on_enter_pressed(self, event):
        new_value = event.widget.get()

        selected_iid = event.widget.editing_item_iid
        column_index = event.widget.editing_column_index

        current_values = list(self.item(selected_iid, 'values'))
        current_values[column_index] = new_value
        self.item(selected_iid, values=current_values)

        event.widget.destroy()

    def _on_delete_pressed(self, event):
        selected_iid = self.focus()
        self.delete(selected_iid)
