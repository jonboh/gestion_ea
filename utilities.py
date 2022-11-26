def get_group_byid(id, groups):
    group_ids = list(map(lambda group: group.id, groups))
    return groups[group_ids.index(id)]


def client_has_vat(client, groups):
    for group_id in client.groups:
        group = get_group_byid(group_id, groups)
        if group.vat != 0:
            return True
    return False
