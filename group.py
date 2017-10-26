class Group:
    def __init__(self, price: float, time_start: int, time_end: int, name_teacher: str, name_activity: str,
                 limit_members: int, members: set):
        self.price = price
        self.time_start = time_start
        self.time_end = time_end
        self.name_teacher = name_teacher
        self.name_activity = name_activity
        self.limit_members = limit_members
        self.members = members
