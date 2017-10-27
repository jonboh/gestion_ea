class Group:
    str_header = ['Actividad', 'Monitor/a', 'Dias', 'Inicio', 'Final', 'Precio', 'Limite de Miembros', 'Miembros',
                  'ID Grupo']

    def __init__(self, name_activity, name_teacher, days, time_start, time_end, price, limit_members, members,
                 group_id):
        self.name_activity = name_activity
        self.name_teacher = name_teacher
        self.days = eval(days)
        self.time_start = int(time_start)
        self.time_end = int(time_end)
        self.price = float(price)
        self.limit_members = int(limit_members)
        self.members = eval(members)  # set
        self.group_id = int(group_id)

    def __str__(self):
        ret_string = ';'.join(
            [self.name_activity, self.name_teacher, str(self.days), str(self.time_start), str(self.time_end),
             str(self.price), str(self.limit_members), str(self.members), str(self.group_id)])
        return ret_string


def check_integrity_groups_list(groups_list):
    get_id = lambda x: x.group_id
    map_ids = map(get_id, groups_list)
    list_ids = list(map_ids)
    if len(set(list_ids)) < len(list_ids):
        raise ValueError('Groups IDs are not unique')
