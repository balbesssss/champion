from db import Bill

with open("C:\session_chmpion\sesseion main\session 1\Приложение Ресурсы\Ресурсы\Import\sales.csv") as file:
    data = file.readlines()
    data = data[1:]
    for row in data:
        row_data = row.split(';')
        Bill.create(
            date=row_data[0],
            id_item=row_data[1],
            total_price=row_data[2],
            count=row_data[3],
            type_pay=row_data[4],
        )

