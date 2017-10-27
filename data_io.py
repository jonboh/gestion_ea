import inspect
import group as gr


def load_clients(file_clients, client_type):
    with open(file_clients) as file:
        column_names = file.readline()
        client_list = [client_type(*line.rstrip('\n').split(';')) for line in file]
    return client_list


def write_clients(file_clients, clients_list, client_type):
    header = ';'.join(inspect.getfullargspec(client_type).args[1:])
    with open(file_clients, 'w') as file:
        file.write(header + '\n')
        file.write('\n'.join(map(str, clients_list)))


def load_groups(file_groups):
    with open(file_groups) as file:
        column_names = file.readline()
        groups_list = [gr.Group(*line.rstrip('\n').split(';')) for line in file]
    return groups_list


def write_groups(file_groups, groups_list):
    header = ';'.join(inspect.getfullargspec(gr.Group).args[1:])
    with open(file_groups, 'w') as file:
        file.write(header + '\n')
        file.write('\n'.join(map(str, groups_list)))
