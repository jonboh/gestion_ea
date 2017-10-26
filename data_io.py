import inspect


def load_clients(file_clients, client_type):
    with open(file_clients) as file:
        column_names = file.readline()
        client_list = [client_type(*line.rstrip('\n').split(';')) for line in file]
    return client_list


def write_clients(file_clients, clients_list, client_type):
    header = ';'.join(inspect.getfullargspec(client_type).args[1:])
    with open(file_clients, 'w') as file:
        file.write(header+'\n')
        file.write('\n'.join(map(str, clients_list)))


def load_groups(file_groups, group_type):
    pass


def write_groups(file_groups, groups_list, group_type):
    pass