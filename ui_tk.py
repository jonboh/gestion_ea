import tkinter as tk
import tkinter.font as tkFont
import tkinter.ttk as ttk
import threading as thr

import data_io as io
import client as cl
import group as gr
import item as it


class GestionEspacioAbierto:
    def __init__(self, root):
        self.root = root
        self.root.title('Gestion Espacio Abierto v0.7')
        self.original_geometry = [1100, 600]
        str_original_geometry = map(str, self.original_geometry)
        self.root.geometry('x'.join(str_original_geometry))
        self.root.protocol("WM_DELETE_WINDOW", self.close_program)
        self.root.rowconfigure(0, weight=1)
        self.root.columnconfigure(0, weight=1)
        self.listbox_proportion = [0.125, 0.05]
        self.popup_root = TkSecureNone()

        # LOADING WINDOW DECLARATION
        self.loading_frame = tk.Frame(self.root, background='green')
        self.loading_frame.grid_rowconfigure(0, weight=1)
        self.loading_frame.grid_columnconfigure(0, weight=1)
        self.loading_frame.grid(row=0, column=0, sticky=tk.N + tk.W + tk.E + tk.S)

        loading_label = tk.Label(self.loading_frame, text='Cargando, por favor espera...', background='white')
        loading_label.grid(row=0, column=0, sticky=tk.N + tk.W + tk.E + tk.S)
        self.loading_frame.tkraise()

        # WELCOME WINDOW DECLARATION
        self.welcome_frame = tk.Frame(self.root, background='yellow')
        self.welcome_frame.grid_rowconfigure(0, weight=1)
        self.welcome_frame.grid_columnconfigure(0, weight=1)
        self.welcome_frame.grid(row=0, column=0, sticky=tk.N + tk.W + tk.E + tk.S)
        welcome_label = tk.Label(self.welcome_frame, background='white', text='Bienvenido, hora de trabajar',
                                 font=("Helvetica", 24))
        welcome_label.grid(row=0, column=0, sticky=tk.N + tk.W, padx=(100, 0), pady=(80, 0))
        welcome_nav_frame = tk.Frame(self.welcome_frame, background='red')
        welcome_nav_frame.grid(row=1, column=0, sticky=tk.S + tk.E)
        self.navigation_interface(welcome_nav_frame)

        # LOAD CLIENTS AND GROUPS
        self.loading_frame.tkraise()
        self.clients = io.load_clients(file_clients, cl.Client)
        self.alumns = io.load_clients(file_alumns, cl.Alumn)
        self.groups = io.load_groups(file_groups)

        # CLIENTS LIST WINDOW
        self.init_client_window()

        # GROUPS WINDOW
        self.init_group_window()

        # INVENTORY WINDOW
        self.init_inventory_window()

        # UPDATE CLIENTS AND GROUPS LISTBOXES
        self.clients_tree_update()
        self.groups_tree_update()

        self.welcome_frame.tkraise()

    def init_client_window(self):
        self.clients_frame = tk.Frame(self.root, background='blue')
        for index in range(1, 2):
            self.clients_frame.grid_rowconfigure(index, weight=1)
        for index in range(1, 2):
            self.clients_frame.grid_columnconfigure(index, weight=1)
        self.clients_frame.grid(row=0, column=0, sticky=tk.N + tk.W + tk.E + tk.S)

        clients_table_label = tk.Label(self.clients_frame, text='Clientes: ', font=("Helvetica", 14))
        clients_table_label.grid(row=0, column=0, sticky=tk.N + tk.W)

        # Clients Checkboxes
        clients_buttons_frame = tk.Frame(self.clients_frame)
        clients_buttons_frame.grid(row=0, column=1, sticky=tk.N + tk.W)
        self.cl_chbox_var = tk.IntVar()
        self.cl_chbox_var.set(1)
        self.clients_checkbox = tk.Checkbutton(clients_buttons_frame, text='Clientes', font=("Helvetica", 10),
                                               variable=self.cl_chbox_var,
                                               command=lambda: self.clients_checkbox_update('Clients'))
        self.clients_checkbox.grid(row=0, column=0, sticky=tk.N + tk.E)
        self.pa_chbox_var = tk.IntVar()
        self.pa_chbox_var.set(0)
        self.patients_checkbox = tk.Checkbutton(clients_buttons_frame, text='Pacientes', font=("Helvetica", 10),
                                                variable=self.pa_chbox_var,
                                                command=lambda: self.clients_checkbox_update('Patients'))
        self.patients_checkbox.grid(row=0, column=1, sticky=tk.N + tk.E)
        self.al_chbox_var = tk.IntVar()
        self.al_chbox_var.set(0)
        self.alumns_checkbox = tk.Checkbutton(clients_buttons_frame, text='Alumnos', font=("Helvetica", 10),
                                              variable=self.al_chbox_var,
                                              command=lambda: self.clients_checkbox_update('Alumns'))
        self.alumns_checkbox.grid(row=0, column=2, sticky=tk.N + tk.E)
        self.al_chbox_bank_var = tk.IntVar()
        self.al_chbox_bank_var.set(0)
        self.alumns_checkbox_bank = tk.Checkbutton(clients_buttons_frame, text='Solo Domiciliados',
                                                   font=("Helvetica", 10),
                                                   variable=self.al_chbox_bank_var,
                                                   command=lambda: self.clients_checkbox_update('bank'))
        self.alumns_checkbox_bank.grid(row=0, column=3, sticky=tk.N + tk.E)
        # Search Box
        self.cl_search_entry = tk.Entry(clients_buttons_frame)
        self.cl_search_entry.grid(row=0, column=4, padx=(25, 0), sticky=tk.E)
        self.cl_search_button = tk.Button(clients_buttons_frame, text='Buscar', command=self.search_clients)
        self.cl_search_button.grid(row=0, column=5, sticky=tk.N + tk.E)
        self.cl_search_clear_button = tk.Button(clients_buttons_frame, text='Resetear',
                                                command=self.clear_search_clients)
        self.cl_search_clear_button.grid(row=0, column=6, sticky=tk.N + tk.E)
        self.search_isactive = False
        # Clients Tree
        clients_table_frame = tk.Frame(self.clients_frame, background='black')
        clients_table_frame.grid(row=1, column=0, columnspan=2, sticky='nwes')
        self.clients_tree_ids = list()
        self.clients_tree = ttk.Treeview(clients_table_frame)
        cl_vsb = ttk.Scrollbar(clients_table_frame, orient="vertical", command=self.clients_tree.yview)
        cl_vsb.pack(side=tk.RIGHT, fill=tk.Y)
        cl_hsb = ttk.Scrollbar(clients_table_frame, orient="horizontal", command=self.clients_tree.xview)
        cl_hsb.pack(side=tk.BOTTOM, fill=tk.X)
        self.clients_tree.configure(yscrollcommand=cl_vsb.set, xscrollcommand=cl_hsb.set)
        self.clients_tree.pack(fill='both', expand=True)
        self.clients_tree.bind('<Double-Button-1>', lambda _: self.view_client())
        clients_list_buttons_frame = tk.Frame(self.clients_frame)
        clients_list_buttons_frame.grid(row=1, column=3, sticky=tk.N + tk.E)
        self.list_buttons(clients_list_buttons_frame, cl.Client)
        clients_list_nav_frame = tk.Frame(self.clients_frame, background='red')
        clients_list_nav_frame.grid(row=2, column=1, columnspan=3, sticky=tk.S + tk.E)
        self.navigation_interface(clients_list_nav_frame)

        # Sorters
        clients_sorters_frame = tk.Frame(self.clients_frame)
        clients_sorters_frame.grid(row=2, column=0, sticky=tk.W + tk.S)
        clients_sort_label = tk.Label(clients_sorters_frame, text='Ordernar por: ')
        clients_sort_label.grid(row=0, column=0, sticky=tk.N + tk.W)
        self.cl_name_sort_var = tk.IntVar()

        self.cl_name_sort_chbox = tk.Checkbutton(clients_sorters_frame, text='Nombre',
                                                 command=lambda: self.sort_clients_event('name'))
        self.cl_name_sort_var.set(1)
        self.cl_name_sort_chbox.select()
        self.cl_name_sort_chbox.grid(row=0, column=1, sticky=tk.N + tk.W)
        self.cl_surname_sort_var = tk.IntVar()
        self.cl_surname_sort_chbox = tk.Checkbutton(clients_sorters_frame, text='Apellidos',
                                                    command=lambda: self.sort_clients_event('surname'))
        self.cl_surname_sort_chbox.grid(row=0, column=2, sticky=tk.N + tk.W)
        self.cl_inverse_sort_var = tk.IntVar()
        self.cl_inverse_sort_chbox = tk.Checkbutton(clients_sorters_frame, text='Invertir orden',
                                                    command=lambda: self.sort_clients_event('inverse'))
        self.cl_inverse_sort_chbox.grid(row=1, column=1, sticky=tk.N + tk.W)

    def init_group_window(self):
        self.groups_frame = tk.Frame(self.root, background='blue')
        for index in range(1, 2):
            self.groups_frame.grid_rowconfigure(index, weight=1)
        for index in range(1, 2):
            self.groups_frame.grid_columnconfigure(index, weight=1)
        self.groups_frame.grid(row=0, column=0, sticky=tk.N + tk.W + tk.E + tk.S)
        groups_table_frame = tk.Frame(self.groups_frame, background='black')
        groups_table_frame.grid(row=1, column=0, columnspan=2, sticky=tk.N + tk.W + tk.E + tk.S)
        groups_table_label = tk.Label(self.groups_frame, text='Grupos: ', font=("Helvetica", 14))
        groups_table_label.grid(row=0, column=0, sticky=tk.N + tk.W)
        groups_list_buttons_frame = tk.Frame(self.groups_frame)
        groups_list_buttons_frame.grid(row=1, column=3, sticky=tk.N + tk.E)
        self.list_buttons(groups_list_buttons_frame, gr.Group)

        self.groups_tree_ids = list()
        self.groups_tree = ttk.Treeview(groups_table_frame)
        gr_vsb = ttk.Scrollbar(groups_table_frame, orient="vertical", command=self.groups_tree.yview)
        gr_vsb.pack(side=tk.RIGHT, fill=tk.Y)
        # gr_hsb = ttk.Scrollbar(groups_table_frame, orient="horizontal", command=self.groups_tree.xview)
        # gr_hsb.pack(side=tk.BOTTOM, fill=tk.X)
        self.groups_tree.configure(yscrollcommand=gr_vsb.set)  # , xscrollcommand=gr_hsb.set)
        self.groups_tree.pack(fill='both', expand=True)
        self.groups_tree.bind('<Double-Button-1>', lambda _: self.view_group())

        groups_list_nav_frame = tk.Frame(self.groups_frame, background='red')
        groups_list_nav_frame.grid(row=2, column=1, columnspan=3, sticky=tk.S + tk.E)
        self.navigation_interface(groups_list_nav_frame)
        # Sorters
        groups_sorters_frame = tk.Frame(self.groups_frame)
        groups_sorters_frame.grid(row=2, sticky=tk.W + tk.S)
        groups_sort_label = tk.Label(groups_sorters_frame, text='Ordernar por: ')
        groups_sort_label.grid(row=0, column=0, sticky=tk.N + tk.W)
        self.gr_activity_sort_var = tk.IntVar()
        self.gr_activity_sort_chbox = tk.Checkbutton(groups_sorters_frame, text='Actividad',
                                                     command=lambda: self.sort_groups_event('activity'))
        self.gr_activity_sort_var.set(1)
        self.gr_activity_sort_chbox.select()
        self.gr_activity_sort_chbox.grid(row=0, column=1, sticky=tk.N + tk.W)
        self.gr_teacher_sort_var = tk.IntVar()
        self.gr_teacher_sort_chbox = tk.Checkbutton(groups_sorters_frame, text='Monitor/a',
                                                    command=lambda: self.sort_groups_event('teacher'))
        self.gr_teacher_sort_chbox.grid(row=0, column=2, sticky=tk.N + tk.W)
        self.gr_inverse_sort_var = tk.IntVar()
        self.gr_inverse_sort_chbox = tk.Checkbutton(groups_sorters_frame, text='Invertir orden',
                                                    command=lambda: self.sort_groups_event('inverse'))
        self.gr_inverse_sort_chbox.grid(row=1, column=1, sticky=tk.N + tk.W)

    def init_inventory_window(self):
        self.items_frame = tk.Frame(self.root, background='blue')
        for index in range(1, 2):
            self.items_frame.grid_rowconfigure(index, weight=1)
        for index in range(1, 2):
            self.items_frame.grid_columnconfigure(index, weight=1)
        self.items_frame.grid(row=0, column=0, sticky=tk.N + tk.W + tk.E + tk.S)
        items_table_frame = tk.Frame(self.items_frame, background='black')
        items_table_frame.grid(row=1, column=0, columnspan=2, sticky=tk.N + tk.W + tk.E + tk.S)
        items_table_label = tk.Label(self.items_frame, text='Inventario: ', font=("Helvetica", 14))
        items_table_label.grid(row=0, column=0, sticky=tk.N + tk.W)
        items_list_buttons_frame = tk.Frame(self.items_frame)
        items_list_buttons_frame.grid(row=1, column=3, sticky=tk.N + tk.E)
        self.list_buttons(items_list_buttons_frame, it.Item)

        self.items_tree_ids = list()
        self.items_tree = ttk.Treeview(items_table_frame)
        it_vsb = ttk.Scrollbar(items_table_frame, orient="vertical", command=self.items_tree.yview)
        it_vsb.pack(side=tk.RIGHT, fill=tk.Y)
        it_hsb = ttk.Scrollbar(items_table_frame, orient="horizontal", command=self.items_tree.xview)
        it_hsb.pack(side=tk.BOTTOM, fill=tk.X)
        self.items_tree.configure(yscrollcommand=it_vsb.set, xscrollcommand=it_hsb.set)
        self.items_tree.pack(fill='both', expand=True)
        self.items_tree.bind('<Double-Button-1>', lambda _: self.view_group())

        items_list_nav_frame = tk.Frame(self.items_frame, background='red')
        items_list_nav_frame.grid(row=2, column=1, columnspan=3, sticky=tk.S + tk.E)
        self.navigation_interface(items_list_nav_frame)
        # Sorters
        items_sorters_frame = tk.Frame(self.items_frame)
        items_sorters_frame.grid(row=2, sticky=tk.W + tk.S)
        items_sort_label = tk.Label(items_sorters_frame, text='Ordernar por: ')
        items_sort_label.grid(row=0, column=0, sticky=tk.N + tk.W)
        self.it_activity_sort_var = tk.IntVar()
        self.it_activity_sort_chbox = tk.Checkbutton(items_sorters_frame, text='Nombre',
                                                     command=lambda: self.sort_items_event('name'))
        self.it_activity_sort_var.set(1)
        self.it_activity_sort_chbox.select()
        self.it_activity_sort_chbox.grid(row=0, column=1, sticky=tk.N + tk.W)
        self.it_teacher_sort_var = tk.IntVar()
        self.it_teacher_sort_chbox = tk.Checkbutton(items_sorters_frame, text='Proveedor',
                                                    command=lambda: self.sort_items_event('provider'))
        self.it_teacher_sort_chbox.grid(row=0, column=2, sticky=tk.N + tk.W)
        self.it_inverse_sort_var = tk.IntVar()
        self.it_inverse_sort_chbox = tk.Checkbutton(items_sorters_frame, text='Invertir orden',
                                                    command=lambda: self.sort_items_event('inverse'))
        self.it_inverse_sort_chbox.grid(row=1, column=1, sticky=tk.N + tk.W)

    def list_buttons(self, parent_frame, type_window):
        if type_window is cl.Client:
            new_button = tk.Button(parent_frame, text='Nuevo', command=self.new_client)
            new_button.grid(row=0, column=0, sticky=tk.N + tk.E, padx=(10, 10), pady=(0, 10))
            view_button = tk.Button(parent_frame, text='Ver', command=self.view_client)
            view_button.grid(row=1, column=0, sticky=tk.N + tk.E, padx=(10, 10), pady=(0, 10))
            modify_button = tk.Button(parent_frame, text='Modificar', command=self.modify_client)
            modify_button.grid(row=2, column=0, sticky=tk.N + tk.E, padx=(10, 10), pady=(0, 10))
            delete_button = tk.Button(parent_frame, text='Eliminar', command=self.delete_client)
            delete_button.grid(row=3, column=0, sticky=tk.N + tk.E, padx=(10, 10), pady=(0, 10))
            export_button = tk.Button(parent_frame, text='Exportar', command=self.export_selection)
            export_button.grid(row=4, column=0, sticky=tk.N + tk.E, padx=(10, 10), pady=(0, 10))
        elif type_window is gr.Group:
            new_button = tk.Button(parent_frame, text='Nuevo', command=self.new_group)
            new_button.grid(row=0, column=0, sticky=tk.N + tk.E, padx=(10, 10), pady=(0, 10))
            view_button = tk.Button(parent_frame, text='Ver', command=self.view_group)
            view_button.grid(row=1, column=0, sticky=tk.N + tk.E, padx=(10, 10), pady=(0, 10))
            modify_button = tk.Button(parent_frame, text='Modificar', command=self.modify_group)
            modify_button.grid(row=2, column=0, sticky=tk.N + tk.E, padx=(10, 10), pady=(0, 10))
            delete_button = tk.Button(parent_frame, text='Eliminar', command=self.delete_group)
            delete_button.grid(row=3, column=0, sticky=tk.N + tk.E, padx=(10, 10), pady=(0, 10))
            export_button = tk.Button(parent_frame, text='Exportar', command=self.export_selection)
            export_button.grid(row=4, column=0, sticky=tk.N + tk.E, padx=(10, 10), pady=(0, 10))
        elif type_window is it.Item:
            new_button = tk.Button(parent_frame, text='Nuevo', command=self.new_item)
            new_button.grid(row=0, column=0, sticky=tk.N + tk.E, padx=(10, 10), pady=(0, 10))
            view_button = tk.Button(parent_frame, text='Ver', command=self.view_item)
            view_button.grid(row=1, column=0, sticky=tk.N + tk.E, padx=(10, 10), pady=(0, 10))
            modify_button = tk.Button(parent_frame, text='Modificar', command=self.modify_item)
            modify_button.grid(row=2, column=0, sticky=tk.N + tk.E, padx=(10, 10), pady=(0, 10))
            delete_button = tk.Button(parent_frame, text='Eliminar', command=self.delete_item)
            delete_button.grid(row=3, column=0, sticky=tk.N + tk.E, padx=(10, 10), pady=(0, 10))
            export_button = tk.Button(parent_frame, text='Exportar', command=self.export_selection)
            export_button.grid(row=4, column=0, sticky=tk.N + tk.E, padx=(10, 10), pady=(0, 10))
        else:
            new_button = tk.Button(parent_frame, text='Nuevo')
            new_button.grid(row=0, column=0, sticky=tk.N + tk.E, padx=(10, 10), pady=(0, 10))
            view_button = tk.Button(parent_frame, text='Ver')
            view_button.grid(row=1, column=0, sticky=tk.N + tk.E, padx=(10, 10), pady=(0, 10))
            modify_button = tk.Button(parent_frame, text='Modificar')
            modify_button.grid(row=2, column=0, sticky=tk.N + tk.E, padx=(10, 10), pady=(0, 10))
            delete_button = tk.Button(parent_frame, text='Eliminar')
            delete_button.grid(row=3, column=0, sticky=tk.N + tk.E, padx=(10, 10), pady=(0, 10))
            export_button = tk.Button(parent_frame, text='Exportar')
            export_button.grid(row=4, column=0, sticky=tk.N + tk.E, padx=(10, 10), pady=(0, 10))
        new_button.config(width=20)
        view_button.config(width=20)
        modify_button.config(width=20)
        delete_button.config(width=20)
        export_button.config(width=20)
        export_button.config(state=tk.DISABLED)

    def navigation_interface(self, parent_frame):
        save_button = tk.Button(parent_frame, command=self.save_all_info, text='Guardar', width=10)
        save_button.grid(row=0, column=0, sticky=tk.N + tk.W, padx=(0, 25), pady=(25, 25))
        welcome_button = tk.Button(parent_frame, command=self.welcome_window, text='Bienvenida',
                                   width=10)
        welcome_button.grid(row=0, column=1, sticky=tk.N + tk.W, padx=(0, 25), pady=(25, 25))
        clients_button = tk.Button(parent_frame, command=self.clients_list_window, text='Clientes',
                                   width=10)
        clients_button.grid(row=0, column=2, sticky=tk.N + tk.W, padx=(0, 25), pady=(25, 25))
        groups_button = tk.Button(parent_frame, command=self.groups_list_window, text='Grupos',
                                  width=10)
        groups_button.grid(row=0, column=3, sticky=tk.N + tk.W, padx=(0, 25), pady=(25, 25))
        items_button = tk.Button(parent_frame, command=self.items_list_window, text='Inventario',
                                 width=10)
        items_button.grid(row=0, column=4, sticky=tk.N + tk.W, padx=(0, 25), pady=(25, 25))

    def loading_window(self):
        self.loading_frame.tkraise()

    def welcome_window(self):
        self.welcome_frame.tkraise()

    # CLIENTS FUNCTIONALITY
    def clients_list_window(self):
        self.clients_frame.tkraise()

    def clients_checkbox_update(self, invoker):
        """invoker: 'Clients' or 'Alumns'"""
        if invoker is 'Clients':
            self.cl_chbox_var.set(1)
            self.pa_chbox_var.set(0)
            self.al_chbox_var.set(0)
            self.al_chbox_bank_var.set(0)
            self.clear_search_clients()
        if invoker is 'Patients':
            self.cl_chbox_var.set(0)
            self.pa_chbox_var.set(1)
            self.al_chbox_var.set(0)
            self.al_chbox_bank_var.set(0)
            self.clear_search_clients()
        if invoker is 'Alumns':
            self.cl_chbox_var.set(0)
            self.pa_chbox_var.set(0)
            self.al_chbox_var.set(1)
            self.clear_search_clients()
        if invoker is 'bank':
            self.cl_chbox_var.set(0)
            self.pa_chbox_var.set(0)
            self.al_chbox_var.set(1)
            self.clear_search_clients()
        self.clients_tree_update()

    def clients_tree_update(self):

        def create_table():
            entries = list()
            if self.search_isactive:
                self.clients_tree.config(columns=cl.Alumn.str_header)
                for client in self.searched_clients:
                    self.clients_tree_obj.append(client)
                    entry = client.entries()
                    entries.append(entry)
            else:
                # Clients
                if self.pa_chbox_var.get():
                    self.clients_tree.config(columns=cl.Client.str_header)
                    for client in self.clients:
                        self.clients_tree_obj.append(client)
                        entry = client.entries()
                        entries.append(entry)

                if self.cl_chbox_var.get():
                    self.clients_tree.config(columns=cl.Alumn.str_header)
                    for client in self.clients + self.alumns:
                        self.clients_tree_obj.append(client)
                        entry = client.entries()
                        entries.append(entry)

                # Alumns
                if self.al_chbox_var.get() is 1:
                    for client in self.alumns:
                        self.clients_tree.config(columns=cl.Alumn.str_header)
                        # Alumns + Only Bank Pay
                        if self.al_chbox_bank_var.get():
                            if client.pay_bank:
                                self.clients_tree_obj.append(client)
                                entry = client.entries()
                                entries.append(entry)
                        else:
                            self.clients_tree_obj.append(client)
                            entry = client.entries()
                            entries.append(entry)
            return entries

        def build_tree(header_):
            for col in header_:
                self.clients_tree.heading(col, text=col.title())
                self.clients_tree.column(col, width=tkFont.Font().measure(col.title()))

        if self.pa_chbox_var.get():
            header = cl.Client.str_header
        else:
            header = cl.Alumn.str_header
        self.clients_tree.config(columns=header, show='headings')
        self.sort_clients()
        for object in self.clients_tree_ids:
            self.clients_tree.delete(object)
        self.clients_tree_obj = list()  # the original object
        self.clients_tree_ids = list()  # the treeview object
        entry_list = create_table()
        build_tree(header)
        for item in entry_list:
            self.clients_tree_ids.append(self.clients_tree.insert('', 'end', values=item))
            for ix, val in enumerate(item):
                col_w = tkFont.Font().measure(val)
                if self.clients_tree.column(header[ix], width=None) < col_w:
                    self.clients_tree.column(header[ix], width=col_w)

    def sort_clients(self):
        def normal_name_sort(clients):
            clients.sort(key=lambda client: (client.name, client.surname))

        def inverse_name_sort(clients):
            clients.sort(key=lambda client: (client.name, client.surname))
            clients.reverse()

        def normal_surname_sort(clients):
            clients.sort(key=lambda client: (client.surname, client.name))

        def inverse_surname_sort(clients):
            clients.sort(key=lambda client: (client.surname, client.name))
            clients.reverse()

        def read_widgets(clients):
            if self.cl_inverse_sort_var.get() is 0:
                if self.cl_name_sort_var.get() is 1:
                    normal_name_sort(clients)
                elif self.cl_surname_sort_var.get() is 1:
                    normal_surname_sort(clients)
            else:
                if self.cl_name_sort_var.get() is 1:
                    inverse_name_sort(clients)
                elif self.cl_surname_sort_var.get() is 1:
                    inverse_surname_sort(clients)

        read_widgets(self.clients)
        read_widgets(self.alumns)

    def sort_clients_event(self, invoker):
        def write_widget():
            if invoker is 'name':
                self.cl_name_sort_var.set(1)
                self.cl_name_sort_chbox.select()
                self.cl_surname_sort_var.set(0)
                self.cl_surname_sort_chbox.deselect()
            elif invoker is 'surname':
                self.cl_surname_sort_var.set(1)
                self.cl_surname_sort_chbox.select()
                self.cl_name_sort_var.set(0)
                self.cl_name_sort_chbox.deselect()
            elif invoker is 'inverse':
                if self.cl_inverse_sort_var.get() is 1:
                    self.cl_inverse_sort_var.set(0)
                    self.cl_inverse_sort_chbox.deselect()
                else:
                    self.cl_inverse_sort_var.set(1)
                    self.cl_inverse_sort_chbox.select()

        write_widget()
        self.sort_clients()
        self.clients_tree_update()

    def search_clients(self):
        self.cl_chbox_var.set(0)
        self.pa_chbox_var.set(0)
        self.al_chbox_var.set(0)
        self.al_chbox_bank_var.set(0)
        self.search_isactive = True
        keyword = self.cl_search_entry.get()
        clients_alumns = self.clients+self.alumns
        names_surnames = list(map(lambda client:client.name+' '+client.surname,clients_alumns))
        self.searched_clients = list()
        counter=0
        for name_surname in names_surnames:
            if keyword in name_surname:
                self.searched_clients.append(clients_alumns[counter])
            counter = counter + 1
        self.searched_clients = list(set(self.searched_clients))
        self.clients_tree_update()

    def clear_search_clients(self):
        self.search_isactive = False
        self.cl_search_entry.delete(0,tk.END)
        self.clients_tree_update()

    def view_client(self):
        if len(self.clients_tree.selection()) is 0:
            return
        selected_index = self.clients_tree.index(self.clients_tree.selection()[0])
        if not selected_index is -1:
            client = self.clients_tree_obj[selected_index]
            if self.popup_root.isalive:
                self.popup_root.destroy()
            self.popup_root = TkSecure()
            if type(client) is cl.Client:
                popup = ClientUI(self.popup_root, client)
            elif type(client) is cl.Alumn:
                popup = ClientUI(self.popup_root, client, self.groups)
            self.popup_root.mainloop()
            self.popup_root.destroy()

    def new_client(self):
        id_new_element = gr.available_id(self.clients + self.alumns)
        if self.popup_root.isalive:
            self.popup_root.destroy()
        self.popup_root = TkSecure()
        if self.pa_chbox_var.get() or self.cl_chbox_var.get():
            popup = ModifyClientUI(self.popup_root, cl.Client(), id_new_element, self.groups)
        else:
            popup = ModifyClientUI(self.popup_root, cl.Alumn(), id_new_element, self.groups)
        self.popup_root.mainloop()
        self.popup_root.destroy()
        if popup.new:
            if type(popup.client) is cl.Client:
                self.clients.append(popup.client)
            if type(popup.client) is cl.Alumn:
                self.alumns.append(popup.client)
        self.clients_tree_update()
        self.groups_tree_update()

    def modify_client(self):
        if len(self.clients_tree.selection()) is 0:
            return
        selected_index = self.clients_tree.index(self.clients_tree.selection()[0])
        client = self.clients_tree_obj[selected_index]
        if self.popup_root.isalive:
            self.popup_root.destroy()
        self.popup_root = TkSecure()
        popup = ModifyClientUI(self.popup_root, client, None, self.groups)
        self.popup_root.mainloop()
        self.popup_root.destroy()
        if popup.new:
            # remove in_client from list
            if type(client) is cl.Client:
                self.clients.remove(client)
            elif type(client) is cl.Alumn:
                self.alumns.remove(client)
            # add out_client from list
            if type(popup.client) is cl.Client:
                self.clients.append(popup.client)
            elif type(popup.client) is cl.Alumn:
                self.alumns.append(popup.client)
        self.clients_tree_update()
        self.groups_tree_update()

    def delete_client(self):
        if len(self.clients_tree.selection()) is 0:
            return
        selected_index = self.clients_tree.index(self.clients_tree.selection()[0])
        client = self.clients_tree_obj[selected_index]
        if self.popup_root.isalive:
            self.popup_root.destroy()
        if self.popup_root.isalive:
            self.popup_root.destroy()
        self.popup_root = TkSecure()
        popup = AreYouSureUI(self.popup_root)
        self.popup_root.mainloop()
        self.popup_root.destroy()
        if popup.answer:
            if type(client) is cl.Client:
                self.clients.remove(client)
            if type(client) is cl.Alumn:
                self.alumns.remove(client)
            self.purge_member_from_groups(client)
        self.clients_tree_update()
        self.groups_tree_update()

    def purge_member_from_groups(self, client):
        for group in self.groups:
            if client.id in group.members:
                group.members.remove(client.id)

    # GROUPS FUNCTIONALITY
    def groups_list_window(self):
        self.groups_frame.tkraise()

    def groups_tree_update(self):

        def create_table():
            entries = list()
            for group in self.groups:
                self.groups_tree_obj.append(group)
                entry = group.entries()
                entries.append(entry)
            return entries

        def build_tree(header_):
            for col in header_:
                self.groups_tree.heading(col, text=col.title())
                self.groups_tree.column(col, width=tkFont.Font().measure(col.title()))

        header = gr.Group.str_header
        self.groups_tree.config(columns=header, show='headings')
        self.sort_groups()
        for object in self.groups_tree_ids:
            self.groups_tree.delete(object)
        self.groups_tree_obj = list()
        self.groups_tree_ids = list()
        entry_list = create_table()
        build_tree(header)
        for item in entry_list:
            self.groups_tree_ids.append(self.groups_tree.insert('', 'end', values=item))
            for ix, val in enumerate(item):
                col_w = tkFont.Font().measure(val)
                if self.groups_tree.column(header[ix], width=None) < col_w:
                    self.groups_tree.column(header[ix], width=col_w)

    def sort_groups(self):
        def normal_activity_sort(groups):
            groups.sort(key=lambda group: (group.name_activity, group.name_teacher))

        def inverse_activity_sort(groups):
            groups.sort(key=lambda group: (group.name_activity, group.name_teacher))
            groups.reverse()

        def normal_teacher_sort(groups):
            groups.sort(key=lambda group: (group.name_teacher, group.name_activity))

        def inverse_teacher_sort(groups):
            groups.sort(key=lambda group: (group.name_teacher, group.name_activity))
            groups.reverse()

        if self.gr_inverse_sort_var.get() is 0:
            if self.gr_activity_sort_var.get() is 1:
                normal_activity_sort(self.groups)
            elif self.gr_teacher_sort_var.get() is 1:
                normal_teacher_sort(self.groups)
        else:
            if self.gr_activity_sort_var.get() is 1:
                inverse_activity_sort(self.groups)
            elif self.gr_teacher_sort_var.get() is 1:
                inverse_teacher_sort(self.groups)

    def sort_groups_event(self, invoker):
        def widget_logic():
            if invoker is 'activity':
                self.gr_activity_sort_var.set(1)
                self.gr_activity_sort_chbox.select()
                self.gr_teacher_sort_var.set(0)
                self.gr_teacher_sort_chbox.deselect()
            elif invoker is 'teacher':
                self.gr_teacher_sort_var.set(1)
                self.gr_teacher_sort_chbox.select()
                self.gr_activity_sort_var.set(0)
                self.gr_activity_sort_chbox.deselect()
            elif invoker is 'inverse':
                if self.gr_inverse_sort_var.get() is 1:
                    self.gr_inverse_sort_var.set(0)
                    self.gr_inverse_sort_chbox.deselect()
                else:
                    self.gr_inverse_sort_var.set(1)
                    self.gr_inverse_sort_chbox.select()

        widget_logic()
        self.sort_groups()
        self.groups_tree_update()

    def view_group(self):
        if len(self.groups_tree.selection()) is 0:
            return
        selected_index = self.groups_tree.index(self.groups_tree.selection()[0])
        if not selected_index is -1:
            group = self.groups_tree_obj[selected_index]
            if self.popup_root.isalive:
                self.popup_root.destroy()
            self.popup_root = TkSecure()
            popup = GroupUI(self.popup_root, group, self.alumns)
            self.popup_root.mainloop()
            self.popup_root.destroy()

    def new_group(self):
        id_new_element = gr.available_id(self.groups)
        if self.popup_root.isalive:
            self.popup_root.destroy()
        self.popup_root = TkSecure()
        popup = ModifyGroupUI(self.popup_root, gr.Group(), id_new_element, self.alumns)
        self.popup_root.mainloop()
        self.popup_root.destroy()
        if popup.new:
            self.groups.append(popup.group)
        self.groups_tree_update()
        self.clients_tree_update()

    def modify_group(self):
        if len(self.groups_tree.selection()) is 0:
            return
        selected_index = self.groups_tree.index(self.groups_tree.selection()[0])
        group = self.groups_tree_obj[selected_index]
        if self.popup_root.isalive:
            self.popup_root.destroy()
        self.popup_root = TkSecure()
        popup = ModifyGroupUI(self.popup_root, group, None, self.alumns)
        self.popup_root.mainloop()
        self.popup_root.destroy()
        if popup.new:
            self.groups.remove(group)
            self.groups.append(popup.group)
        self.groups_tree_update()

    def delete_group(self):
        if len(self.groups_tree.selection()) is 0:
            return
        selected_index = self.groups_tree.index(self.groups_tree.selection()[0])
        group = self.groups_tree_obj[selected_index]
        if self.popup_root.isalive:
            self.popup_root.destroy()
        self.popup_root = TkSecure()
        popup = AreYouSureUI(self.popup_root)
        self.popup_root.mainloop()
        self.popup_root.destroy()
        if popup.answer:
            self.groups.remove(group)
            self.purge_group_from_alumns(group)
        self.groups_tree_update()
        self.clients_tree_update()

    def purge_group_from_alumns(self, group):
        for client in self.alumns:
            if group.id in client.groups:
                client.groups.remove(group.id)

    # INVENTORY FUNCTIONALITY
    def items_list_window(self):
        self.items_frame.tkraise()

    def sort_items_event(self, invoker):
        pass

    def view_item(self):
        pass

    def new_item(self):
        pass

    def modify_item(self):
        pass

    def delete_item(self):
        pass

    # GENERAL FUNCTIONALITY
    def export_selection(self):
        pass

    def save_all_info(self):
        io.write_clients(file_clients, self.clients, cl.Client)
        io.write_clients(file_alumns, self.alumns, cl.Alumn)
        io.write_groups(file_groups, self.groups)

    def close_program(self):
        self.save_all_info()
        self.root.quit()


