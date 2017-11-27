import inspect
import group as gr
import item as it


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


def load_items(file_items):
    with open(file_items) as file:
        column_names = file.readline()
        items_list = [it.Item(*line.rstrip('\n').split(';')) for line in file]
    return items_list


def write_items(file_items, items_list):
    header = ';'.join(inspect.getfullargspec(it.Item).args[1:])
    with open(file_items, 'w') as file:
        file.write(header + '\n')
        file.write('\n'.join(map(str, items_list)))


def write_export(filename, objects, object_type, header_map):
    with open(filename, 'w') as file:
        file.write(','.join(object_type().tree_header_map(header_map)) + '\n')
        for object_ in objects:
            file.write(','.join(map(str, object_.tree_entries(header_map))) + '\n')
