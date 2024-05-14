from MVC.Views.editable_table import EditableTable
import tkinter.ttk as ttk


class ComboboxTable(EditableTable):
    def __init__(self, parent, non_editable_columns=None, allow_delete=True, **kw):
        super().__init__(parent, non_editable_columns, allow_delete, **kw)
        self.combobox_values = {}
        self.is_editing = False

    def _on_double_click(self, event):
        if self.is_editing:
            return

        self.is_editing = True

        region_clicked = self.identify_region(event.x, event.y)

        if region_clicked == 'heading':
            return

        elif region_clicked == 'nothing':
            new_item = self.insert('', 'end', values=['' for _ in range(len(self['columns']))])
            self.selection_set(new_item)
            self.focus(new_item)

        column = self.identify_column(event.x)
        column_index = int(column[1:]) - 1

        if column_index in self.non_editable_columns:
            self.is_editing = False
            return

        selected_iid = self.focus()
        selected_values = self.item(selected_iid).get('values')
        selected_item = selected_values[column_index]
        item_box = self.bbox(selected_iid, column)

        self.combobox_edit = ttk.Combobox(self, values=self.combobox_values.get(column_index, []))
        self.combobox_edit.editing_column_index = column_index
        self.combobox_edit.editing_item_iid = selected_iid
        self.combobox_edit.place(x=item_box[0], y=item_box[1], w=item_box[2], h=item_box[3])
        self.combobox_edit.set(selected_item)
        self.combobox_edit.select_range(0, 'end')
        self.combobox_edit.config(state='readonly')
        self.combobox_edit.focus()

        self.combobox_edit.bind("<<ComboboxSelected>>", self._on_combobox_selected)
        self.combobox_edit.bind("<Escape>", self._on_focus_out)
        self.bind("<Escape>", self._on_focus_out)
        self.combobox_edit.get()

    def set_combobox_values(self, column_name, values):
        column_index = self['columns'].index(column_name)
        self.combobox_values[column_index] = values

    def _on_focus_out(self, event):
        self.combobox_edit.destroy()
        self.is_editing = False

    def _on_combobox_selected(self, event):
        self.on_value_selected(event.widget.get())
        self._on_enter_pressed(event)
        self.is_editing = False

    def on_value_selected(self, value):
        pass