class ClientUI:
    def __init__(self, popup_root, client, available_groups=list()):
        self.popup_root = popup_root
        self.popup_root.title('Cliente: ' + client.name + ' ' + client.surname)
        original_geometry = [200, 150]
        str_original_geometry = map(str, original_geometry)
        self.popup_root.geometry('x'.join(str_original_geometry))
        self.popup_root.protocol("WM_DELETE_WINDOW", self.close_window)
        self.client = client
        self.available_groups = available_groups

        self.main_frame = tk.Frame(self.popup_root)
        self.main_frame.pack(fill='both', expand=True)
        # FIELDS
        name_field = tk.Label(self.main_frame, text='Nombre: ')
        name_field.grid(row=0, column=0, sticky=tk.N + tk.W)
        surname_field = tk.Label(self.main_frame, text='Apellidos: ')
        surname_field.grid(row=1, column=0, sticky=tk.N + tk.W)
        id_card_field = tk.Label(self.main_frame, text='DNI: ')
        id_card_field.grid(row=2, column=0, sticky=tk.N + tk.W)
        phone1_field = tk.Label(self.main_frame, text='Tlf 1: ')
        phone1_field.grid(row=3, column=0, sticky=tk.N + tk.W)
        phone2_field = tk.Label(self.main_frame, text='Tlf 2:')
        phone2_field.grid(row=4, column=0, sticky=tk.N + tk.W)
        email_field = tk.Label(self.main_frame, text='E-mail: ')
        email_field.grid(row=5, column=0, sticky=tk.N + tk.W)
        client_id_field = tk.Label(self.main_frame, text='ID Cliente: ')
        client_id_field.grid(row=6, column=0, sticky=tk.N + tk.W)

        # FIELD VALUES
        self.name_ans = tk.Label(self.main_frame, text=self.client.name)
        self.name_ans.grid(row=0, column=1, sticky=tk.N + tk.W)
        self.surname_ans = tk.Label(self.main_frame, text=self.client.surname)
        self.surname_ans.grid(row=1, column=1, sticky=tk.N + tk.W)
        self.id_card_ans = tk.Label(self.main_frame, text=self.client.id_card)
        self.id_card_ans.grid(row=2, column=1, sticky=tk.N + tk.W)
        self.phone1_ans = tk.Label(self.main_frame, text=self.client.phone1)
        self.phone1_ans.grid(row=3, column=1, sticky=tk.N + tk.W)
        self.phone2_ans = tk.Label(self.main_frame, text=self.client.phone2)
        self.phone2_ans.grid(row=4, column=1, sticky=tk.N + tk.W)
        self.email_ans = tk.Label(self.main_frame, text=self.client.email)
        self.email_ans.grid(row=5, column=1, sticky=tk.N + tk.W)
        self.client_id_ans = tk.Label(self.main_frame, text=self.client.id)
        self.client_id_ans.grid(row=6, column=1, sticky=tk.N + tk.W)

        if type(client) is cl.Alumn:
            self.popup_root.title('Cliente: ' + client.name + ' ' + client.surname)
            original_geometry = [600, 220]
            str_original_geometry = map(str, original_geometry)
            self.popup_root.geometry('x'.join(str_original_geometry))
            # FIELDS
            pay_bank_field = tk.Label(self.main_frame, text='Domicilia?:')
            pay_bank_field.grid(row=8, column=0, sticky=tk.N + tk.W)
            bank_acc_field = tk.Label(self.main_frame, text='IBAN:')
            bank_acc_field.grid(row=9, column=0, sticky=tk.N + tk.W)
            pay_period_field = tk.Label(self.main_frame, text='Tipo Pago:')
            pay_period_field.grid(row=10, column=0, sticky=tk.N + tk.W)

            # FIELD VALUES
            if client.pay_bank:
                pay_bank = 'Si'
            else:
                pay_bank = 'No'
            if client.pay_period is 0:
                pay_period = 'Mensual'
            elif client.pay_period is 1:
                pay_period = 'Trimestral'
            elif client.pay_period is 2:
                pay_period = 'Anual'
            else:
                pay_period = 'Desconocido'
            self.pay_bank_ans = tk.Label(self.main_frame, text=pay_bank)
            self.pay_bank_ans.grid(row=8, column=1, sticky=tk.N + tk.W)
            self.bank_acc_ans = tk.Label(self.main_frame, text=client.bank_acc)
            self.bank_acc_ans.grid(row=9, column=1, sticky=tk.N + tk.W)
            self.pay_period_ans = tk.Label(self.main_frame, text=pay_period)
            self.pay_period_ans.grid(row=10, column=1, sticky=tk.N + tk.W)

            # Groups Labels
            self.groups_frame_init()
            titlegroups_label = tk.Label(self.groups_frame, text='Miembro de: ')
            titlegroups_label.grid(sticky=tk.W)
            for group in self.available_groups:
                group_checkbox = tk.Checkbutton(self.groups_frame, text=group.display(), state=tk.DISABLED)
                group_checkbox.grid(sticky=tk.W, padx=(10, 0))
                if group.id in self.client.groups:
                    group_checkbox.select()
                else:
                    group_checkbox.deselect()

    def groups_frame_init(self):
        self.groups_frame = tk.Frame(self.main_frame, width=600)
        self.groups_frame.grid(row=0, rowspan=20, column=3, columnspan=2, sticky=tk.N + tk.W + tk.E + tk.S,
                               padx=(20, 0))

    def close_window(self):
        self.popup_root.quit()


