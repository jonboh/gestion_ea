class Group:
    tree_header = ['Actividad', 'Monitor/a', 'Dias', 'Horario', 'Precio', 'Numero de Miembros',
                   'Limite de Miembros', 'ID Grupo']
    default_header_map = [1 for _ in tree_header]

    def __init__(self, name_activity='', name_teacher='', days='{}', time_start='00', time_end='00',
                 price='0.0',
                 limit_members='0', members='{}',
                 group_id='-1'):
        self.name_activity = name_activity
        self.name_teacher = name_teacher
        if type(eval(days)) is dict:
            self.days = set()
        else:
            self.days = eval(days)
        self.time_start = int(time_start)
        self.time_end = int(time_end)
        self.price = float(price)
        if type(eval(members)) is dict:
            self.members = set()
        else:
            self.members = eval(members)  # set
        self.limit_members = int(limit_members)
        self.id = int(group_id)

    def __str__(self):
        ret_string = ';'.join(
            [self.name_activity, self.name_teacher, str(self.days), str(self.time_start),
             str(self.time_end), str(self.price), str(self.limit_members), str(self.members),
             str(self.id)])
        return ret_string

    def display(self):
        disp_string = ' '.join(
            [self.name_activity, self.name_teacher, self.days_format(), self.timetable_format()])
        return disp_string

    def tree_header_map(self, header_map):
        raw_entries_list = Group.tree_header
        entries_list = list()
        for entry, isincluded in zip(raw_entries_list, header_map[0:len(raw_entries_list)]):
            if isincluded:
                entries_list.append(entry)
        return entries_list

    def tree_entries(self, header_map):
        raw_entries_list = [self.name_activity, self.name_teacher, self.days_format(),
                            self.timetable_format(),                            self.price,
                            len(self.members), self.limit_members, self.id]
        entries_list = list()
        for entry, isincluded in zip(raw_entries_list, header_map):
            if isincluded:
                entries_list.append(entry)
        return entries_list

    def timetable_format(self):
        hour_start = int(self.time_start / 100)
        min_start = int(self.time_start - 100 * hour_start)
        hour_end = int(self.time_end / 100)
        min_end = int(self.time_end - 100 * hour_end)

        if hour_start < 10:
            time_str = '0' + str(hour_start) + ':'
        else:
            time_str = str(hour_start) + ':'
        if min_start < 10:
            time_str = time_str + '0' + str(min_start) + ' - '
        else:
            time_str = time_str + str(min_start) + ' - '
        if hour_end < 10:
            time_str = time_str + '0' + str(hour_end) + ':'
        else:
            time_str = time_str + str(hour_end) + ':'
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
            days_str = days_str + 'Martes '
        if 'X' in self.days:
            days_str = days_str + 'Miercoles '
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
    def get_id(element): return element.id
    map_ids = map(get_id, elements_list)
    list_ids = list(map_ids)
    if len(list_ids) == 0:
        id_available = 0
    else:
        id_available = max(list_ids) + 1
    return id_available


def check_id_integrity(elements_list):
    def get_id(element): return element.id
    map_ids = map(get_id, elements_list)
    list_ids = list(map_ids)
    if len(set(list_ids)) < len(list_ids):
        return False
    else:
        return True
