class Client:
    def __init__(self, name: str, surname: str, id_card: str, phone1: str, phone2: str, phone3: str, email: str,
                 client_num: str):
        self.name = name
        self.surname = surname
        self.id_card = id_card
        self.phone1 = phone1
        self.phone2 = phone2
        self.phone3 = phone3
        self.email = email
        self.client_num = int(client_num)

    def __str__(self):
        ret_string = ';'.join(
            [self.name, self.surname, self.id_card, self.phone1, self.phone2, self.phone3, self.email, str(self.client_num)])
        return ret_string


class Alumn(Client):
    def __init__(self, name: str, surname: str, id_card: str, phone1: str, phone2: str, phone3: str, email: str,
                 client_num: str, pay_bank: str, bank_acc: str, pay_period: str, groups: str):
        super().__init__(name, surname, id_card, phone1, phone2, phone3, email, client_num)
        self.pay_bank = bool(eval(pay_bank))
        self.bank_acc = bank_acc
        self.pay_period = pay_period
        self.groups = eval(groups)  # set

    def __str__(self):
        ret_string = ';'.join([super().__str__(),str(self.pay_bank),self.bank_acc,self.pay_period,str(self.groups)])
        return ret_string


class Patient(Client):
    def __init__(self, ):
        super().__init__()

    def __str__(self):
        return


def check_integrity_clients_list(clients_list):
    get_id = lambda x : x.client_num
    map_ids = map(get_id, clients_list)
    if len(set(map_ids)) < len(list(map_ids)):
        raise ValueError('Clients IDs are not unique')