class ModifyClientUI(ClientUI):
    def __init__(self, popup_root, client, new_id=None, available_groups=list()):
        super().__init__(popup_root, client)
        self.saved = True
        if client.name is '':
            self.popup_root.title('Nuevo Cliente')
        original_geometry = [300, 300]
        str_original_geometry = map(str, original_geometry)
        self.popup_root.geometry('x'.join(str_original_geometry))
        self.client = client
        self.new_id = new_id
        self.available_groups = available_groups
        self.new = False
        # NEW FIELD VALUES
        self.name_new = tk.Entry(self.main_frame, text=self.client.name)
        self.name_new.delete(0, tk.END)
        self.name_new.insert(0, self.client.name)
        self.name_new.grid(row=0, column=2, sticky=tk.N + tk.W)
        self.surname_new = tk.Entry(self.main_frame, text=self.client.surname)
        self.surname_new.delete(0, tk.END)
        self.surname_new.insert(0, self.client.surname)
        self.surname_new.grid(row=1, column=2, sticky=tk.N + tk.W)
        self.id_card_new = tk.Entry(self.main_frame, text=self.client.id_card)
        self.id_card_new.delete(0, tk.END)
        self.id_card_new.insert(0, self.client.id_card)
        self.id_card_new.grid(row=2, column=2, sticky=tk.N + tk.W)
        self.phone1_new = tk.Entry(self.main_frame, text=self.client.phone1)
        self.phone1_new.delete(0, tk.END)
        self.phone1_new.insert(0, self.client.phone1)
        self.phone1_new.grid(row=3, column=2, sticky=tk.N + tk.W)
        self.phone2_new = tk.Entry(self.main_frame, text=self.client.phone2)
        self.phone2_new.delete(0, tk.END)
        self.phone2_new.insert(0, self.client.phone2)
        self.phone2_new.grid(row=4, column=2, sticky=tk.N + tk.W)
        self.email_new = tk.Entry(self.main_frame, text=self.client.email)
        self.email_new.delete(0, tk.END)
        self.email_new.insert(0, self.client.email)
        self.email_new.grid(row=5, column=2, sticky=tk.N + tk.W)

        if type(client) is cl.Alumn:
            original_geometry = [900, 320]
            str_original_geometry = map(str, original_geometry)
            self.popup_root.geometry('x'.join(str_original_geometry))
            self.pay_bank_new_var = tk.IntVar()
            self.pay_bank_new = tk.Checkbutton(self.main_frame, variable=self.pay_bank_new_var,
                                               command=lambda: self.press_pay_bank_ans())
            if self.client.pay_bank:
                self.pay_bank_new_var.set(1)
                self.pay_bank_new.select()
                self.pay_bank_new.config(text='Si')
            else:
                self.pay_bank_new_var.set(0)
                self.pay_bank_new.deselect()
                self.pay_bank_new.config(text='No')
            self.pay_bank_new.grid(row=8, column=2, sticky=tk.N + tk.W)
            self.bank_acc_new = tk.Entry(self.main_frame)
            self.bank_acc_new.delete(0, tk.END)
            self.bank_acc_new.insert(0, self.client.bank_acc)
            self.bank_acc_new.grid(row=9, column=2, sticky=tk.N + tk.W)
            self.pay_period_miniframe = tk.Frame(self.main_frame)
            self.pay_period_miniframe.grid(row=10, column=2, sticky=tk.N + tk.W)
            self.month_var = tk.IntVar()
            self.month_checkbox = tk.Checkbutton(self.pay_period_miniframe, text='Mensual ', variable=self.month_var,
                                                 command=lambda: self.press_period_ans('Month'), onvalue=1, offvalue=0)
            if self.client.pay_period is 0:
                self.month_var.set(1)
                self.month_checkbox.select()
            else:
                self.month_var.set(0)
                self.month_checkbox.deselect()
            self.month_checkbox.grid(row=0, column=2, sticky=tk.N + tk.W)
            self.trimonth_var = tk.IntVar()
            self.trimonth_checkbox = tk.Checkbutton(self.pay_period_miniframe, text='Trimestral',
                                                    variable=self.trimonth_var,
                                                    command=lambda: self.press_period_ans('Trimonth'), onvalue=1,
                                                    offvalue=0)
            if self.client.pay_period is 1:
                self.trimonth_var.set(1)
                self.trimonth_checkbox.select()
            else:
                self.trimonth_var.set(0)
                self.trimonth_checkbox.deselect()
            self.trimonth_checkbox.grid(row=1, column=2, sticky=tk.N + tk.W)
            self.year_var = tk.IntVar()
            self.year_checkbox = tk.Checkbutton(self.pay_period_miniframe, text='Anual ', variable=self.year_var,
                                                command=lambda: self.press_period_ans('Year'), onvalue=1, offvalue=0)
            if self.client.pay_period is 2:
                self.year_var.set(1)
                self.year_checkbox.select()
            else:
                self.year_var.set(0)
                self.year_checkbox.deselect()
            self.year_checkbox.grid(row=2, column=2, sticky=tk.N + tk.W)

            self.groups_frame.destroy()
            self.groups_frame_init()
            titlegroups_label = tk.Label(self.groups_frame, text='Miembro de: ')
            titlegroups_label.grid(sticky=tk.W)
            self.groups_var = list()
            self.groups_checkboxes = list()
            self.groups_id_list = list()
            for group in self.available_groups:
                group_var = tk.IntVar()
                group_checkbox = tk.Checkbutton(self.groups_frame, text=group.display())
                group_checkbox.bind('<Button-1>', self.press_group_checkbox)
                group_checkbox.grid(sticky=tk.W, padx=(10, 0))
                if group.id in self.client.groups:
                    group_var.set(1)
                    group_checkbox.select()
                else:
                    group_var.set(0)
                    group_checkbox.deselect()
                self.groups_var.append(group_var)
                self.groups_checkboxes.append(group_checkbox)
                self.groups_id_list.append(group.id)

        save_button = tk.Button(self.main_frame, text='Guardar', command=self.check_save)
        self.save_button_row = 15
        save_button.grid(row=self.save_button_row, column=0, columnspan=5, sticky=tk.S)
        if type(self.client) is cl.Alumn:
            trans_label = 'Transformar en Paciente'
        else:
            trans_label = 'Transformar en Alumno'
        transform_button = tk.Button(self.main_frame, text=trans_label, command=self.transform_client)
        transform_button.grid(row=self.save_button_row + 1, column=0, columnspan=5, sticky=tk.S)

    def press_group_checkbox(self, event):
        counter = 0
        for checkbox in self.groups_checkboxes:
            if event.widget is checkbox:
                if self.groups_var[counter].get() is 0:
                    self.groups_var[counter].set(1)
                else:
                    self.groups_var[counter].set(0)
            counter = counter + 1

    def press_pay_bank_ans(self):
        if self.pay_bank_new_var.get() is 0:
            self.pay_bank_new_var.set(1)
            self.pay_bank_new.config(text='Si')
        else:
            self.pay_bank_new_var.set(0)
            self.pay_bank_new.config(text='No')

    def press_period_ans(self, invoker):
        if invoker is 'Month':
            self.month_var.set(1)
            self.month_checkbox.select()
            self.trimonth_var.set(0)
            self.trimonth_checkbox.deselect()
            self.year_var.set(0)
            self.year_checkbox.deselect()
        if invoker is 'Trimonth':
            self.month_var.set(0)
            self.month_checkbox.deselect()
            self.trimonth_var.set(1)
            self.trimonth_checkbox.select()
            self.year_var.set(0)
            self.year_checkbox.deselect()
        if invoker is 'Year':
            self.month_var.set(0)
            self.month_checkbox.deselect()
            self.trimonth_var.set(0)
            self.trimonth_checkbox.deselect()
            self.year_var.set(1)
            self.year_checkbox.select()

    def transform_client(self):
        self.popup_root.grab_set()
        areusure_root = tk.Tk()
        message1 = '¿Estas seguro de que quieres transformar este cliente?'
        if type(self.client) is cl.Alumn:
            message2 = 'Estas transformando un Alumno en Paciente, perderas su informacion Bancaria'
        else:
            message2 = ''
        areusure = AreYouSureUI(areusure_root, message1, message2)
        areusure_root.mainloop()
        areusure_root.destroy()
        if areusure.answer:
            if type(self.client) is cl.Client:
                self.client = cl.cast_client_alumn(self.client)
            elif type(self.client) is cl.Alumn:
                self.client = cl.cast_alumn_client(self.client)
        self.popup_root.grab_release()
        self.reset_window()

    def reset_window(self):
        self.main_frame.destroy()
        self.__init__(self.popup_root, self.client, self.new_id, self.available_groups)

    def check_save(self):
        if self.info_integrity():
            self.client.name = self.name_new.get()
            self.client.surname = self.surname_new.get()
            self.client.id_card = self.id_card_new.get()
            self.client.phone1 = self.phone1_new.get()
            self.client.phone2 = self.phone2_new.get()
            self.client.email = self.email_new.get()
            if not self.new_id is None:
                self.client.id = self.new_id
            if type(self.client) is cl.Alumn:
                counter = 0
                for checkbox_var in self.groups_var:
                    if checkbox_var.get() is 1:
                        self.client.groups.add(self.groups_id_list[counter])
                        self.update_group(self.available_groups[counter], self.client.id, 'add')
                    else:
                        self.client.groups.discard(self.groups_id_list[counter])
                        self.update_group(self.available_groups[counter], self.client.id, 'remove')
                    counter = counter + 1
                self.client.pay_bank = bool(self.pay_bank_new_var.get())
                self.client.bank_acc = self.bank_acc_new.get()
                if self.month_var.get() is 1:
                    self.client.pay_period = 0
                elif self.trimonth_var.get() is 1:
                    self.client.pay_period = 1
                elif self.year_var.get() is 1:
                    self.client.pay_period = 2
                else:
                    self.client.pay_period = -1

            self.update_answers()
            self.saved = True
            self.new = True
        else:
            error_label = tk.Label(self.main_frame, text='Error al Guardar, revisa la informacion introducida.',
                                   fg='red')
            error_label.grid(row=self.save_button_row - 1, column=0, columnspan=5, sticky=tk.S)

    def update_group(self, group, client_id, action):
        if action is 'add':
            group.members.add(client_id)
        else:
            group.members.discard(client_id)

    def update_answers(self):
        self.name_ans.config(text=self.client.name)
        self.surname_ans.config(text=self.client.surname)
        self.id_card_ans.config(text=self.client.id_card)
        self.phone1_ans.config(text=self.client.phone1)
        self.phone2_ans.config(text=self.client.phone2)
        self.email_ans.config(text=self.client.email)
        self.client_id_ans.config(text=self.client.id)
        if type(self.client) is cl.Alumn:
            if self.client.pay_bank:
                pay_bank = 'Si'
            else:
                pay_bank = 'No'
            if self.client.pay_period is 0:
                pay_period = 'Mensual'
            elif self.client.pay_period is 1:
                pay_period = 'Trimestral'
            elif self.client.pay_period is 2:
                pay_period = 'Anual'
            else:
                pay_period = 'Desconocido'
            self.pay_bank_ans.config(text=pay_bank)
            self.bank_acc_ans.config(text=self.client.bank_acc)
            self.pay_period_ans.config(text=pay_period)

    def info_integrity(self):
        info_integrity = True
        info_integrity = info_integrity * self.check_semicolons()
        return info_integrity

    def check_semicolons(self):
        no_semicolon = True
        var_list = [self.name_new.get(), self.surname_new.get(), self.id_card_new.get(), self.phone1_new.get(),
                    self.phone2_new.get(), self.email_new.get()]
        if self.client is cl.Alumn:
            var_list = var_list + [self.bank_acc_new.get()]
        for var in var_list:
            no_semicolon = no_semicolon and not (';' in var)
        return no_semicolon

    def check_differences_ans_new(self):
        self.saved = True
        if self.client.name != self.name_new.get(): self.saved = False
        if self.client.surname != self.surname_new.get(): self.saved = False
        if self.client.id_card != self.id_card_new.get(): self.saved = False
        if self.client.phone1 != self.phone1_new.get(): self.saved = False
        if self.client.phone2 != self.phone2_new.get(): self.saved = False
        if self.client.email != self.email_new.get(): self.saved = False
        if type(self.client) is cl.Alumn:
            if self.client.pay_bank != self.pay_bank_new_var.get(): self.saved = False
            if self.client.bank_acc != self.bank_acc_new: self.saved = False
            if self.month_var.get() is 1:
                pay_period_new = 0
            elif self.trimonth_var.get() is 1:
                pay_period_new = 1
            elif self.year_var.get() is 1:
                pay_period_new = 2
            else:
                pay_period_new = -1
            if self.client.pay_period != pay_period_new: self.saved = False
            counter = 0
            for checkbox_var in self.groups_var:
                if checkbox_var.get() is 1:
                    if not self.groups_id_list[counter] in self.client.groups: self.saved = False
                else:
                    if self.groups_id_list[counter] in self.client.groups: self.saved = False
                counter = counter + 1

    def close_window(self):
        self.check_differences_ans_new()
        if not self.saved:
            areusure_root = tk.Tk()
            message1 = 'No has guardado, ¿Quieres guardar la información?'
            message2 = ''
            areusure = AreYouSureUI(areusure_root, message1, message2)
            areusure_root.mainloop()
            areusure_root.destroy()
            if areusure.answer:
                self.check_save()
        super().close_window()


