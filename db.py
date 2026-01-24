from peewee import * 
import pymysql
import bcrypt

db = MySQLDatabase('db',user='root',password='root',host='localhost',port=3306)

class BaseModel(Model):
    class Meta:
        database=db

class Type_apparat_pay(BaseModel):
    pay = CharField()

class Status_apparate(BaseModel):
    name = TextField()

class Counrty_proizv(BaseModel):
    name = TextField()

class Employee(BaseModel):
    surname = TextField()
    username = TextField()
    middle_name = TextField()

class Vendigovskiy_apparats(BaseModel):
    location = TextField()
    model = TextField()
    type_apparat = ForeignKeyField(Type_apparat_pay)
    sum_donate = IntegerField()
    number_ser = IntegerField(unique=True)
    invent_number = IntegerField(unique=True)
    firma = TextField()
    date_izgotov = DateField()
    date_input_system = DateField()
    # date_input_pretpri9tie = DateField(constraints=[SQL("Check ('date_izgotov <= date_input_pretpri9tie AND date_input_pretpri9tie <= date_input_system')")])
    date_input_pretpri9tie = DateField()
    # date_last_check = DateField(constraints=[SQL("Check ('date_izgotov <= date_last_check')")])
    date_last_check = DateField()
    # next_check = IntegerField(constraints=[Check('next_check > 0')])
    next_check = IntegerField()
    # resurs = IntegerField(constraints=[Check('resurs > 0')])
    resurs = IntegerField()
    # date_next_fix = DateField(constraints=[SQL("Check ('date_next_fix > date_input_system')")])
    date_next_fix = DateField()

    @property
    def next_check_date(self):
        from datetime import timedelta
        return self.date_last_check + timedelta(days=30 * self.next_check)

    # time_check = IntegerField(constraints=[Check('1 <= time_check <= 20')])
    time_check = IntegerField()
    status = ForeignKeyField(Status_apparate)
    counrty = ForeignKeyField(Counrty_proizv)
    # date_inventor = DateField(constraints=[Check(f"date_inventor >= date_izgotov")])
    date_inventor = DateField()
    employee_check = ForeignKeyField(Employee)

    class Meta:
        constraints=['SQL("date_izgotov <= date_last_check")']

class Item(BaseModel):
    id_item = AutoField()
    name = TextField()
    description = TextField()
    price = FloatField()
    count = IntegerField()
    min_zap = IntegerField()
    sclonnosti = FloatField()

class Type_pay(BaseModel):
    name = TextField()

class Bill(BaseModel):
    id_bill = AutoField()
    id_apparat = ForeignKeyField(Vendigovskiy_apparats)
    id_item = ForeignKeyField(Item)
    count = IntegerField()
    total_price = FloatField()
    date = DateTimeField()
    type_pay = ForeignKeyField(Type_pay)

class Role(BaseModel):
    name = TextField()

class User(BaseModel):
    id_user = AutoField()
    last_name = TextField()
    first_name = TextField()
    middle_name = TextField()
    password = TextField()

    def hash_password(self,password):
        self.password = bcrypt.hashpw(password.encode('utf-8'),bcrypt.gensalt()).decode('utf-8')

    def check_password(self,password):
        return bcrypt.checkpw(password.encode('utf-8'),self.password.encode('utf-8'))

    email = TextField()
    phone = TextField() 
    role = ForeignKeyField(Role)

class Checks(BaseModel):
    id_check = AutoField()
    id_apparat = ForeignKeyField(Vendigovskiy_apparats)
    date_check = DateTimeField()
    description = TextField()
    problem = TextField()
    employee = ForeignKeyField(Employee)

def init():
    conn = pymysql.connect(host='localhost', port=3306, user='root', password='root')
    conn.cursor().execute('CREATE DATABASE IF NOT EXISTS db')
    conn.close()

init()
db.create_tables([Checks,User,Role,Bill,Type_pay,Item,Vendigovskiy_apparats,Employee,Counrty_proizv,Status_apparate,Type_apparat_pay])

