import tkinter as tk
import tkinter.font as tkFont
import tkinter.ttk as ttk
import copy


class TreeObject:
    def __init__(self, parent_frame, object_list, object_type, header_map=None):
        self.main_frame = parent_frame
        self.objects = list()  # new objects are added on add_objects()
        self.master_type = object_type
        if header_map is None:
            self.header_map = object_type.default_header_map
        else:
            self.header_map = header_map  # this will control which columns are shown
        self.header = list()
        for entry, isinmap in zip(self.master_type.tree_header, self.header_map):
            if isinmap:
                self.header.append(entry)

        self.tree_ids = list()
        self.tree = ttk.Treeview(self.main_frame)
        vsb = ttk.Scrollbar(self.main_frame, orient="vertical", command=self.tree.yview)
        vsb.pack(side=tk.RIGHT, fill=tk.Y)
        hsb = ttk.Scrollbar(self.main_frame, orient="horizontal", command=self.tree.xview)
        hsb.pack(side=tk.BOTTOM, fill=tk.X)
        self.tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        self.tree.pack(fill='both', expand=True)
        self.tree.config(columns=self.header, show='headings')

        for col in self.header:
            self.tree.heading(col, text=col.title())
            self.tree.column(col, width=tkFont.Font().measure(col.title()))

        self.add_objects(object_list)

    def bind(self, event_name, function):
        self.tree.bind(event_name, function)

    def add_objects(self, new_objects):
        for object_ in new_objects:
            self.tree_ids.append(
                self.tree.insert('', 'end', values=object_.tree_entries(self.header_map)))
            self.objects.append(object_)
            for ix, val in enumerate(object_.tree_entries(self.header_map)):
                col_w = tkFont.Font().measure(val)
                if self.tree.column(self.header[ix], width=None) < col_w:
                    self.tree.column(self.header[ix], width=col_w)

    def update_entries(self, old_objects, new_objects):
        for old, new in zip(old_objects, new_objects):
            index = self.objects.index(old)
            self.objects.pop(old)
            self.tree.delete(self.tree_ids.pop(index))
            self.tree_ids.append(
                self.tree.insert('', index, values=new.tree_entries()))

    def delete_objects(self, objects):
        for object_ in objects:
            obj_index = self.objects.index(object_)
            self.objects.pop(obj_index)
            self.tree.delete(self.tree_ids.pop(obj_index))

    def clear_tree(self):
        for object_ in self.tree_ids:
            self.tree.delete(object_)
        self.objects = list()
        self.tree_ids = list()

    def _theres_selection(self):
        if len(self.tree.selection()) is 0:
            return False
        else:
            return True

    def _selection_index(self):
        return self.tree.index(self.tree.selection()[0])

    def selection(self):
        if self._theres_selection():
            return self.objects[self._selection_index()]
        else:
            return -1