class GroupUI:
    def __init__(self, root, group, available_clients=list()):
        self.root = root
        self.root.title('Grupo: ' + group.name_activity + ' ' + group.name_teacher + ' ' + str(group.days) + ' '
                        + str(group.time_start))
        original_geometry = [1150, 500]
        str_original_geometry = map(str, original_geometry)
        self.root.geometry('x'.join(str_original_geometry))
        self.root.protocol("WM_DELETE_WINDOW", self.close_window)
        self.group = group
        self.available_clients = available_clients

        # FIELDS
        name_activity_field = tk.Label(self.root, text='Actividad: ')
        name_activity_field.grid(row=0, column=0, sticky=tk.N + tk.W)
        name_teacher_field = tk.Label(self.root, text='Monitor/a: ')
        name_teacher_field.grid(row=1, column=0, sticky=tk.N + tk.W)
        days_field = tk.Label(self.root, text='Dias: ')
        days_field.grid(row=2, column=0, sticky=tk.N + tk.W)
        time_field = tk.Label(self.root, text='Horario: ')
        time_field.grid(row=3, column=0, sticky=tk.N + tk.W)
        price_field = tk.Label(self.root, text='Precio: ')
        price_field.grid(row=4, column=0, sticky=tk.N + tk.W)
        members_number_field = tk.Label(self.root, text='Numero Miembros')
        members_number_field.grid(row=5, column=0, sticky=tk.N + tk.W)
        members_limit_field = tk.Label(self.root, text='Limite Miembros')
        members_limit_field.grid(row=6, column=0, sticky=tk.N + tk.W)
        group_id_field = tk.Label(self.root, text='ID Grupo: ')
        group_id_field.grid(row=7, column=0, sticky=tk.N + tk.W)

        # FIELD VALUES
        self.name_activity_ans = tk.Label(self.root, text=group.name_activity)
        self.name_activity_ans.grid(row=0, column=1, sticky=tk.N + tk.W)
        self.name_teacher_ans = tk.Label(self.root, text=group.name_teacher)
        self.name_teacher_ans.grid(row=1, column=1, sticky=tk.N + tk.W)
        self.days_ans = tk.Label(self.root, text=group.days_format())
        self.days_ans.grid(row=2, column=1, sticky=tk.N + tk.W)
        self.time_ans = tk.Label(self.root, text=group.timetable_format())
        self.time_ans.grid(row=3, column=1, sticky=tk.N + tk.W)
        self.price_ans = tk.Label(self.root, text=str(group.price) + ' EUR')
        self.price_ans.grid(row=4, column=1, sticky=tk.N + tk.W)
        self.members_number_ans = tk.Label(self.root, text=str(len(group.members)))
        self.members_number_ans.grid(row=5, column=1, sticky=tk.N + tk.W)
        self.members_limit_ans = tk.Label(self.root, text=str(group.limit_members))
        self.members_limit_ans.grid(row=6, column=1, sticky=tk.N + tk.W)
        self.group_id_ans = tk.Label(self.root, text=str(group.id))
        self.group_id_ans.grid(row=7, column=1, sticky=tk.N + tk.W)

        # MEMBERS LIST
        self.members_listbox_frame = tk.Frame(self.root, width=800)
        self.members_listbox_frame.grid(row=0, rowspan=20, column=3, sticky=tk.N + tk.W + tk.E + tk.S)
        self.members_listbox = tk.Listbox(self.members_listbox_frame, width=60, height=30)
        self.members_listbox.grid(row=0, column=0, sticky=tk.N + tk.W)
        self.update_members_listbox()

    def update_members_listbox(self):
        self.members_listbox.delete(0, tk.END)
        self.members_listbox.insert(tk.END, cl.Alumn.str_header)
        ids = list(map(lambda client: client.id, self.available_clients))
        self.members_listbox_obj = list()
        for member_id in self.group.members:
            index_client = ids.index(member_id)
            client = self.available_clients[index_client]
            self.members_listbox_obj.append(client)
            self.members_listbox.insert(tk.END, str(client))

    def close_window(self):
        self.root.quit()