def test():
    type_1 = Type_apparat_pay.create(pay="карта")
    type_2 = Type_apparat_pay.create(pay="наличка")
    status_1 = Status_apparate.create(name="рабоатает")
    status_2 = Status_apparate.create(name="вышел из строя")
    status_3 = Status_apparate.create(name="в ремонте")
    status_4 = Status_apparate.create(name="на обслуживании")
    counrty_1 = Counrty_proizv.create(name='Россия')
    counrty_2 = Counrty_proizv.create(name='Польша')
    counrty_3 = Counrty_proizv.create(name='США')
    counrty_4 = Counrty_proizv.create(name='Китай')
    employee_1 = Employee.create(surname="работников",username="работник",middle_name="1")
    employee_2 = Employee.create(surname="работников",username="работник",middle_name="2")
    employee_3 = Employee.create(surname="работников",username="работник",middle_name="3")
    employee_4 = Employee.create(surname="работников",username="работник",middle_name="4")
    ven_app_1 = Vendigovskiy_apparats.create(
        location="Узбекистан",
        model='1',
        type_apparat=type_1,
        sum_donate=1000,
        number_ser=1,
        invent_number=1,
        firma='УКЗ',
        date_izgotov='2000-01-01',
        date_input_system='2000-01-01',
        date_input_pretpri9tie='2000-01-01',
        date_last_check='2000-01-01',
        next_check=10,
        resurs=1,
        date_next_fix='2000-01-01',
        time_check=20,
        status=status_1,
        counrty=counrty_1,
        date_inventor='2000-01-01',
        employee_check=employee_1
        )
    ven_app_2 = Vendigovskiy_apparats.create(
        location="Ватикан",
        model='2',
        type_apparat=type_2,
        sum_donate=1100,
        number_ser=2,
        invent_number=2,
        firma='ВКЗ',
        date_izgotov='2000-01-01',
        date_input_system='2000-01-01',
        date_input_pretpri9tie='2000-01-01',
        date_last_check='2000-01-01',
        next_check=10,
        resurs=2,
        date_next_fix='2000-01-01',
        time_check=10,
        status=status_2,
        counrty=counrty_2,
        date_inventor='2000-01-01',
        employee_check=employee_2
        )
    ven_app_3 = Vendigovskiy_apparats.create(
        location="Нигерия",
        model='3',
        type_apparat=type_2,
        sum_donate=1200,
        number_ser=3,
        invent_number=3,
        firma='НКЗ',
        date_izgotov='2000-01-01',
        date_input_system='2000-01-01',
        date_input_pretpri9tie='2000-01-01',
        date_last_check='2000-01-01',
        next_check=5,
        resurs=5,
        date_next_fix='2000-01-01',
        time_check=14,
        status=status_3,
        counrty=counrty_3,
        date_inventor='2000-01-01',
        employee_check=employee_3
        )
    ven_app_4 = Vendigovskiy_apparats.create(
        location="Латвия",
        model='4',
        type_apparat=type_1,
        sum_donate=9000,
        number_ser=4,
        invent_number=4,
        firma='ЛКЗ',
        date_izgotov='2000-01-01',
        date_input_system='2000-01-01',
        date_input_pretpri9tie='2000-01-01',
        date_last_check='2000-01-01',
        next_check=12,
        resurs=4,
        date_next_fix='2000-01-01',
        time_check=1,
        status=status_4,
        counrty=counrty_4,
        date_inventor='2000-01-01',
        employee_check=employee_4
        )
    item_1 = Item.create(name='стронг',description="мощный",price=1200,count=30,min_zap=10,sclonnosti='часто')
    item_2 = Item.create(name='портативная гитара',description="в форме ежа",price=5000,count=452,min_zap=10,sclonnosti='маленькая')
    item_3 = Item.create(name='галерея вкусов чай',description="лягушачий напиток",price=12,count=12000,min_zap=50,sclonnosti='средне')
    item_4 = Item.create(name='обои ',description="вайбовые обои, жужжат как жуки",price=1_000_000,count=10,min_zap=2,sclonnosti='маленькие')
    type_pay_1 = Type_pay.create(name="карта")
    type_pay_2 = Type_pay.create(name="qr")
    type_pay_3 = Type_pay.create(name="наличка")
    bill1 =  Bill.create(id_apparat=ven_app_1,id_item=item_1,count=15,total_price=12000*15,date='2000-01-01',type_pay=type_pay_1)
    bill2 =  Bill.create(id_apparat=ven_app_2,id_item=item_2,count=1,total_price=5000*1,date='2000-01-01',type_pay=type_pay_1)
    bill3 =  Bill.create(id_apparat=ven_app_3,id_item=item_3,count=1,total_price=12*1,date='2000-01-01',type_pay=type_pay_2)
    bill4 =  Bill.create(id_apparat=ven_app_4,id_item=item_4,count=1,total_price=1_000_000*1,date='2000-01-01',type_pay=type_pay_3)
    role1 = Role.create(name="администратор")
    role2 = Role.create(name="Оператор")
    role3 = Role.create(name='пользователь')
    user1 = User.create(last_name="юзер",first_name = "юзер",middle_name = "1",email = "1",phone = "1",role = role1)
    user2 = User.create(last_name="юзер",first_name = "юзер",middle_name = "2",email = "2",phone = "2",role = role2)
    user3 = User.create(last_name="юзер",first_name = "юзер",middle_name = "3",email = "3",phone = "3",role = role3)
    user4 = User.create(last_name="юзер",first_name = "юзер",middle_name = "4",email = "4",phone = "4",role = role3)
    checks1 = Checks.create(id_apparat=ven_app_1,date_check='2000-01-01',description='капут',problem='чип',employee=employee_1)
    checks2 = Checks.create(id_apparat=ven_app_2,date_check='2000-01-01',description='капут',problem='чип',employee=employee_2)
    checks3 = Checks.create(id_apparat=ven_app_3,date_check='2000-01-01',description='капут',problem='чип',employee=employee_3)
    checks4 = Checks.create(id_apparat=ven_app_4,date_check='2000-01-01',description='капут',problem='чип',employee=employee_4)

# test()