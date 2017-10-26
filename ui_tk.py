import tkinter as tk
from pandastable import Table
import ctypes
import time
import threading as th

import data_io as io
import client as cl
import group as gr


class Gestion_EspacioAbierto:
    def __init__(self, root):
        self.root = root
        self.root.title('Gestion Espacio Abierto v0.1')
        self.root.geometry('800x600')
        self.root.protocol("WM_DELETE_WINDOW", self.close_program)
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
        welcome_buttons_frame = tk.Frame(self.welcome_frame, background='red')
        welcome_buttons_frame.grid(row=1, column=0, sticky=tk.S + tk.E)
        self.navigation_interface(welcome_buttons_frame)

        # CLIENTS LIST WINDOW
        self.clients_list_frame = tk.Frame(self.root, background='blue')
        self.clients_list_frame.grid_rowconfigure(0, weight=1)
        self.clients_list_frame.grid_columnconfigure(0, weight=1)
        self.clients_list_frame.grid(row=0, column=0, sticky=tk.N + tk.W + tk.E + tk.S)
        table_frame = tk.Frame(self.clients_list_frame,background='black')
        table_frame.grid(row=1,column=0, sticky=tk.N+tk.W)

        clients_list_buttons_frame = tk.Frame(self.clients_list_frame, background='red')
        clients_list_buttons_frame.grid(row=1, column=0, sticky=tk.S + tk.E)
        self.navigation_interface(clients_list_buttons_frame)

        # NEW CLIENT WINDOW

        # MODIFY CLIENT WINDOW



        # GROUPS WINDOW
        self.groups_list_frame = tk.Frame(self.root, background='yellow')
        self.groups_list_frame.grid_rowconfigure(0, weight=1)
        self.groups_list_frame.grid_columnconfigure(0, weight=1)
        self.groups_list_frame.grid(row=0, column=0, sticky=tk.N + tk.W + tk.E + tk.S)
        groups_list_buttons_frame = tk.Frame(self.groups_list_frame, background='red')
        groups_list_buttons_frame.grid(row=1, column=0, sticky=tk.S + tk.E)
        self.navigation_interface(groups_list_buttons_frame)

        self.loading_frame.tkraise()

        load_info_runner = th.Thread(target=self.load_info_start, name='Info Loader')
        load_info_runner.start()

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

    def load_info_start(self):
        self.loading_frame.tkraise()
        self.clients = io.load_clients(file_clients, cl.Client)
        # self.alumns = io.load_clients(file_alumns,cl.Alumn)
        # self.patients = io.load_clients(file_alumns,cl.Alumn)
        # self.groups = io.load_groups(file_groups, gr.Group)
        self.welcome_frame.tkraise()

    def loading_window(self):
        self.loading_frame.tkraise()

    def welcome_window(self):
        self.welcome_frame.tkraise()

    def clients_list_window(self):
        self.clients_list_frame.tkraise()

    # def client_window(self, client):

    # def new_client(self):

    # def modify_client_window(self,client):

    def groups_list_window(self):
        self.groups_list_frame.tkraise()

    # def group_window(self, group):

    # def new_group(self):

    # def modify_group_window(self,group):

    def save_all_info(self):
        io.write_clients(file_clients, self.clients, cl.Client)
        # io.write_clients(file_alumns, self.alumns, cl.Alumn)
        # io.write_clients(file_clients, self.patients, cl.Patient)
        # io.write_groups(file_groups, self.groups, gr.Group)

    def close_program(self):
        self.save_all_info()
        self.root.destroy()


if __name__ == '__main__':
    file_clients = 'clients.txt'
    file_alumns = 'alumnos.txt'
    file_patients = 'patients.txt'
    file_groups = 'groups.txt'

    root = tk.Tk()
    myapp = Gestion_EspacioAbierto(root)

    root.mainloop()