class ModifyGroupUI(GroupUI):
    def __init__(self, root, group, new_id=None, available_clients=list()):
        super().__init__(root, group, available_clients)
        self.saved = True
        self.group = group
        self.new_id = new_id
        self.new = False
        self.available_clients = available_clients

        # FIELD ENTRIES
        self.name_activity_new = tk.Entry(self.root)
        self.name_activity_new.delete(0, tk.END)
        self.name_activity_new.insert(0, group.name_activity)
        self.name_activity_new.grid(row=0, column=2, sticky=tk.N + tk.W)
        self.name_teacher_new = tk.Entry(self.root)
        self.name_teacher_new.delete(0, tk.END)
        self.name_teacher_new.insert(0, group.name_teacher)
        self.name_teacher_new.grid(row=1, column=2, sticky=tk.N + tk.W)
        days_new_frame = tk.Frame(self.root)
        days_new_frame.grid(row=2, column=2, sticky=tk.N + tk.W)
        self.monday_var = tk.IntVar()
        self.monday_checkbox = tk.Checkbutton(days_new_frame, variable=self.monday_var, text='Lunes',
                                              command=lambda: self.press_days_checkbox('monday'))
        self.monday_checkbox.grid(sticky=tk.W)
        if 'L' in self.group.days:
            self.monday_checkbox.select()
            self.monday_var.set(1)
        self.tuesday_var = tk.IntVar()
        self.tuesday_checkbox = tk.Checkbutton(days_new_frame, variable=self.tuesday_var, text='Martes',
                                               command=lambda: self.press_days_checkbox('tuesday'))
        self.tuesday_checkbox.grid(sticky=tk.W)
        if 'M' in self.group.days:
            self.tuesday_checkbox.select()
            self.tuesday_var.set(1)
        self.wednesday_var = tk.IntVar()
        self.wednesday_checkbox = tk.Checkbutton(days_new_frame, variable=self.wednesday_var, text='Miercoles',
                                                 command=lambda: self.press_days_checkbox('wednesday'))
        self.wednesday_checkbox.grid(sticky=tk.W)
        if 'X' in self.group.days:
            self.wednesday_checkbox.select()
            self.wednesday_var.set(1)
        self.thrusday_var = tk.IntVar()
        self.thrusday_checkbox = tk.Checkbutton(days_new_frame, variable=self.thrusday_var, text='Jueves',
                                                command=lambda: self.press_days_checkbox('thrusday'))
        self.thrusday_checkbox.grid(sticky=tk.W)
        if 'J' in self.group.days:
            self.thrusday_checkbox.select()
            self.thrusday_var.set(1)
        self.friday_var = tk.IntVar()
        self.friday_checkbox = tk.Checkbutton(days_new_frame, variable=self.friday_var, text='Viernes',
                                              command=lambda: self.press_days_checkbox('friday'))
        self.friday_checkbox.grid(sticky=tk.W)
        if 'V' in self.group.days:
            self.friday_checkbox.select()
            self.friday_var.set(1)
        self.saturday_var = tk.IntVar()
        self.saturday_checkbox = tk.Checkbutton(days_new_frame, variable=self.saturday_var, text='Sabado',
                                                command=lambda: self.press_days_checkbox('saturday'))
        self.saturday_checkbox.grid(sticky=tk.W)
        if 'S' in self.group.days:
            self.saturday_checkbox.select()
            self.saturday_var.set(1)
        self.sunday_var = tk.IntVar()
        self.sunday_checkbox = tk.Checkbutton(days_new_frame, variable=self.sunday_var, text='Domingo',
                                              command=lambda: self.press_days_checkbox('sunday'))
        self.sunday_checkbox.grid(sticky=tk.W)
        if 'D' in self.group.days:
            self.sunday_checkbox.select()
            self.sunday_var.set(1)
        time_new_frame = tk.Frame(self.root)
        time_new_frame.grid(row=3, column=2, sticky=tk.N + tk.W)

        start_hour = self.group.timetable_format()[0:2]
        start_min = self.group.timetable_format()[3:5]
        end_hour = self.group.timetable_format()[8:10]
        end_min = self.group.timetable_format()[11:13]
        self.time_start_hour_new = tk.Entry(time_new_frame, justify="right", width=3)
        self.time_start_hour_new.delete(0, tk.END)
        self.time_start_hour_new.insert(0, start_hour)
        self.time_start_hour_new.grid(row=0, column=0, sticky=tk.N + tk.W)
        self.time_start_min_new = tk.Entry(time_new_frame, width=3)
        self.time_start_min_new.delete(0, tk.END)
        self.time_start_min_new.insert(0, start_min)
        self.time_start_min_new.grid(row=0, column=1, sticky=tk.N + tk.W)
        self.time_end_hour_new = tk.Entry(time_new_frame, justify="right", width=3)
        self.time_end_hour_new.delete(0, tk.END)
        self.time_end_hour_new.insert(0, end_hour)
        self.time_end_hour_new.grid(row=1, column=0, sticky=tk.N + tk.W)
        self.time_end_min_new = tk.Entry(time_new_frame, width=3)
        self.time_end_min_new.delete(0, tk.END)
        self.time_end_min_new.insert(0, end_min)
        self.time_end_min_new.grid(row=1, column=1, sticky=tk.N + tk.W)
        self.price_new = tk.Entry(self.root)
        self.price_new.delete(0, tk.END)
        self.price_new.insert(0, str(group.price))
        self.price_new.grid(row=4, column=2, sticky=tk.N + tk.W)
        self.members_limit_new = tk.Entry(self.root)
        self.members_limit_new.delete(0, tk.END)
        self.members_limit_new.insert(0, str(group.limit_members))
        self.members_limit_new.grid(row=6, column=2, sticky=tk.N + tk.W)

        # AVAILABLE CLIENTS LISTBOX
        buttons_frame = tk.Frame(self.members_listbox_frame)
        buttons_frame.grid(row=0, column=1)
        self.add_button = tk.Button(buttons_frame, text='<< Añadir <<', width=15)
        self.add_button.bind('<Button-1>', self.add_member)
        self.add_button.grid(row=0, column=0, sticky=tk.S)
        self.delete_button = tk.Button(buttons_frame, text='>> Eliminar >>', width=15)
        self.delete_button.bind('<Button-1>', self.delete_member)
        self.delete_button.grid(row=1, column=0, sticky=tk.N)
        self.available_clients_listbox = tk.Listbox(self.members_listbox_frame, width=60, height=30)
        self.available_clients_listbox.grid(row=0, column=2, sticky=tk.N + tk.W)
        self.update_available_clients_listbox()

        save_button = tk.Button(self.root, text='Guardar', command=self.check_save)
        self.save_button_row = 10
        save_button.grid(row=self.save_button_row, column=0, columnspan=3, sticky=tk.S)

    def add_member(self, event):
        self.saved = False
        if len(self.available_clients_listbox.curselection()) is 0:
            return
        index = self.available_clients_listbox.curselection()[0] - 1
        self.group.members.add(self.available_clients_listbox_obj[index].id)
        self.update_members_listbox()
        self.update_available_clients_listbox()

    def delete_member(self, event):
        self.saved = False
        if len(self.members_listbox.curselection()) is 0:
            return
        index = self.members_listbox.curselection()[0] - 1
        client = self.members_listbox_obj[index]
        self.group.members.discard(client.id)
        self.update_members_listbox()
        self.update_available_clients_listbox()

    def update_available_clients_listbox(self):
        self.available_clients_listbox.delete(0, tk.END)
        self.available_clients_listbox.insert(tk.END, cl.Alumn.str_header)
        self.available_clients_listbox_obj = list()
        for client in self.available_clients:
            if not client.id in self.group.members:
                self.available_clients_listbox_obj.append(client)
                self.available_clients_listbox.insert(tk.END, str(client))

    def press_days_checkbox(self, invoker):
        if invoker is 'monday':
            if self.monday_var.get() is 0:
                self.monday_var.set(1)
            else:
                self.monday_var.set(0)
        if invoker is 'tuesday':
            if self.tuesday_var.get() is 0:
                self.tuesday_var.set(1)
            else:
                self.tuesday_var.set(0)
        if invoker is 'wednesday':
            if self.wednesday_var.get() is 0:
                self.wednesday_var.set(1)
            else:
                self.wednesday_var.set(0)
        if invoker is 'thrusday':
            if self.thrusday_var.get() is 0:
                self.thrusday_var.set(1)
            else:
                self.thrusday_var.set(0)
        if invoker is 'friday':
            if self.friday_var.get() is 0:
                self.friday_var.set(1)
            else:
                self.friday_var.set(0)
        if invoker is 'saturday':
            if self.saturday_var.get() is 0:
                self.saturday_var.set(1)
            else:
                self.saturday_var.set(0)
        if invoker is 'sunday':
            if self.sunday_var.get() is 0:
                self.sunday_var.set(1)
            else:
                self.sunday_var.set(0)

    def check_save(self):
        if self.info_integrity():
            self.group.name_activity = self.name_activity_new.get()
            self.group.name_teacher = self.name_teacher_new.get()
            self.group.days = set()
            if self.monday_var.get() is 1:
                self.group.days.add('L')
            if self.tuesday_var.get() is 1:
                self.group.days.add('M')
            if self.wednesday_var.get() is 1:
                self.group.days.add('X')
            if self.thrusday_var.get() is 1:
                self.group.days.add('J')
            if self.friday_var.get() is 1:
                self.group.days.add('V')
            if self.saturday_var.get() is 1:
                self.group.days.add('S')
            if self.sunday_var.get() is 1:
                self.group.days.add('D')
            self.group.time_start = int(self.time_start_hour_new.get()) * 100 + int(self.time_start_min_new.get())
            self.group.time_end = int(self.time_end_hour_new.get()) * 100 + int(self.time_end_min_new.get())
            self.group.price = float(self.price_new.get())
            self.group.limit_members = int(self.members_limit_new.get())
            if not self.new_id is None:  # We are modifying an existing group
                self.group.id = self.new_id
            self.update_answers()
            self.new = True
            self.saved = True
        else:
            error_label = tk.Label(self.root, text='Error al Guardar, revisa la informacion introducida.',
                                   fg='red')
            error_label.grid(row=self.save_button_row - 1, column=0, columnspan=3, sticky=tk.S)

    def update_answers(self):
        self.name_activity_ans.config(text=self.group.name_activity)
        self.name_teacher_ans.config(text=self.group.name_teacher)
        self.days_ans.config(text=self.group.days_format())
        self.time_ans.config(text=self.group.timetable_format())
        self.price_ans.config(text=str(self.group.price) + ' EUR')
        self.members_number_ans.config(text=str(len(self.group.members)))
        self.members_limit_ans.config(text=str(self.group.limit_members))
        self.group_id_ans.config(text=str(self.group.id))

    def info_integrity(self):
        info_integrity = True
        info_integrity = info_integrity * self.check_semicolons()
        time_characters = self.time_start_hour_new.get() + self.time_start_min_new.get() + self.time_end_hour_new.get() + self.time_end_min_new.get()

        if len(self.time_start_hour_new.get()) > 2: info_integrity = False
        if len(self.time_start_min_new.get()) > 2: info_integrity = False
        if len(self.time_end_hour_new.get()) > 2: info_integrity = False
        if len(self.time_end_min_new.get()) > 2: info_integrity = False
        for character in time_characters:
            info_integrity = info_integrity * (character in '0123456789')
        if info_integrity:
            if not 0 <= int(self.time_start_hour_new.get()) < 23:
                info_integrity = False
            if not 0 <= int(self.time_start_min_new.get()) < 59:
                info_integrity = False
            if not 0 <= int(self.time_end_hour_new.get()) < 23:
                info_integrity = False
            if not 0 <= int(self.time_end_min_new.get()) < 59:
                info_integrity = False

        return info_integrity

    def check_semicolons(self):
        no_semicolon = True
        var_list = [self.name_activity_new.get(), self.name_teacher_new.get(), self.time_start_hour_new.get(),
                    self.time_start_min_new.get(), self.time_end_hour_new.get(), self.time_end_min_new.get(),
                    self.price_new.get(), self.members_limit_new.get()]
        for var in var_list:
            no_semicolon = no_semicolon and not (';' in var)
        return no_semicolon

    def check_differences_ans_new(self):
        self.saved = True
        if self.group.name_activity != self.name_activity_new.get(): self.saved = False
        if self.group.name_teacher != self.name_teacher_new.get(): self.saved = False
        if self.group.price != float(self.price_new.get()): self.saved = False
        if self.group.limit_members != int(self.members_limit_new.get()): self.saved = False
        if self.group.time_start != int(self.time_start_hour_new.get()) * 100 + int(self.time_start_min_new.get()):
            self.saved = False
        if self.group.time_end != int(self.time_end_hour_new.get()) * 100 + int(self.time_end_min_new.get()):
            self.saved = False
        if self.monday_var.get():
            if not 'L' in self.group.days: self.saved = False
        else:
            if 'L' in self.group.days: self.saved = False
        if self.tuesday_var.get():
            if not 'M' in self.group.days: self.saved = False
        else:
            if 'M' in self.group.days: self.saved = False
        if self.wednesday_var.get():
            if not 'X' in self.group.days: self.saved = False
        else:
            if 'X' in self.group.days: self.saved = False
        if self.thrusday_var.get():
            if not 'J' in self.group.days: self.saved = False
        else:
            if 'J' in self.group.days: self.saved = False
        if self.friday_var.get():
            if not 'F' in self.group.days: self.saved = False
        else:
            if 'F' in self.group.days: self.saved = False
        if self.saturday_var.get():
            if not 'S' in self.group.days: self.saved = False
        else:
            if 'S' in self.group.days: self.saved = False
        if self.sunday_var.get():
            if not 'D' in self.group.days: self.saved = False
        else:
            if 'D' in self.group.days: self.saved = False

    def close_window(self):
        self.check_differences_ans_new()
        if not self.saved:
            areusure_root = tk.Tk()
            message1 = 'No has guardado, ¿Quieres guardar la información?'
            message2 = ''
            areusure = AreYouSureUI(areusure_root, message1, message2)
            areusure_root.mainloop()
            areusure_root.destroy()
            if areusure.answer:
                self.check_save()
                if self.saved:
                    super().close_window()
            else:
                super().close_window()
        else:
            super().close_window()


