import csv

import client as cl
import data_io as io

file_mncsv = 'datos_mn.csv'
output_file = 'alumns.txt'
client_list = list()
with open(file_mncsv) as file:
    reader = csv.reader(file, delimiter=',')
    counter = 0
    for row in reader:
        if counter is 0:
            counter = counter +1
            continue
        name_surname = row[0].split(' ')
        name = name_surname[0]
        surname = ' '.join(name_surname[1:])
        id_card = row[1]
        email = row[2]
        phone1 = row[3]
        phone2 = row[4]
        bank_acc = row[5]
        new_id = counter

        client_list.append(cl.Alumn(name,surname,id_card,phone1,phone2,email,new_id,'1',bank_acc,0))
        counter = counter + 1

io.write_clients(output_file, client_list, cl.Alumn)