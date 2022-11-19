import inspect
import os
import shutil
import datetime
import group as gr
import item as it
import client as cl


def load_clients(file_clients, client_type):
    with open(file_clients) as file:
        _ = file.readline()  # column_names
        client_list = [client_type(*line.rstrip('\n').split(';'))
                       for line in file]
    return client_list


def write_clients(file_clients, clients_list, client_type):
    header = ';'.join(inspect.getfullargspec(client_type).args[1:])
    with open(file_clients, 'w') as file:
        file.write(header + '\n')
        file.write('\n'.join(map(str, clients_list)))


def load_groups(file_groups):
    with open(file_groups) as file:
        _ = file.readline()  # column_names
        groups_list = [gr.Group(*line.rstrip('\n').split(';'))
                       for line in file]
    return groups_list


def write_groups(file_groups, groups_list):
    header = ';'.join(inspect.getfullargspec(gr.Group).args[1:])
    with open(file_groups, 'w') as file:
        file.write(header + '\n')
        file.write('\n'.join(map(str, groups_list)))


def load_items(file_items):
    with open(file_items) as file:
        _ = file.readline()  # column_names
        items_list = [it.Item(*line.rstrip('\n').split(';')) for line in file]
    return items_list


def write_items(file_items, items_list):
    header = ';'.join(inspect.getfullargspec(it.Item).args[1:])
    with open(file_items, 'w') as file:
        file.write(header + '\n')
        file.write('\n'.join(map(str, items_list)))


def write_export_clients(filename, objects, object_type, header_map):
    with open(filename, 'w') as file:
        # Join name and surname in a single column
        if header_map[0] == 1 and header_map[1] == 1:
            str_list = object_type().tree_header_map(header_map)
            str_list[0:2] = [' y '.join(str_list[0:2])]
            file.write(','.join(str_list) + '\n')
            for object_ in objects:
                str_list = list(map(str, object_.tree_entries(header_map)))
                str_list[0:2] = [' '.join(str_list[0:2])]
                file.write(','.join(str_list) + '\n')
        else:
            file.write(
                ','.join(object_type().tree_header_map(header_map)) + '\n')
            for object_ in objects:
                file.write(
                    ','.join(map(str, object_.tree_entries(header_map))) + '\n')


def write_export(filename, objects, object_type, header_map):
    with open(filename, 'w') as file:
        file.write(','.join(object_type().tree_header_map(header_map)) + '\n')
        for object_ in objects:
            file.write(
                ','.join(map(str, object_.tree_entries(header_map))) + '\n')


def is_last_backup_old(backup_dir, backup_freq):
    backups = next(os.walk(backup_dir))[1]  # generator
    backups_dates = list(map(dateparser, backups))
    backups_oldness = list(map(lambda element:
                               (datetime.date.today() -
                                element[0]).total_seconds() / 60 / 60 / 24,
                               backups_dates))
    if min(backups_oldness) > backup_freq:
        return True
    else:
        return False


def purge_old_backups(backup_dir, old_backup_dir, max_oldness):
    def move_old_dir(dir):
        shutil.move(backup_dir + '/' + dir, old_backup_dir + '/' + dir)

    backups = next(os.walk(backup_dir))[1]  # generator
    backups_dates = list(map(dateparser, backups))
    backups_oldness = list(map(lambda element:
                               (datetime.date.today() - element[0]).total_seconds() / 60 / 60 / 24, backups_dates))
    for i in range(0, len(backups)):
        if backups_oldness[i] > max_oldness:
            if backups_dates[i][1] is True:
                date = backups_dates[i][0]
                datestring = date2string(date.year, date.month, date.day)
                move_old_dir(datestring)


def make_backup(backup_dir, data_dir, file_clients, file_alumns, file_groups, file_items):
    clients = load_clients(file_clients, cl.Client)
    alumns = load_clients(file_alumns, cl.Alumn)
    groups = load_groups(file_groups)
    items = load_items(file_items)
    date = datetime.datetime.now()
    datestring = date2string(date.year, date.month, date.day)
    backup_dated_dir = backup_dir + '/' + datestring + '/'
    # file_whatever already includes the data_dir
    os.makedirs(backup_dated_dir + '/' + data_dir)
    write_clients(backup_dated_dir + file_clients, clients,
                  cl.Client)  # we have to include it
    write_clients(backup_dated_dir + file_alumns, alumns,
                  cl.Alumn)  # only to create the dir
    write_groups(backup_dated_dir + file_groups, groups)
    write_items(backup_dated_dir + file_items, items)


def dateparser(datestring):  # YYYYMMDD
    try:
        year = int(datestring) // 10000
        month = int(datestring) // 100 - year * 100
        day = int(datestring) - month * 100 - year * 10000
        date = datetime.date(year, month, day)
        return (date, True)
    except:
        return (datetime.date(1, 1, 1), False)


def date2string(year, month, day):
    yearstring = str(year)
    monthstring = str(month)
    daystring = str(day)
    if len(yearstring) < 4:
        yearstring = '0' * (4 - len(yearstring)) + yearstring
    if len(monthstring) < 2:
        monthstring = '0' + monthstring
    if len(daystring) < 2:
        daystring = '0' + daystring
    datestring = yearstring + monthstring + daystring
    return datestring
