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
        self.clients_listbox = tk.Listbox(clients_table_frame, width=int(original_geometry[0] * 0.1),
                                          height=int(original_geometry[1] * 0.05))
        self.clients_listbox.grid(row=1, column=0, columnspan=3, sticky=tk.N + tk.W)
        self.clients_listbox.bind('<Double-Button-1>', self.client_window)
        clients_list_buttons_frame = tk.Frame(self.clients_list_frame)
        clients_list_buttons_frame.grid(row=0, column=0, sticky=tk.N + tk.E)
        self.list_buttons(clients_list_buttons_frame, cl.Client)
        clients_list_nav_frame = tk.Frame(self.clients_list_frame, background='red')
        clients_list_nav_frame.grid(row=1, column=0, sticky=tk.S + tk.E)
        self.navigation_interface(clients_list_nav_frame)

        # GROUPS WINDOW
        self.groups_list_frame = tk.Frame(self.root, background='yellow')
        self.groups_list_frame.grid_rowconfigure(0, weight=1)
        self.groups_list_frame.grid_columnconfigure(0, weight=1)
        self.groups_list_frame.grid(row=0, column=0, sticky=tk.N + tk.W + tk.E + tk.S)
        groups_table_frame = tk.Frame(self.groups_list_frame, background='black')
        groups_table_frame.grid(row=0, column=0, sticky=tk.N + tk.W + tk.E + tk.S)
        groups_table_label = tk.Label(groups_table_frame, text='Grupos: ', font=("Helvetica", 14))
        groups_table_label.grid(row=0, column=0, sticky=tk.N + tk.W)
        groups_list_buttons_frame = tk.Frame(self.groups_list_frame)
        groups_list_buttons_frame.grid(row=0, column=0, sticky=tk.N + tk.E)
        self.list_buttons(groups_list_buttons_frame, gr.Group)
        self.groups_listbox = tk.Listbox(groups_table_frame)
        self.groups_listbox.grid()
        self.groups_listbox.bind('<Double-Button-1>', self.group_window)

        groups_list_nav_frame = tk.Frame(self.groups_list_frame, background='red')
        groups_list_nav_frame.grid(row=1, column=0, sticky=tk.S + tk.E)
        self.navigation_interface(groups_list_nav_frame)

        # LOAD CLIENTS AND GROUPS
        self.loading_frame.tkraise()
        self.clients = io.load_clients(file_clients, cl.Client)
        self.alumns = io.load_clients(file_alumns, cl.Alumn)
        self.groups = io.load_groups(file_groups)
        self.welcome_frame.tkraise()

        # UPDATE CLIENTS AND GROUPS LISTBOXES
        self.clients_listbox_update()
        self.groups_listbox_update()

    def list_buttons(self, parent_frame, type):
        if type is cl.Client:
            new_button = tk.Button(parent_frame, text='Nuevo', command=self.new_client)
            new_button.grid(row=0, column=0, sticky=tk.N + tk.E, padx=(10, 10), pady=(100, 10))
            modify_button = tk.Button(parent_frame, text='Modificar', command=self.modify_client)
            modify_button.grid(row=1, column=0, sticky=tk.E, padx=(10, 10), pady=(0, 10))
            export_button = tk.Button(parent_frame, text='Exportar', command=self.export_selection)
            export_button.grid(row=2, column=0, sticky=tk.N + tk.E, padx=(10, 10), pady=(0, 10))
        elif type is gr.Group:
            new_button = tk.Button(parent_frame, text='Nuevo', command=self.new_group)
            new_button.grid(row=0, column=0, sticky=tk.N + tk.E, padx=(10, 10), pady=(100, 10))
            modify_button = tk.Button(parent_frame, text='Modificar', command=self.modify_group)
            modify_button.grid(row=1, column=0, sticky=tk.N + tk.E, padx=(10, 10), pady=(0, 10))
            export_button = tk.Button(parent_frame, text='Exportar', command=self.export_selection)
            export_button.grid(row=2, column=0, sticky=tk.N + tk.E, padx=(10, 10), pady=(0, 10))
        else:
            new_button = tk.Button(parent_frame, text='Nuevo')
            new_button.grid(row=0, column=0, sticky=tk.N + tk.E, padx=(10, 10), pady=(100, 10))
            modify_button = tk.Button(parent_frame, text='Modificar')
            modify_button.grid(row=1, column=0, sticky=tk.N + tk.E, padx=(10, 10), pady=(0, 10))
            export_button = tk.Button(parent_frame, text='Exportar')
            export_button.grid(row=2, column=0, sticky=tk.N + tk.E, padx=(10, 10), pady=(0, 10))
        new_button.config(width=20)
        modify_button.config(width=20)
        export_button.config(width=20)

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
        """invoker: 'Clients' or 'Alumns'"""
        if invoker is 'Clients':
            self.cl_chbox_var.set(1)
            self.al_chbox_var.set(0)
            self.clients_listbox_update()
        if invoker is 'Alumns':
            self.cl_chbox_var.set(0)
            self.al_chbox_var.set(1)
            self.clients_listbox_update()

    def clients_listbox_update(self, ):
        self.clients_listbox.delete(0, tk.END)
        self.clients_listbox_obj = list()
        if self.cl_chbox_var.get() is 1:
            # header = format_clients()
            header = ' '.join(cl.Client.str_header)
            self.clients_listbox.insert(tk.END, header)
            for client in self.clients:
                # entry = format_clients()
                self.clients_listbox_obj.append(client)
                entry = ' '.join(str(client).split(';'))
                self.clients_listbox.insert(tk.END, entry)
        if self.al_chbox_var.get() is 1:
            # header = format_clients()
            header = ' '.join(cl.Alumn.str_header)
            self.clients_listbox.insert(tk.END, header)
            for client in self.alumns:
                # entry = format_clients()
                self.clients_listbox_obj.append(client)
                entry = ' '.join(str(client).split(';'))
                self.clients_listbox.insert(tk.END, entry)
                # if self.pa_chbox_var.get() is 1:
                #     # header = format_clients()
                #     header = ' '.join(cl.Patient.str_header)
                #     self.clients_listbox.insert(tk.END, header)
                #     for client in self.patients:
                #         # entry = format_clients()
                #         self.clients_listbox_obj.append(client)
                #         entry = ' '.join(str(client).split(';'))
                #         self.clients_listbox.insert(tk.END, entry)

    def groups_listbox_update(self):
        self.groups_listbox.delete(0, tk.END)
        self.groups_listbox_obj = list()
        # header = format_groups()
        header = ' '.join(gr.Group.str_header)
        self.groups_listbox.insert(tk.END, header)
        for group in self.groups:
            # entry = format_clients()
            self.groups_listbox_obj.append(group)
            entry = ' '.join(str(group).split(';'))
            self.groups_listbox.insert(tk.END, entry)

    def client_window(self, event):
        selected_index = self.clients_listbox.curselection()[0] - 1  # -1 discounts the header
        if not selected_index is -1:
            client = self.clients_listbox_obj[selected_index]
            popup_root = tk.Tk()
            popup = ClientUI(popup_root, client)
            popup_root.mainloop()

    def new_client(self):
        id_new_element = gr.available_id(self.clients + self.alumns)
        popup_root = tk.Tk()
        if self.cl_chbox_var.get() is 1:
            popup = ModifyClientUI(popup_root, cl.Client(), id_new_element)
        else:
            popup = ModifyClientUI(popup_root, cl.Alumn(), id_new_element)
        popup_root.mainloop()
        if type(popup.client) is cl.Client:
            self.clients.append(popup.client)
        if type(popup.client) is cl.Alumn:
            self.alumns.append(popup.client)

    def modify_client(self):
        selected_index = self.clients_listbox.curselection()[0] - 1
        client = self.clients_listbox_obj[selected_index]
        popup_root = tk.Tk()
        popup = ModifyClientUI(popup_root, client)
        popup_root.mainloop()
        popup_root.destroy()
        if type(client) is cl.Client:
            self.clients.remove(client)
            self.clients.append(popup.client)
        elif type(client) is cl.Alumn:
            self.alumns.remove(client)
            self.alumns.append(popup.client)

    def groups_list_window(self):
        self.groups_list_frame.tkraise()

    def group_window(self, event):
        selected_index = self.groups_listbox.curselection()[0] - 1
        if not selected_index is -1:
            group = self.groups_listbox_obj[selected_index]
            popup_root = tk.Tk()
            popup = GroupUI(popup_root, group)
            popup_root.mainloop()

    def new_group(self):
        id_new_element = gr.available_id(self.groups)
        popup_root = tk.Tk()
        popup = ModifyGroupUI(popup_root, gr.Group(), id_new_element)
        popup_root.mainloop()
        self.groups.append(popup.group)

    def modify_group(self):
        selected_index = self.groups_listbox.curselection()
        group = self.groups_listbox.get(selected_index)
        popup_root = tk.Tk()
        popup = ModifyGroupUI(popup_root, group)
        popup_root.mainloop()
        self.groups.remove(group)
        self.groups.append(popup.group)

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
    def __init__(self, popup_root, client):
        self.popup_root = popup_root
        self.popup_root.title('Cliente: ' + client.name + ' ' + client.surname)
        original_geometry = [200, 150]
        str_original_geometry = map(str, original_geometry)
        self.popup_root.geometry('x'.join(str_original_geometry))
        self.popup_root.protocol("WM_DELETE_WINDOW", self.close_window)
        self.client = client

        # FIELDS
        name_field = tk.Label(self.popup_root, text='Nombre: ')
        name_field.grid(row=0, column=0, sticky=tk.N + tk.W)
        surname_field = tk.Label(self.popup_root, text='Apellidos: ')
        surname_field.grid(row=1, column=0, sticky=tk.N + tk.W)
        id_card_field = tk.Label(self.popup_root, text='DNI: ')
        id_card_field.grid(row=2, column=0, sticky=tk.N + tk.W)
        phone1_field = tk.Label(self.popup_root, text='Tlf 1: ')
        phone1_field.grid(row=3, column=0, sticky=tk.N + tk.W)
        phone2_field = tk.Label(self.popup_root, text='Tlf 2:')
        phone2_field.grid(row=4, column=0, sticky=tk.N + tk.W)
        email_field = tk.Label(self.popup_root, text='E-mail: ')
        email_field.grid(row=5, column=0, sticky=tk.N + tk.W)
        client_id_field = tk.Label(self.popup_root, text='ID Cliente: ')
        client_id_field.grid(row=6, column=0, sticky=tk.N + tk.W)

        # FIELD VALUES
        name_ans = tk.Label(self.popup_root, text=self.client.name)
        name_ans.grid(row=0, column=1, sticky=tk.N + tk.W)
        surname_ans = tk.Label(self.popup_root, text=self.client.surname)
        surname_ans.grid(row=1, column=1, sticky=tk.N + tk.W)
        id_card_ans = tk.Label(self.popup_root, text=self.client.id_card)
        id_card_ans.grid(row=2, column=1, sticky=tk.N + tk.W)
        phone1_ans = tk.Label(self.popup_root, text=self.client.phone1)
        phone1_ans.grid(row=3, column=1, sticky=tk.N + tk.W)
        phone2_ans = tk.Label(self.popup_root, text=self.client.phone2)
        phone2_ans.grid(row=4, column=1, sticky=tk.N + tk.W)
        email_ans = tk.Label(self.popup_root, text=self.client.email)
        email_ans.grid(row=5, column=1, sticky=tk.N + tk.W)
        client_id_ans = tk.Label(self.popup_root, text=self.client.id)
        client_id_ans.grid(row=6, column=1, sticky=tk.N + tk.W)

        if type(client) is cl.Alumn:
            self.popup_root.title('Cliente: ' + client.name + ' ' + client.surname)
            original_geometry = [200, 220]
            str_original_geometry = map(str, original_geometry)
            self.popup_root.geometry('x'.join(str_original_geometry))
            # FIELDS
            pay_bank_field = tk.Label(self.popup_root, text='Domicilia?:')
            pay_bank_field.grid(row=8, column=0, sticky=tk.N + tk.W)
            bank_acc_field = tk.Label(self.popup_root, text='IBAN:')
            bank_acc_field.grid(row=9, column=0, sticky=tk.N + tk.W)
            pay_period_field = tk.Label(self.popup_root, text='Tipo Pago:')
            pay_period_field.grid(row=10, column=0, sticky=tk.N + tk.W)

            # FIELD VALUES
            if client.pay_bank is True:
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
            pay_bank_ans = tk.Label(self.popup_root, text=pay_bank)
            pay_bank_ans.grid(row=8, column=1, sticky=tk.N + tk.W)
            bank_acc_ans = tk.Label(self.popup_root, text=client.bank_acc)
            bank_acc_ans.grid(row=9, column=1, sticky=tk.N + tk.W)
            pay_period_ans = tk.Label(self.popup_root, text=pay_period)
            pay_period_ans.grid(row=10, column=1, sticky=tk.N + tk.W)

    def close_window(self):
        self.popup_root.quit()


