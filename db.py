from peewee import * 
import pymysql
import bcrypt

db = MySQLDatabase('db',user='root',password='root',host='localhost',port=3306)

class BaseModel(Model):
    class Meta:
        database=db

class Type_apparat_pay(BaseModel):
    mo = BooleanField(null=True)
    cu = BooleanField(null=True)
    be = BooleanField(null=True)
    qr = BooleanField(null=True)

class Status_apparate(BaseModel):
    name = TextField()

class Counrty_proizv(BaseModel):
    name = TextField()

class Employee(BaseModel):
    surname = TextField()
    username = TextField()
    middle_name = TextField()

class Product_matrix(BaseModel):
    name = TextField()

class TimeZone(BaseModel):
    time_zone = CharField(unique=True)

class Action(BaseModel):
    edit = BooleanField(null=True)
    delete = BooleanField(null=True)
    block = BooleanField(null=True)

class Type_work(BaseModel):
    name = TextField()

class Firma(BaseModel):
    name = TextField()

class Model(BaseModel):
    name = TextField()

class Client(BaseModel):
    name = TextField()

class Manager(BaseModel):
    name = TextField()

class Ingener(BaseModel):
    name = TextField()

class Operator(BaseModel):
    name = TextField()

class Priority(BaseModel):
    name = TextField()

class Casse(BaseModel):
    id = TextField()


class Vendigovskiy_apparats(BaseModel):
    name = TextField(null=True)
    company = TextField(null=True)
    modem = IntegerField(null=True)
    location = TextField(null=True)
    adres = TextField(null=True)
    coord = TextField(null=True)
    time_work = TimeField(null=True)
    model = ForeignKeyField(Model,null=True)
    type_work = ForeignKeyField(Type_work,null=True)
    action = ForeignKeyField(Action,null=True)
    type_apparat = ForeignKeyField(Type_apparat_pay,null=True)
    sum_donate = IntegerField(null=True)
    number_ser = IntegerField(unique=True,null=True)
    invent_number = IntegerField(unique=True,null=True)
    firma = ForeignKeyField(Firma,null=True)
    crit_znac = TextField(null=True)
    signal = TextField(null=True)
    time_zone = ForeignKeyField(TimeZone,null=True)
    date_izgotov = DateField(null=True)
    date_input_system = DateField(null=True)
    matrix = ForeignKeyField(Product_matrix,null=True)
    client = ForeignKeyField(Client,null=True)
    ingener = ForeignKeyField(Ingener,null=True)
    manager = ForeignKeyField(Manager,null=True)
    op = ForeignKeyField(Operator,null=True)
    priority = ForeignKeyField(Priority,null=True)
    rfid_ob = IntegerField(null=True)
    rfid_in = IntegerField(null=True)
    rfid_dow = IntegerField(null=True)
    casse = TextField(null=True)
    # date_input_pretpri9tie = DateField(constraints=[SQL("Check ('date_izgotov <= date_input_pretpri9tie AND date_input_pretpri9tie <= date_input_system')")])
    date_input_pretpri9tie = DateField(null=True)
    # date_last_check = DateField(constraints=[SQL("Check ('date_izgotov <= date_last_check')")])
    date_last_check = DateField(null=True)
    # next_check = IntegerField(constraints=[Check('next_check > 0')])
    next_check = IntegerField(null=True)
    # resurs = IntegerField(constraints=[Check('resurs > 0')])
    resurs = IntegerField(null=True)
    # date_next_fix = DateField(constraints=[SQL("Check ('date_next_fix > date_input_system')")])
    date_next_fix = DateField(null=True)

    @property
    def next_check_date(self):
        from datetime import timedelta
        return self.date_last_check + timedelta(days=30 * self.next_check)

    # time_check = IntegerField(constraints=[Check('1 <= time_check <= 20')])
    time_check = IntegerField(null=True)
    status = ForeignKeyField(Status_apparate,null=True)
    counrty = ForeignKeyField(Counrty_proizv,null=True)
    # date_inventor = DateField(constraints=[Check(f"date_inventor >= date_izgotov")])
    date_inventor = DateField()
    employee_check = ForeignKeyField(Employee,null=True)

    class Meta:
        constraints = [
            # Все CHECK constraints должны быть здесь, на уровне таблицы
            SQL("CHECK (date_input_pretpri9tie >= date_izgotov AND date_input_pretpri9tie <= date_input_system)"),
            SQL("CHECK (date_last_check >= date_izgotov)"),
            SQL("CHECK (next_check > 0)"),
            SQL("CHECK (resurs > 0)"),
            SQL("CHECK (date_next_fix >= date_input_system)"),
            SQL("CHECK (time_check BETWEEN 1 AND 20)"),
            SQL("CHECK (date_inventor >= date_izgotov)")
        ]


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
db.create_tables([Checks,User,Role,Bill,Type_pay,Item,
                  Vendigovskiy_apparats,Employee,Counrty_proizv,
                  Status_apparate,Type_apparat_pay,Action,Firma,Type_work,Priority,Operator,
                  Ingener,Manager,Client,Model,TimeZone,Product_matrix,Casse])

