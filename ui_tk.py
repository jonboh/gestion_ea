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

        # MAIN WINDOW DECLARATION
        self.welcome_frame = tk.Frame(self.root, background='yellow')
        self.welcome_frame.grid_rowconfigure(0, weight=1)
        self.welcome_frame.grid_columnconfigure(0, weight=1)
        self.welcome_frame.grid(row=0, column=0, sticky=tk.N + tk.W + tk.E + tk.S)
        welcome_label = tk.Label(self.welcome_frame, background='white', text='Bienvenido, hora de trabajar',
                                 font=("Helvetica", 24))
        welcome_label.grid(row=0, column=0, sticky=tk.N + tk.W, padx=(100, 0), pady=(80, 0))

        welcome_clients_button = tk.Button(self.welcome_frame, command=self.clients_list_window, text='Clientes')
        welcome_clients_button.grid(row=1, column=0, sticky=tk.N + tk.W, padx=(50, 50), pady=(50, 50))
        # welcome_alumns_button =
        # welcome_patients_button =
        # welcome_groups_button =

        self.clients_list_frame = tk.Frame(self.root, background='blue')
        self.clients_list_frame.grid_rowconfigure(0, weight=1)
        self.clients_list_frame.grid_columnconfigure(0, weight=1)
        self.clients_list_frame.grid(row=0, column=0, sticky=tk.N + tk.W + tk.E + tk.S)
        # clients_list_stvar = tk.StringVar()
        # clients_list_stvar.set('Object1 Object2')
        # clients_list_listbox = tk.Listbox(self.clients_list_frame, listvariable=clients_list_stvar)
        # clients_list_listbox.grid(row=1, column=0, sticky=tk.N + tk.W)
        clients_list_table = Table(self.clients_list_frame)
        clients_list_table.show()

        self.loading_frame.tkraise()

        load_info_runner = th.Thread(target=self.load_info_start, name='Info Loader')
        load_info_runner.start()

    def load_info_start(self):
        self.loading_frame.tkraise()
        self.clients = io.load_clients(file_clients, cl.Client)
        # self.alumns = io.load_clients(file_alumns,cl.Alumn)
        # self.patients = io.load_clients(file_alumns,cl.Alumn)
        # self.groups = io.load_groups(file_groups, gr.Group)
        self.welcome_frame.tkraise()

    def loading_window(self):
        self.loading_frame.tkraise()

    def clients_list_window(self):
        self.clients_list_frame.tkraise()

    # def client_window(self, client):

    # def new_client(self):

    # def modify_client_window(self,client):

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
