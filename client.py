class Client:
    str_header = ['Nombre', 'Apellidos', 'DNI', 'Tlf 1', 'Tlf 2', 'e-mail', 'ID Cliente']

    def __init__(self, name = '', surname = '', id_card = '', phone1 = '', phone2 = '', email = '',
                 client_id = ''):
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

    def entries(self):
        entries_list = [self.name, self.surname, self.id_card, self.phone1,self.phone2,self.email, self.id]
        return entries_list

    def __str__(self):
        ret_string = ';'.join(
            [self.name, self.surname, self.id_card, self.phone1, self.phone2, self.email,
             str(self.id)])
        return ret_string


class Alumn(Client):
    str_header = Client.str_header + ['Domicilia', 'Cuenta Bancaria', 'Periodo Pago', 'Grupos']

    def __init__(self, name='', surname='', id_card='', phone1='', phone2='', email='',
                 client_id='', pay_bank='0', bank_acc='', pay_period='0', groups='{}'):
        super().__init__(name, surname, id_card, phone1, phone2, email, client_id)
        self.pay_bank = bool(eval(pay_bank))
        self.bank_acc = bank_acc
        self.pay_period = int(pay_period)
        if type(eval(groups)) is dict:
            self.groups = set()
        else:
            self.groups = eval(groups)  # set

    def entries(self):
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
        entries_list = super().entries() + [pay_bank, self.bank_acc, pay_period, self.groups]
        return entries_list

    def __str__(self):
        ret_string = ';'.join([super().__str__(), str(self.pay_bank), self.bank_acc, str(self.pay_period), str(self.groups)])
        return ret_string