def test():
    type_1 = Type_apparat_pay.create(mo=True,cu=True,be=True,qr=True)
    type_2 = Type_apparat_pay.create(mo=True,cu=False)
    type_3 = Type_apparat_pay.create(be=True,qr=True)
    type_4 = Type_apparat_pay.create(cu=True,be=True,qr=True)

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

    action_1 = Action.create(edit=True)
    action_2 = Action.create(edit=True,block=True)
    action_3 = Action.create(edit=True,delete=True,block=True)
    action_4 = Action.create(edit=True,delete=True)
    action_5 = Action.create(block=True)
    action_6 = Action.create(delete=True,block=True)
    action_7 = Action.create()

    time_1 = TimeZone.create(time_zone='UTC+2')
    time_2 = TimeZone.create(time_zone='UTC+3')
    time_3 = TimeZone.create(time_zone='UTC+4')
    time_4 = TimeZone.create(time_zone='UTC+5')
    time_5 = TimeZone.create(time_zone='UTC+6')
    time_6 = TimeZone.create(time_zone='UTC+7')
    time_7 = TimeZone.create(time_zone='UTC+8')
    time_8 = TimeZone.create(time_zone='UTC+9')
    time_9 = TimeZone.create(time_zone='UTC+10')
    time_10 = TimeZone.create(time_zone='UTC+11')
    time_11 = TimeZone.create(time_zone='UTC+12')

    firma_1 = Firma.create(name='ЛКЗ')
    firma_2 = Firma.create(name='ЧМК')
    firma_3 = Firma.create(name='ЧМЗ')
    firma_4 = Firma.create(name='КЗУ')

    model_1 = Model.create(name='1')
    model_2 = Model.create(name='2')
    model_3 = Model.create(name='3')
    model_4 = Model.create(name='4')
    model_5 = Model.create(name='5')
    model_6 = Model.create(name='6')
    model_7 = Model.create(name='7')
    model_8 = Model.create(name='8')
    model_9 = Model.create(name='9')
    model_10 = Model.create(name='10')

    type_work_1 = Type_work.create(name='Стандартный')
    type_work_2 = Type_work.create(name='Замедленный')
    type_work_3 = Type_work.create(name='Повышенный')

    matrix_1 = Product_matrix.create(name='Напитки')
    matrix_2 = Product_matrix.create(name='Еда')
    matrix_3 = Product_matrix.create(name='Вкусности')

    client_1 = Client.create(name='Вася')
    client_2 = Client.create(name='Петя')
    client_3 = Client.create(name='Маша')

    manager_1 = Manager.create(name='Марат')
    manager_2 = Manager.create(name='Дмитрий')
    manager_3 = Manager.create(name='Елизавета')

    ingener_1 = Ingener.create(name='Дядя Вова')
    ingener_2 = Ingener.create(name='Дядя Миша')
    ingener_3 = Ingener.create(name='Дядя Саша')

    op_1 = Operator.create(name='Владимир')
    op_2 = Operator.create(name='Николай')
    op_3 = Operator.create(name='Павел')

    priority_1 = Priority.create(name='Низкий')
    priority_2 = Priority.create(name='Средний')
    priority_3 = Priority.create(name='Высокий')

    casse_1 = Casse.create(id=None)
    casse_2 = Casse.create(id=None)
    casse_3 = Casse.create(id=None)

    ven_app_1 = Vendigovskiy_apparats.create(
        location="Магазин Магнит",
        crit_znac = '1',
        sign='1',
        client=client_1,
        ingener=ingener_1,
        manager=manager_1,
        op=op_1,
        priority=priority_1,
        model=model_1,
        matrix=matrix_1,
        name = 'ГП Магнит',
        company = 'ООО ТА',
        modem = '123456789',
        action= action_1,
        time_zone=time_1,
        type_apparat=type_1,
        type_work=type_work_1,
        sum_donate=1000,
        number_ser=1,
        invent_number=1,
        firma=firma_1,
        rfid_card_ob = 1,
        rfid_card_in=1,
        rfid_card_dow=1,
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
        employee_check=employee_1,
        casse="1"
        )
    ven_app_2 = Vendigovskiy_apparats.create(
        location="Магазин Пятерочка",
        model=model_2,
        crit_znac = '2',
        client=client_1,
        ingener=ingener_1,
        manager=manager_2,
        op=op_1,
        priority=priority_2,
        sign='2',
        matrix=matrix_2,
        name = 'Пятерочка',
        company = 'ООО ТА',
        modem = '123456789',
        action= action_2,
        time_zone=time_2,
        type_apparat=type_2,
        type_work=type_work_2,
        sum_donate=1100,
        number_ser=2,
        invent_number=2,
        firma=firma_2,
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
        casse="2",
        employee_check=employee_2
        )
    ven_app_3 = Vendigovskiy_apparats.create(
        location="Магазин ВЛ",
        model=model_3,
        crit_znac = '3',
        client=client_1,
        ingener=ingener_1,
        manager=manager_3,
        op=op_1,
        priority=priority_3,
        sign='3',
        matrix=matrix_3,
        name = 'Высшая лига',
        company = 'ООО ТА',
        modem = '123456789',
        action= action_3,
        time_zone=time_3,
        type_apparat=type_3,
        type_work=type_work_3,        
        sum_donate=1200,
        number_ser=3,
        invent_number=3,
        firma=firma_3,
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
        casse="casse_3",
        employee_check=employee_3
        )
    ven_app_4 = Vendigovskiy_apparats.create(
        location="Механический завод",
        model=model_4,
        crit_znac = '4',
        client=client_1,
        ingener=ingener_2,
        manager=manager_1,
        op=op_2,
        priority=priority_1,
        sign='4',
        matrix=matrix_1,
        name = 'Мой завод',
        company = 'ООО ТА',
        modem = '123456789',
        action= action_4,
        time_zone=time_4,
        type_apparat=type_1,
        type_work=type_work_1,
        sum_donate=9000,
        number_ser=4,
        invent_number=4,
        firma=firma_4,
        date_izgotov='2000-01-01',
        date_input_system='2000-01-01',
        date_input_pretpri9tie='2000-01-01',
        date_last_check='2000-01-01',
        next_check=12,
        resurs=4,
        date_next_fix='2000-01-01',
        time_check=1,
        status=status_1,
        counrty=counrty_4,
        date_inventor='2000-01-01',
        employee_check=employee_4,
        casse="casse_1",
        )
    ven_app_5 = Vendigovskiy_apparats.create(
        location="КГУ",
        client=client_1,
        ingener=ingener_2,
        manager=manager_2,
        model=model_5,
        crit_znac = '5',
        op=op_2,
        priority=priority_2,
        sign='5',
        matrix=matrix_2,
        name = 'КГУ',
        company = 'ООО ТА',
        modem = '123456789',
        action= action_7,
        time_zone=time_5,
        type_apparat=type_4,
        type_work=type_work_2,
        sum_donate=9000,
        number_ser=5,
        invent_number=5,
        firma=firma_1,
        date_izgotov='2000-01-01',
        date_input_system='2000-01-01',
        date_input_pretpri9tie='2000-01-01',
        date_last_check='2000-01-01',
        next_check=12,
        resurs=4,
        date_next_fix='2000-01-01',
        time_check=1,
        status=status_3,
        counrty=counrty_4,
        date_inventor='2000-01-01',
        casse="casse_2",
        employee_check=employee_4
        )
    ven_app_6 = Vendigovskiy_apparats.create(
        location="ТЦ РИО",
        model=model_6,
        client=client_1,
        ingener=ingener_2,
        manager=manager_3,
        crit_znac = '6',
        op=op_2,
        priority=priority_3,
        sign='6',
        matrix=matrix_3,
        name = 'ГаЗи',
        company = 'ООО ТА',
        modem = '123456789',
        action= action_4,
        time_zone=time_6,
        type_apparat=type_1,
        type_work=type_work_3,
        sum_donate=9000,
        number_ser=6,
        invent_number=6,
        firma=firma_2,
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
        casse="casse_3",
        employee_check=employee_4
        )
    ven_app_7 = Vendigovskiy_apparats.create(
        location="ТЦ РИО",
        model=model_7,
        client=client_1,
        ingener=ingener_3,
        manager=manager_3,
        crit_znac = '7',
        op=op_3,
        priority=priority_1,
        sign='7',
        matrix=matrix_1,
        name = 'ПоКУШАЙ',
        company = 'ООО ТА',
        modem = '123456789',
        action= action_4,
        time_zone=time_7,
        type_apparat=type_2,
        type_work=type_work_1,
        sum_donate=9000,
        number_ser=7,
        invent_number=7,
        firma=firma_3,
        date_izgotov='2000-01-01',
        date_input_system='2000-01-01',
        date_input_pretpri9tie='2000-01-01',
        date_last_check='2000-01-01',
        next_check=12,
        resurs=4,
        date_next_fix='2000-01-01',
        time_check=1,
        status=status_1,
        counrty=counrty_4,
        date_inventor='2000-01-01',
        casse="casse_1",
        employee_check=employee_4
        )
    ven_app_8 = Vendigovskiy_apparats.create(
        location="ТЦ РИО",
        model=model_8,
        client=client_2,
        ingener=ingener_1,
        manager=manager_1,
        op=op_3,
        priority=priority_3,
        crit_znac = '8',
        sign='8',
        matrix=matrix_2,
        name = 'ПРИЗОПАД',
        company = 'ООО ТА',
        modem = '123456789',
        action= action_4,
        time_zone=time_8,
        type_apparat=type_3,
        type_work=type_work_2,
        sum_donate=9000,
        number_ser=8,
        invent_number=8,
        firma=firma_4,
        date_izgotov='2000-01-01',
        date_input_system='2000-01-01',
        date_input_pretpri9tie='2000-01-01',
        date_last_check='2000-01-01',
        next_check=12,
        resurs=4,
        date_next_fix='2000-01-01',
        time_check=1,
        status=status_2,
        counrty=counrty_4,
        date_inventor='2000-01-01',
        casse="casse_3",
        employee_check=employee_4
        )
    ven_app_9 = Vendigovskiy_apparats.create(
        location="ТЦ РИО",
        model=model_9,
        client=client_2,
        ingener=ingener_2,
        manager=manager_1,
        op=op_3,
        priority=priority_2,
        crit_znac = '9',
        sign='9',
        matrix=matrix_3,
        name = 'Кофей-ок',
        company = 'ООО ТА',
        modem = '123456789',
        action= action_4,
        time_zone=time_9,
        type_apparat=type_3,
        type_work=type_work_3,
        sum_donate=9000,
        number_ser=9,
        invent_number=9,
        firma=firma_1,
        date_izgotov='2000-01-01',
        date_input_system='2000-01-01',
        date_input_pretpri9tie='2000-01-01',
        date_last_check='2000-01-01',
        next_check=12,
        resurs=4,
        date_next_fix='2000-01-01',
        time_check=1,
        status=status_1,
        counrty=counrty_4,
        date_inventor='2000-01-01',
        casse="casse_1",
        employee_check=employee_4
        )
    ven_app_10 = Vendigovskiy_apparats.create(
        location="КПК",
        client=client_2,
        ingener=ingener_3,
        manager=manager_3,
        matrix=matrix_1,
        op=op_1,
        priority=priority_1,
        crit_znac = '10',
        sign='10',
        model=model_10,
        name = 'Барахолка',
        company = 'ООО ТА',
        modem = '123456789',
        action = action_4,
        time_zone=time_10,
        type_apparat=type_4,
        type_work=type_work_1,
        sum_donate=9000,
        number_ser=10,
        invent_number=10,
        firma=firma_2,
        date_izgotov='2000-01-01',
        date_input_system='2000-01-01',
        date_input_pretpri9tie='2000-01-01',
        date_last_check='2000-01-01',
        next_check=12,
        resurs=4,
        date_next_fix='2000-01-01',
        time_check=1,
        status=status_1,
        counrty=counrty_4,
        date_inventor='2000-01-01',
        casse="casse_2",
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