class AreYouSureUI:
    def __init__(self, root, message1=None, message2=None):
        self.root = root
        if message1 is None:
            message1 = '¿Estas seguro de eliminar este elemento?'
        if message2 is None:
            message2 = 'Esta accion es irreversible'
        window_x = max([tkFont.Font().measure(message1), tkFont.Font().measure(message2)])
        original_geometry = [window_x, 75]
        str_original_geometry = map(str, original_geometry)
        self.root.geometry('x'.join(str_original_geometry))
        self.root.title(message1)
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(fill='both', expand=True)
        for index in range(0, 3):
            self.main_frame.rowconfigure(index, weight=1)
        for index in range(0, 2):
            self.main_frame.columnconfigure(index, weight=1)
        sure_label = tk.Label(self.main_frame, text=message1)
        sure_label.grid(row=0, column=0, columnspan=2)
        another_label = tk.Label(self.main_frame, text=message2, fg='red')
        another_label.grid(row=1, column=0, columnspan=2)
        yes_button = tk.Button(self.main_frame, text='SI', command=self.delete_it)
        yes_button.grid(row=2, column=0)
        yes_button.config(width=10)
        no_button = tk.Button(self.main_frame, text='NO', command=self.dont_delete_it)
        no_button.grid(row=2, column=1)
        no_button.config(width=10)
        self.answer = False

    def delete_it(self):
        self.answer = True
        self.root.quit()

    def dont_delete_it(self):
        self.answer = False
        self.root.quit()


class TkSecureNone():
    def __init__(self):
        self.isalive = False


class TkSecure(tk.Tk):
    def __init__(self):
        super().__init__()
        self.isalive = True

    def destroy(self):
        super().destroy()
        self.isalive = False


if __name__ == '__main__':
    file_clients = 'clients.txt'
    file_alumns = 'alumnos.txt'
    file_groups = 'groups.txt'

    root = tk.Tk()
    myapp = GestionEspacioAbierto(root)

    root.mainloop()
