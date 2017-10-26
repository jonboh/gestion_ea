class Group:
    def __init__(self, price: str, time_start: str, time_end: str, name_teacher: str, name_activity: str,
                 limit_members: str, members: str, group_num: str):
        self.name_teacher = name_teacher
        self.name_activity = name_activity
        self.price = float(price)
        self.time_start = time_start
        self.time_end = time_end
        self.limit_members = limit_members
        self.members = eval(members)  # set
        self.group_num = int(group_num)


def check_integrity_groups_list(groups_list):
    get_id = lambda x : x.group_num
    map_ids = map(get_id, groups_list)
    list_ids = list(map_ids)
    if len(set(list_ids)) < len(list_ids):
        raise ValueError('Groups IDs are not unique')