import tkinter as tk
import tkinter.font as tkFont
import tkinter.ttk as ttk


class TreeObject:
    def __init__(self, parent_frame, object_list, object_type, ):
        self.main_frame = parent_frame
        self.objects = object_list
        self.master_type = object_type

        self.clients_tree_ids = list()
        self.clients_tree = ttk.Treeview(self.main_frame)
        cl_vsb = ttk.Scrollbar(self.main_frame, orient="vertical", command=self.clients_tree.yview)
        cl_vsb.pack(side=tk.RIGHT, fill=tk.Y)
        cl_hsb = ttk.Scrollbar(self.main_frame, orient="horizontal", command=self.clients_tree.xview)
        cl_hsb.pack(side=tk.BOTTOM, fill=tk.X)
        self.clients_tree.configure(yscrollcommand=cl_vsb.set, xscrollcommand=cl_hsb.set)
        self.clients_tree.pack(fill='both', expand=True)

        self.redraw_tree(self.objects)

    def bind(self, event_name, function):
        self.clients_tree.bind(event_name, function)

    def add_objects(self, objects):
        pass

    def delete_objects(self, objects):
        pass

    def clear_tree(self):
        pass

    def redraw_tree(self, objects):
        pass
