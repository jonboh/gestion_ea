class Client:
    tree_header = ['Nombre', 'Apellidos', 'DNI', 'Tlf 1', 'Tlf 2', 'e-mail', 'ID Cliente']
    default_header_map = [1 for _ in tree_header]
    default_header_map[tree_header.index('ID Cliente')] = 0

    def __init__(self, name='', surname='', id_card='', phone1='', phone2='', email='',
                 client_id=''):
        self.name = name
        self.surname = surname
        self.id_card = id_card
        self.phone1 = phone1
        self.phone2 = phone2
        self.email = email
        if client_id is '':
            self.id = -1
        else:
            self.id = int(client_id)

    def tree_header_map(self, header_map):
        raw_entries_list = Client.tree_header
        entries_list = list()
        for entry, isincluded in zip(raw_entries_list, header_map[0:len(raw_entries_list)]):
            if isincluded:
                entries_list.append(entry)
        return entries_list

    def tree_entries(self, header_map=default_header_map):
        raw_entries_list = [self.name, self.surname, self.id_card, self.phone1, self.phone2, self.email, self.id]
        entries_list = list()
        for entry, isincluded in zip(raw_entries_list, header_map[0:len(raw_entries_list)]):
            if isincluded:
                entries_list.append(entry)
        return entries_list

    def __str__(self):
        ret_string = ';'.join(
            [self.name, self.surname, self.id_card, self.phone1, self.phone2, self.email,
             str(self.id)])
        return ret_string


class Alumn(Client):
    alumn_extra =['Alta/Baja', 'Domicilia', 'Cuenta Bancaria', 'Fecha Mandato', 'Periodo Pago', 'Grupos']
    tree_header = Client.tree_header + alumn_extra
    default_header_map = Client.default_header_map + [1 for _ in alumn_extra]

    def __init__(self, name='', surname='', id_card='', phone1='', phone2='', email='',
                 client_id='', active='0', pay_bank='0', bank_acc='', date_sent='', pay_period='0', groups='{}'):
        super().__init__(name, surname, id_card, phone1, phone2, email, client_id)
        self.active = int(active)
        self.pay_bank = bool(eval(pay_bank))
        self.bank_acc = bank_acc
        self.date_sent = date_sent
        self.pay_period = int(pay_period)
        if type(eval(groups)) is dict:
            self.groups = set()
        else:
            self.groups = eval(groups)  # set

    def tree_header_map(self, header_map):
        raw_entries_list = ['Alta/Baja', 'Domicilia', 'Cuenta Bancaria', 'Fecha Mandato', 'Periodo Pago', 'Grupos']
        entries_list = super().tree_header_map(header_map)
        for entry, isincluded in zip(raw_entries_list, header_map[len(Client.tree_header):]):
            if isincluded:
                entries_list.append(entry)
        return entries_list

    def tree_entries(self, header_map=default_header_map):
        if self.active is 1:
            active = 'Alta'
        else:
            active = 'Baja'
        if self.pay_bank:
            pay_bank = 'Si'
        else:
            pay_bank = 'No'
        if self.pay_period is 0:
            pay_period = 'Mensual'
        elif self.pay_period is 1:
            pay_period = 'Trimensual'
        elif self.pay_period is 2:
            pay_period = 'Anual'
        else:
            pay_period = 'Desconocido'
        groups = self.groups
        if len(self.groups) == 0:
            groups = '{}'
        raw_entries_list = [active, pay_bank, self.bank_acc, self.date_sent, pay_period, groups]
        entries_list = super().tree_entries(header_map)
        for entry, isincluded in zip(raw_entries_list, header_map[len(Client.tree_header):]):
            if isincluded:
                entries_list.append(entry)
        return entries_list

    def __str__(self):
        ret_string = ';'.join(
            [super().__str__(), str(self.active), str(self.pay_bank), self.bank_acc, self.date_sent,str(self.pay_period),
             str(self.groups)])
        return ret_string


def cast_client_alumn(client):
    alumn = Alumn()
    alumn.name = client.name
    alumn.surname = client.surname
    alumn.id_card = client.id_card
    alumn.phone1 = client.phone1
    alumn.phone2 = client.phone2
    alumn.email = client.email
    alumn.id = client.id
    return alumn


def cast_alumn_client(alumn):
    client = Client()
    client.name = alumn.name
    client.surname = alumn.surname
    client.id_card = alumn.id_card
    client.phone1 = alumn.phone1
    client.phone2 = alumn.phone2
    client.email = alumn.email
    client.id = alumn.id
    return client