class ModifyClientUI(ClientUI):
    def __init__(self, popup_root, client, id=None):
        super().__init__(popup_root, client)
        if client.name is '':
            self.popup_root.title('Nuevo Cliente')
        original_geometry = [300, 300]
        str_original_geometry = map(str, original_geometry)
        self.popup_root.geometry('x'.join(str_original_geometry))
        self.client = client
        # NEW FIELD VALUES
        name_new = tk.Entry(self.popup_root, text=self.client.name)
        name_new.grid(row=0, column=2, sticky=tk.N + tk.W)
        surname_new = tk.Entry(self.popup_root, text=self.client.surname)
        surname_new.grid(row=1, column=2, sticky=tk.N + tk.W)
        id_card_new = tk.Entry(self.popup_root, text=self.client.id_card)
        id_card_new.grid(row=2, column=2, sticky=tk.N + tk.W)
        phone1_new = tk.Entry(self.popup_root, text=self.client.phone1)
        phone1_new.grid(row=3, column=2, sticky=tk.N + tk.W)
        phone2_new = tk.Entry(self.popup_root, text=self.client.phone2)
        phone2_new.grid(row=4, column=2, sticky=tk.N + tk.W)
        email_new = tk.Entry(self.popup_root, text=self.client.email)
        email_new.grid(row=5, column=2, sticky=tk.N + tk.W)
        client_id_ans = tk.Label(self.popup_root, text=id)
        client_id_ans.grid(row=6, column=2, sticky=tk.N + tk.W)

        if type(client) is cl.Alumn:
            pay_bank_ans = tk.Checkbutton(self.popup_root)
            pay_bank_ans.grid(row=8, column=2, sticky=tk.N + tk.W)
            bank_acc_ans = tk.Entry(self.popup_root)
            bank_acc_ans.grid(row=9, column=2, sticky=tk.N + tk.W)
            pay_period_miniframe = tk.Frame(self.popup_root)
            pay_period_miniframe.grid(row=10, column=2, sticky=tk.N + tk.W)
            month_label = tk.Label(pay_period_miniframe, text='Mensual: ')
            month_label.grid(row=0, column=1, sticky=tk.N + tk.E)
            month_checkbox = tk.Checkbutton(pay_period_miniframe)
            month_checkbox.grid(row=0, column=2, sticky=tk.N + tk.E)
            trimonth_label = tk.Label(pay_period_miniframe, text='Trimestral:')
            trimonth_label.grid(row=1, column=1, sticky=tk.N + tk.E)
            trimonth_checkbox = tk.Checkbutton(pay_period_miniframe)
            trimonth_checkbox.grid(row=1, column=2, sticky=tk.N + tk.E)
            yearly_label = tk.Label(pay_period_miniframe, text='Anual: ')
            yearly_label.grid(row=2, column=1, sticky=tk.N + tk.E)
            yearly_checkbox = tk.Checkbutton(pay_period_miniframe)
            yearly_checkbox.grid(row=2, column=2, sticky=tk.N + tk.E)

        save_button = tk.Button(self.popup_root, text='Guardar', command=self.check_save)
        save_button.grid(row=20, column=0, columnspan=5, sticky=tk.S)

    def check_save(self):
        pass


