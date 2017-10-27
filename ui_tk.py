import tkinter as tk
from pandastable import Table
import ctypes
import time
import threading as th

import data_io as io
import client as cl
import group as gr


class GestionEspacioAbierto:
    def __init__(self, root):
        self.root = root
        self.root.title('Gestion Espacio Abierto v0.1')
        original_geometry = [800, 600]
        str_original_geometry = map(str, original_geometry)
        self.root.geometry('x'.join(str_original_geometry))
        self.root.protocol("WM_DELETE_WINDOW", self.close_program)
        self.root.bind('<Configure>', self.resize_window)
        self.root.rowconfigure(0, weight=1)
        self.root.columnconfigure(0, weight=1)

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

        # CLIENTS LIST WINDOW
        self.clients_list_frame = tk.Frame(self.root, background='blue')
        self.clients_list_frame.grid_rowconfigure(0, weight=1)
        self.clients_list_frame.grid_columnconfigure(0, weight=1)
        self.clients_list_frame.grid(row=0, column=0, sticky=tk.N + tk.W + tk.E + tk.S)
        clients_table_frame = tk.Frame(self.clients_list_frame, background='black')
        clients_table_frame.grid(row=0, column=0, sticky=tk.N + tk.W + tk.E + tk.S)
        clients_table_label = tk.Label(clients_table_frame, text='Clientes: ', font=("Helvetica", 14))
        clients_table_label.grid(row=0, column=0, sticky=tk.N + tk.W)
        self.cl_chbox_var = tk.IntVar()
        self.cl_chbox_var.set(1)
        self.clients_checkbox = tk.Checkbutton(clients_table_frame, text='Clientes', font=("Helvetica", 10),
                                               variable=self.cl_chbox_var,
                                               command=lambda: self.clients_checkbox_update('Clients'))
        self.clients_checkbox.grid(row=0, column=1, sticky=tk.N + tk.E)
        self.al_chbox_var = tk.IntVar()
        self.al_chbox_var.set(0)
        self.alumns_checkbox = tk.Checkbutton(clients_table_frame, text='Alumnos', font=("Helvetica", 10),
                                              variable=self.al_chbox_var,
                                               command=lambda: self.clients_checkbox_update('Alumns'))
        self.alumns_checkbox.grid(row=0, column=2, sticky=tk.N + tk.E)
        self.pa_chbox_var = tk.IntVar()
        self.pa_chbox_var.set(0)
        self.patients_checkbox = tk.Checkbutton(clients_table_frame, text='Pacientes', font=("Helvetica", 10),
                                                variable=self.pa_chbox_var,
                                               command=lambda: self.clients_checkbox_update('Patients'))
        self.patients_checkbox.grid(row=0, column=3, sticky=tk.N + tk.E)
        self.clients_listbox = tk.Listbox(clients_table_frame, width=int(original_geometry[0] * 0.1),
                                          height=int(original_geometry[1] * 0.05))
        self.clients_listbox.grid(row=1, column=0, sticky=tk.N + tk.W)
        clients_list_nav_frame = tk.Frame(self.clients_list_frame, background='red')
        clients_list_nav_frame.grid(row=1, column=0, sticky=tk.S + tk.E)

        self.navigation_interface(clients_list_nav_frame)

        # GROUPS WINDOW
        self.groups_list_frame = tk.Frame(self.root, background='yellow')
        self.groups_list_frame.grid_rowconfigure(0, weight=1)
        self.groups_list_frame.grid_columnconfigure(0, weight=1)
        self.groups_list_frame.grid(row=0, column=0, sticky=tk.N + tk.W + tk.E + tk.S)
        groups_list_nav_frame = tk.Frame(self.groups_list_frame, background='red')
        groups_list_nav_frame.grid(row=1, column=0, sticky=tk.S + tk.E)
        groups_table_frame = tk.Frame(self.groups_list_frame, background='black')
        groups_table_frame.grid(row=0, column=0, sticky=tk.N + tk.W + tk.E + tk.S)
        groups_table_label = tk.Label(groups_table_frame, text='Grupos: ', font=("Helvetica", 14))
        groups_table_label.grid(row=0, column=0, sticky=tk.N + tk.W)
        self.groups_listbox = tk.Listbox(groups_table_frame)
        self.groups_listbox.grid()
        self.navigation_interface(groups_list_nav_frame)

        # LOAD CLIENTS AND GROUPS
        self.loading_frame.tkraise()
        self.clients = io.load_clients(file_clients, cl.Client)
        self.alumns = io.load_clients(file_alumns, cl.Alumn)
        # self.patients = io.load_clients(file_patients, cl.Patient)
        self.groups = io.load_groups(file_groups)
        self.welcome_frame.tkraise()

        # UPDATE CLIENTS AND GROUPS LISTBOXES
        self.clients_listbox_update()
        self.groups_listbox_update()

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

    def resize_window(self, event):
        if event.widget is self.root:
            w = event.width
            h = event.height
            self.clients_listbox.config(width=int(w * 0.1), height=int(h * 0.05))
            self.groups_listbox.config(width=int(w * 0.1), height=int(h * 0.05))

    def loading_window(self):
        self.loading_frame.tkraise()

    def welcome_window(self):
        self.welcome_frame.tkraise()

    def clients_list_window(self):
        self.clients_list_frame.tkraise()

    def clients_checkbox_update(self, invoker):
        """invoker: 'Clients' or 'Alumns' or 'Patients'"""
        if invoker is 'Clients':
            self.cl_chbox_var.set(1)
            self.al_chbox_var.set(0)
            self.pa_chbox_var.set(0)
            self.clients_listbox_update()
        if invoker is 'Alumns':
            self.cl_chbox_var.set(0)
            self.al_chbox_var.set(1)
            self.pa_chbox_var.set(0)
            self.clients_listbox_update()
        if invoker is 'Patients':
            self.cl_chbox_var.set(0)
            self.al_chbox_var.set(0)
            self.pa_chbox_var.set(1)
            self.clients_listbox_update()

    def clients_listbox_update(self,):
        self.clients_listbox.delete(0, tk.END)
        if self.cl_chbox_var.get() is 1:
            # header = format_clients()
            header = ' '.join(cl.Client.str_header)
            self.clients_listbox.insert(tk.END, header)
            for client in self.clients:
                # entry = format_clients()
                entry = ' '.join(str(client).split(';'))
                self.clients_listbox.insert(tk.END, entry)
        if self.al_chbox_var.get() is 1:
            # header = format_clients()
            header = ' '.join(cl.Alumn.str_header)
            self.clients_listbox.insert(tk.END, header)
            for client in self.alumns:
                # entry = format_clients()
                entry = ' '.join(str(client).split(';'))
                self.clients_listbox.insert(tk.END, entry)
        # if self.pa_chbox_var.get() is 1:
        #     # header = format_clients()
        #     header = ' '.join(cl.Patient.str_header)
        #     self.clients_listbox.insert(tk.END, header)
        #     for client in self.patients:
        #         # entry = format_clients()
        #         entry = ' '.join(str(client).split(';'))
        #         self.clients_listbox.insert(tk.END, entry)

    def groups_listbox_update(self):
        self.groups_listbox.delete(0, tk.END)
        # header = format_groups()
        header = ' '.join(gr.Group.str_header)
        self.groups_listbox.insert(tk.END, header)
        for group in self.groups:
            # entry = format_clients()
            entry = ' '.join(str(group).split(';'))
            self.groups_listbox.insert(tk.END, entry)

    # def client_window(self, client):

    def new_client(self):
        popup = NewClientUI(tk.Tk())
        self.clients.append(popup.client)

    def modify_client(self, client):
        self.clients.remove(client)
        popup = ModifyClientUI(tk.Tk(), client)
        self.clients.append(popup.client)

    def groups_list_window(self):
        self.groups_list_frame.tkraise()

    # def group_window(self, group):

    def new_group(self):
        popup = NewGroupUI(tk.Tk())
        self.groups.append(popup.group)

    def modify_group_window(self, group):
        self.groups.remove(group)
        popup = ModifyGroupUI(tk.Tk(), group)
        self.groups.append(popup.group)

    def save_all_info(self):
        io.write_clients(file_clients, self.clients, cl.Client)
        io.write_clients(file_alumns, self.alumns, cl.Alumn)
        # io.write_clients(file_clients, self.patients, cl.Patient)
        io.write_groups(file_groups, self.groups)

    def close_program(self):
        self.save_all_info()
        self.root.destroy()


class NewClientUI:
    def __init__(self, root):
        self.client = cl.Client()


class ModifyClientUI(NewClientUI):
    def __init__(self, root, client):
        super().__init__(root)
        self.client = client


class NewGroupUI:
    def __init__(self, root):
        self.group = gr.Group()


class ModifyGroupUI(NewGroupUI):
    def __init__(self, root, group):
        super().__init__(root)
        self.group = group


if __name__ == '__main__':
    file_clients = 'clients.txt'
    file_alumns = 'alumnos.txt'
    file_patients = 'patients.txt'
    file_groups = 'groups.txt'

    root = tk.Tk()
    myapp = GestionEspacioAbierto(root)

    root.mainloop()
