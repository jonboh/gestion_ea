import tkinter as tk
import tkinter.font as tkFont
import tkinter.ttk as ttk
import copy

class TreeObject:
    def __init__(self, parent_frame, object_list, object_type, ):
        self.main_frame = parent_frame
        self.objects = copy.deepcopy(object_list)
        self.master_type = object_type
        self.header = self.master_type.str_header

        self.tree_ids = list()
        self.tree = ttk.Treeview(self.main_frame)
        vsb = ttk.Scrollbar(self.main_frame, orient="vertical", command=self.tree.yview)
        vsb.pack(side=tk.RIGHT, fill=tk.Y)
        hsb = ttk.Scrollbar(self.main_frame, orient="horizontal", command=self.tree.xview)
        hsb.pack(side=tk.BOTTOM, fill=tk.X)
        self.tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        self.tree.pack(fill='both', expand=True)
        self.tree.config(columns=self.header, show='headings')

        def build_tree(header_):
            for col in header_:
                self.tree.heading(col, text=col.title())
                self.tree.column(col, width=tkFont.Font().measure(col.title()))
        build_tree(self.header)

        self.add_objects(self.objects)

    def bind(self, event_name, function):
        self.tree.bind(event_name, function)

    def add_objects(self, objects):
        for object_ in objects:
            self.tree_ids.append(
                self.tree.insert('', 'end', values=object_.tree_entries()))
            for ix, val in enumerate(object_):
                col_w = tkFont.Font().measure(val)
                if self.tree.column(self.header[ix], width=None) < col_w:
                    self.tree.column(self.header[ix], width=col_w)

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

    def theres_selection(self):
        if len(self.tree.selection()) is 0:
            return False
        else:
            return True

    def selection_index(self):
        return self.tree.index(self.tree.selection()[0])