class GroupUI:
    def __init__(self, root, group):
        self.root = root
        self.root.title('Grupo: ' + group.name_activity + ' ' + group.name_teacher + ' ' + str(group.days) + ' '
                        + str(group.time_start))
        original_geometry = [650, 500]
        str_original_geometry = map(str, original_geometry)
        self.root.geometry('x'.join(str_original_geometry))

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
        name_activity_ans = tk.Label(self.root, text=group.name_activity)
        name_activity_ans.grid(row=0, column=1, sticky=tk.N + tk.W)
        name_teacher_ans = tk.Label(self.root, text=group.name_teacher)
        name_teacher_ans.grid(row=1, column=1, sticky=tk.N + tk.W)
        days_ans = tk.Label(self.root, text=group.days_format())
        days_ans.grid(row=2, column=1, sticky=tk.N + tk.W)
        time_ans = tk.Label(self.root, text=group.timetable_format())
        time_ans.grid(row=3, column=1, sticky=tk.N + tk.W)
        price_ans = tk.Label(self.root, text=str(group.price) + ' EUR')
        price_ans.grid(row=4, column=1, sticky=tk.N + tk.W)
        members_number_ans = tk.Label(self.root, text=str(len(group.members)))
        members_number_ans.grid(row=5, column=1, sticky=tk.N + tk.W)
        members_limit_ans = tk.Label(self.root, text=str(group.limit_members))
        members_limit_ans.grid(row=6, column=1, sticky=tk.N + tk.W)
        group_id_ans = tk.Label(self.root, text=str(group.id))
        group_id_ans.grid(row=7, column=1, sticky=tk.N + tk.W)


class ModifyGroupUI(GroupUI):
    def __init__(self, root, group, id=None):
        super().__init__(root, group)
        self.group = group


if __name__ == '__main__':
    file_clients = 'clients.txt'
    file_alumns = 'alumnos.txt'
    file_groups = 'groups.txt'

    root = tk.Tk()
    myapp = GestionEspacioAbierto(root)

    root.mainloop()
