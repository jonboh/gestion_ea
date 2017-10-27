class Group:
    str_header = ['Actividad', 'Monitor/a', 'Dias', 'Inicio', 'Final', 'Precio', 'Limite de Miembros', 'Miembros',
                  'ID Grupo']

    def __init__(self, name_activity='', name_teacher='', days='', time_start='', time_end='', price='',
                 limit_members='', members='{}',
                 group_id=''):
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

    def timetable_format(self):
        hour_start = int(self.time_start / 100)
        min_start = int(self.time_start - 100 * hour_start)
        hour_end = int(self.time_end / 100)
        min_end = int(self.time_end - 100 * hour_end)

        time_str = str(hour_start) + ':'
        if min_start < 10:
            time_str = time_str + '0' + str(min_start) + ' - ' + str(hour_end) + ':'
        else:
            time_str = time_str + str(min_start) + ' - ' + str(hour_end) + ':'
        if min_end < 10:
            time_str = time_str + '0' + str(min_end)
        else:
            time_str = time_str + str(min_end)

        return time_str

    def days_format(self):
        days_str = ''
        if 'L' in self.days:
            days_str = days_str + 'Lunes '
        if 'M' in self.days:
            days_str = days_str + 'Martes'
        if 'X' in self.days:
            days_str = days_str + 'Miercoles'
        if 'J' in self.days:
            days_str = days_str + 'Jueves '
        if 'V' in self.days:
            days_str = days_str + 'Viernes '
        if 'S' in self.days:
            days_str = days_str + 'Sabado '
        if 'D' in self.days:
            days_str = days_str + 'Domingo '
        return days_str


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
