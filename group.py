class Group:
    str_header = ['Actividad', 'Monitor/a', 'Dias', 'Inicio', 'Final', 'Precio', 'Limite de Miembros', 'Miembros',
                  'ID Grupo']

    def __init__(self, name_activity = '', name_teacher = '', days = '', time_start = '', time_end = '', price = '', limit_members = '', members = '',
                 group_id = ''):
        self.name_activity = name_activity
        self.name_teacher = name_teacher
        self.days = eval(days)
        self.time_start = int(time_start)
        self.time_end = int(time_end)
        self.price = float(price)
        self.limit_members = int(limit_members)
        self.members = eval(members)  # set
        self.id = int(group_id)

    def __str__(self):
        ret_string = ';'.join(
            [self.name_activity, self.name_teacher, str(self.days), str(self.time_start), str(self.time_end),
             str(self.price), str(self.limit_members), str(self.members), str(self.id)])
        return ret_string


def available_id(elements_list):
    get_id = lambda element: element.id
    map_ids = map(get_id, elements_list)
    list_ids = list(map_ids)
    id = max(list_ids) + 1
    return id


def check_id_integrity(elements_list):
    get_id = lambda element: element.id
    map_ids = map(get_id, elements_list)
    list_ids = list(map_ids)
    if len(set(list_ids)) < len(list_ids):
        raise ValueError('IDs are not unique')
