from db import *
from peewee import DoesNotExist
from random import choice


names = ["Ignat","Gleb","Nikita","Vlad","Olga","Karina"]

with open("C:/session_chmpion/sesseion main/session 1/Приложение Ресурсы/Ресурсы/Import/vending_machines.csv") as file:
    data = file.readlines()
    for i in range(1,len(data)):
        vending_app = data[i].split(';')
        number_ser = vending_app[0]
        name = vending_app[1]
        client = vending_app[2]
        try:
            client_obj = Client.get(Client.id == client)
        except DoesNotExist:
            client_obj = Client.create(id=client,name=choice(names))

        rfid_in = vending_app[3]
        notes = vending_app[4]
        location = vending_app[5]
        type_work = vending_app[6]
        rfid_dow = vending_app[7]
        model = vending_app[8]
        try:
            model_obj = Model.get(Model.name == model)
        except DoesNotExist:
            model_obj = Model.create(name=model)
        casse = vending_app[9]
        try:
            casse_obj = Casse.get(Casse.name == model)
        except DoesNotExist:
            casse_obj = Casse.create(name=casse)
        company = vending_app[10]
        try:
            company_obj = Company.get(Company.name == company)
        except DoesNotExist:
            company_obj = Company.create(name=company)
        type_apparat = vending_app[11]
        crit_znac = vending_app[12]
        priority = vending_app[13]
        manager = vending_app[14]
        try:
            manager_obj = Manager.get(Manager.name == manager)
        except DoesNotExist:
            manager_obj = Manager.create(name=manager)
        status = vending_app[15]
        signal = vending_app[16]
        time_work = vending_app[17]
        ingener = vending_app[18]
        try:
            ingener_obj = Ingener.get(Ingener.name == ingener)
        except DoesNotExist:
            ingener_obj = Ingener.create(name=ingener)
        id = vending_app[19]
        date_input_pretpri9tie = vending_app[20]
        place = vending_app[21]
        phone_operator = vending_app[22]
        try:
            phone_operator_obj = Phone_Op.get(Phone_Op.name_op == phone_operator)
        except DoesNotExist:
            phone_operator_obj = Phone_Op.create(name_op=phone_operator)
        employee_check = vending_app[23]
        try:
            employee_check_obj = Employee.get(Employee.name == employee_check)
        except DoesNotExist:
            employee_check_obj = Employee.create(name=phone_operator)
        date_last_check = vending_app[24]
        rfid_ob = vending_app[25]
        coord = vending_app[26]
        sum_incos = vending_app[27]
        time_zone = vending_app[28][:-2]
        Vendigovskiy_apparats.create(
            number_ser = number_ser,
            name = name,
            client = client_obj,
            rfid_in = rfid_in,
            notes = notes,
            location = location,
            type_work = type_work,
            rfid_dow = rfid_dow,
            model = model_obj,
            casse = casse_obj,
            company = company_obj,
            type_apparat = type_apparat,
            crit_znac = crit_znac,
            priority = priority,
            manager = manager_obj,
            status = status,
            signal = signal,
            time_work = time_work,
            ingener = ingener_obj,
            id = id,
            date_input_pretpri9tie = date_input_pretpri9tie,
            place = place,
            phone_operator = phone_operator_obj,
            employee_check = employee_check_obj,
            date_last_check = date_last_check,
            rfid_ob = rfid_ob,
            coord = coord,
            sum_incos = sum_incos,
            time_zone = time_zone
        )

        