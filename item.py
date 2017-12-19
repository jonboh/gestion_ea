class Item:
    tree_header = ['Producto', 'Cantidad', 'Distribuidor', 'Proveedor', 'Referencia Dist.', 'Referencia EA',
                   'Precio Compra', 'PVP']
    default_header_map = [1 for _ in tree_header]

    def __init__(self, name='', quantity=0, distributor='', provider='', ref_dist='', ref_ea='', price_buy='0',
                 price_pvp='0', item_id='-1'):
        self.name = name
        self.quantity = quantity
        self.distributor = distributor
        self.provider = provider
        self.ref_dist = ref_dist
        self.ref_ea = ref_ea
        self.price_buy = float(price_buy)
        self.price_pvp = float(price_pvp)
        self.id = int(item_id)

    def __str__(self):
        ret_string = ';'.join(
            [self.name, self.quantity, self.distributor, self.provider, self.ref_dist, self.ref_ea, str(self.price_buy),
             str(self.price_pvp), str(self.id)])
        return ret_string

    def display(self):
        pass

    def tree_header_map(self, header_map):
        raw_entries_list = Item.tree_header
        entries_list = list()
        for entry, isincluded in zip(raw_entries_list, header_map[0:len(raw_entries_list)]):
            if isincluded:
                entries_list.append(entry)
        return entries_list

    def tree_entries(self, header_map):
        raw_entries_list = [self.name, self.distributor, self.provider, self.ref_dist,
                            self.ref_ea, self.price_buy, self.price_pvp, self.quantity]
        entries_list = list()
        for entry, isincluded in zip(raw_entries_list, header_map):
            if isincluded:
                entries_list.append(entry)
        return entries_list
