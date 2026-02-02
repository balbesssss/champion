from tkinter import *
from tkinter import ttk
import PIL.Image
import PIL.ImageTk
from db import Vendigovskiy_apparats, Status_apparate, Action, \
    Firma, Model, Type_work, TimeZone,Client, Ingener, Manager, \
        Operator, Priority, Product_matrix, Type_apparat_pay,Casse,Counrty_proizv,Employee, User, Role
import datetime
from tkinter.messagebox import showinfo,showerror,showwarning



root = Tk()
root.geometry('1920x1080')

frame_for_hat = Frame(root,background='white',width=1920-150,height=50)
frame_for_hat.place(x=0,y=0)

frame_auth = Button(root,background='white')
frame_auth.place(x=1920-150+2,y=0,width=150,height=50)

select = False


def check():
    try:
        f = open('data.txt')
    except FileNotFoundError:
        return None
    return f.readline().split(",")

def auth(*args):
    with open('data.txt','w') as f:
        f.write(','.join(str(i) for i in args))


def person_menu(event):

    global select, auth_canvas, frame_auth
    data = check()

    if data:
        frame_auth.config(text=data[0])
        if not select:

            auth_canvas = Canvas(root, width=150,height=200,background="white")
            auth_canvas.place(x=1920-150+2,y=60)


            def my_profile(event):
                nonlocal data
                

            but_profile = Button(auth_canvas,background="white",text="Мой профиль")
            but_profile.place(x=0,y=25,width=150,height=50)
            but_profile.bind("<Button-1>", my_profile)
            but_session = Button(auth_canvas,background="white",text="Мои сессии")
            but_session.place(x=0,y=75,width=150,height=50)

            but_exit = Button(auth_canvas,background="white",text="Выход")
            but_exit.place(x=0,y=125,width=150,height=50)

            select = True
        else:
            auth_canvas.destroy()
            select = False
    else:
        win = Canvas(root, width=150,height=200,background="white")
        win.place(x=1920//4+400,y=500)
        name_win = ttk.Entry(win)
        name_win.place(x=30,y=30,width=100,height=20)
        email_win = ttk.Entry(win)
        email_win.place(x=30,y=50,width=100,height=20)
        phone_win = ttk.Entry(win) 
        phone_win.place(x=30,y=70,width=100,height=20)
        role_win = ttk.Entry(win)
        role_win.place(x=30,y=90,width=100,height=20)
        pass_win = ttk.Entry(win) 
        pass_win.place(x=30,y=110,width=100,height=20)
        but_reg = Button(win,text='Авторизироваться')
        but_reg.place(x=30,y=150)
        def reg(event):
            data_reg = [name_win.get(),email_win.get(),phone_win.get(),
                        role_win.get(),pass_win.get()]
            role_name = Role.get(Role.name == data_reg[3])
            with open('data.txt','w') as f:
                f.write(','.join(str(i) for i in data_reg))
                User.create(username=data_reg[0],
                            email=data_reg[1],
                            phone=data_reg[2],
                            role=role_name,
                            password=data_reg[4])
                showinfo(title="Регистрация",message='Успешно доабвлен')
            win.destroy()
            frame_auth['text'] = data[0]
        but_reg.bind('<Button-1>',reg)



frame_auth.bind("<Button-1>",person_menu)

frame_left_side = Frame(root,background='#142733',width=1920//4,height=1080-50)
frame_left_side.place(x=0, y=50)

nav = Label(frame_left_side,text='Навигация',background='#142733',foreground='white',font=(...,22))
nav.place(x=5,y=5,width=150, height=50)

but_three_line = Button(frame_left_side, text='≡' ,background='#142733', foreground="white",font=(...,22))
but_three_line.place(x=430,y=5,width=50, height=50)

img_lupa = PIL.Image.open('i.png')
img_lupa = img_lupa.resize((50,50))
photo_lupa = PIL.ImageTk.PhotoImage(img_lupa)

button_main = Button(frame_left_side,image=photo_lupa,text="Главная",background='#142733',compound=LEFT,foreground="White",font=(...,22),anchor='w')
button_main.place(x=5,y=55,width=1920//4,height=50)

canvas_right_side = Canvas(root)
canvas_right_side.place(x=480,y=50,width=1920-480,height=1080-115)

class Pattenr:
    def main():
        canvas_right_side = Canvas(root)
        canvas_right_side.place(x=480,y=50,width=1920-480,height=1080-115)
        Label(canvas_right_side,text='ООО Торговые автоматы',background='#142733',foreground='white',font=(...,22),anchor=W).place(x=5,y=5,width=1920-480, height=50)
        Label(canvas_right_side,text='Личный кабинет. Главная',foreground='black',font=(...,22),anchor=W).place(x=45,y=100,width=350, height=50)
        effe_network = Frame(canvas_right_side,background='white',width=(1920-480)//3-50, height=200)
        effe_network.place(x=70,y=200)
        working_apparat = 0
        all_ven_app = 0
        stat_work = Status_apparate.get(Status_apparate.name == "рабоатает")

        for apparat in Vendigovskiy_apparats.select():
            if apparat.status == stat_work:
                working_apparat+=1
            all_ven_app = apparat.id

        label_for_effe = Label(effe_network, text=f"Работающих автоматов {round(((working_apparat/all_ven_app)*100),2)}",foreground='black',background="white",font=(...,11))
        label_for_effe.place(x=120,y=170,width=225,height=15)

        Label(effe_network,text="Эффективность сети",foreground='black',font=(...,18),anchor=W).place(x=5,y=5,width=(1920-480)//3-65, height=50)

        status_network = Frame(canvas_right_side,background='white',width=(1920-480)//3-50, height=200)
        status_network.place(x=535,y=200)

        working=0
        remont = 0
        not_working=0

        for apparat in Vendigovskiy_apparats.select():
            if apparat.status.id == 1:
                working+=1
            if apparat.status.id == 3:
                remont+=1
            if apparat.status.id == 2:
                not_working+=1

        canvas_for_status = Canvas(status_network,background='white',width=(1920-480)//3-49, height=150)
        canvas_for_status.place(x=-2,y=55)

        total = working+remont+not_working

        canvas_for_status.create_rectangle(10,40,10+(working / total) * 430,55,fill='green')
        canvas_for_status.create_rectangle(10,65,10+(not_working / total) * 430,80,fill='red')
        canvas_for_status.create_rectangle(10,90,10+(remont / total) * 430,105,fill='blue')

        canvas_for_status_canvas = Canvas(canvas_for_status,background='white',width=(1920-480)//3-49, height=20)
        canvas_for_status_canvas.place(x=0,y=120)

        canvas_for_status_canvas.create_rectangle(10,5,25,20,fill='green')
        canvas_for_status_canvas.create_text(60,12,text='- работает')

        canvas_for_status_canvas.create_rectangle(160,5,175,20,fill='red')
        canvas_for_status_canvas.create_text(210,12,text='- не работает')

        canvas_for_status_canvas.create_rectangle(310,5,325,20,fill='blue')
        canvas_for_status_canvas.create_text(360,12,text='- в ремонте')

        Label(status_network,text="Состояние сети",foreground='black',font=(...,18),anchor=W).place(x=5,y=5,width=(1920-480)//3-65, height=50)

        info = Frame(canvas_right_side,background='white',width=(1920-480)//3-50, height=200)
        info.place(x=535+460,y=200)

        Label(info,text="Сводка",foreground='black',font=(...,18),anchor=W).place(x=5,y=5,width=(1920-480)//3-65, height=50)

        money_info = Label(info,text="Денег в ТА")
        money_info.place(x=5,y=60, height=20)
        money_info = Label(info,text="Сдача в ТА")
        money_info.place(x=5,y=80, height=20)
        money_info = Label(info,text="Выручка сегодня")
        money_info.place(x=5,y=100, height=20)
        money_info = Label(info,text="Выручка вчера")
        money_info.place(x=5,y=120, height=20)
        money_info = Label(info,text="Инкасированно сегодня")
        money_info.place(x=5,y=140, height=20)
        money_info = Label(info,text="Инкасированно вчера")
        money_info.place(x=5,y=160, height=20)
        money_info = Label(info,text="Обслуженно ТА, сег/вчера")
        money_info.place(x=5,y=180, height=20)

        dynamic_sell = Frame(canvas_right_side,background='white',width=(500+480)-85, height=200*3-100)
        dynamic_sell.place(x=70,y=200*2+20)

        news = Frame(canvas_right_side,background='white',width=(1920-480)//3-50, height=200*3-100)
        news.place(x=535+460,y=200*2+20)

        Label(news,text="Новости",foreground='black',font=(...,18),anchor=W).place(x=5,y=5,width=(1920-480)//3-65, height=50)

    def admin():
        canvas_right_side = Canvas(root)
        canvas_right_side.place(x=480,y=50,width=1920-480,height=1080-115)
        Label(canvas_right_side,text='ООО Торговые автоматы',background='#142733',foreground='white',font=(...,22),anchor=W).place(x=5,y=5,width=1920-480, height=50)
        canvas_admin = Canvas(canvas_right_side,background='white')
        canvas_admin.place(x=(1920-480)//4,y=75,width=(1920-480)//2,height=1000-145)
        canvas_admin.create_line(0,2,(1920-480)//4+(1920-480)//2,2,fill='blue')
        canvas_admin.create_line(0,3,(1920-480)//4+(1920-480)//2,3,fill='blue')
        canvas_admin.create_line(0,4,(1920-480)//4+(1920-480)//2,4,fill='blue')
        Label(canvas_right_side,text='ООО Торговые автоматы',background='#142733',foreground='white',font=(...,22),anchor=W).place(x=5,y=5,width=1920-480, height=50)
        frame_under_label = Frame(canvas_admin,background='#F7F7F7')
        frame_under_label.place(x=0,y=5,width=(1920-480)//2-2,height=75)
        Label(frame_under_label,text='Торговые автоматы',foreground='blue',bg='#F7F7F7',font=(...,16)).place(x=20,y=10)

        def add_VA():
            add_win = Canvas(canvas_right_side,background='white')
            add_win.place(x=(1920-480)//4,y=75,width=(1920-480)//2,height=1000-115)
            add_win.create_line(0,2,(1920-480)//4+(1920-480)//2,2,fill='blue')
            add_win.create_line(0,3,(1920-480)//4+(1920-480)//2,3,fill='blue')
            add_win.create_line(0,4,(1920-480)//4+(1920-480)//2,4,fill='blue')
            frame_under_label = Frame(add_win,background='#F7F7F7')
            frame_under_label.place(x=0,y=5,width=(1920-480)//2-2,height=50)
            Label(frame_under_label,text='Создание торгового автоата',foreground='blue',bg='#F7F7F7',font=(...,16)).place(x=20,y=10)

            Label(add_win,text='Название',background='white',foreground='black').place(x=10,y=60)

            name = ttk.Entry(add_win)
            name.place(x=10,y=90,width=200,height=20)

            Label(add_win,text='Производитель ТА',background='white',foreground='black').place(x=260,y=60)

            proi_list = [firma.name for firma in Firma.select()]

            proizvod = ttk.Combobox(add_win,values=proi_list)
            proizvod.place(x=260,y=90,width=200,height=20)

            Label(add_win,text='Модель ТА',background='white',foreground='black').place(x=510,y=60)

            model_list = [model.name for model in Model.select()]

            model = ttk.Combobox(add_win,values=model_list)
            model.place(x=510,y=90,width=200,height=20)

            Label(add_win,text='Режим работы',background='white',foreground='black').place(x=10,y=150)

            work_list = [type_work.name for type_work in Type_work.select()]

            type_work = ttk.Combobox(add_win,values=work_list)
            type_work.place(x=10,y=170,width=200,height=20)

            Label(add_win,text='Производитель ТА (Slave)',background='white',foreground='black').place(x=260,y=150)

            proizvod_slave = ttk.Entry(add_win)
            proizvod_slave.place(x=260,y=170,width=200,height=20)

            Label(add_win,text='Модель ТА (Slave)',background='white',foreground='black').place(x=510,y=150)

            model_slave = ttk.Entry(add_win)
            model_slave.place(x=510,y=170,width=200,height=20)

            Label(add_win,text='Адрес',background='white',foreground='black').place(x=10,y=230)

            adres = ttk.Entry(add_win)
            adres.place(x=10,y=250,width=200,height=20)

            Label(add_win,text='Место',background='white',foreground='black').place(x=260,y=230)

            location = ttk.Entry(add_win)
            location.place(x=260,y=250,width=200,height=20)

            Label(add_win,text='Координаты',background='white',foreground='black').place(x=510,y=230)

            coords = ttk.Entry(add_win)
            coords.place(x=510,y=250,width=200,height=20)

            Label(add_win,text='Номер автомата',background='white',foreground='black').place(x=10,y=310)

            number = ttk.Entry(add_win)
            number.place(x=10,y=330,width=200,height=20)

            Label(add_win,text='Время работы (формат: 08:00 - 22:00)',background='white',foreground='black').place(x=260,y=310)

            time_work = ttk.Entry(add_win)
            time_work.place(x=260,y=330,width=200,height=20)

            Label(add_win,text='Часовой пояс',background='white',foreground='black').place(x=510,y=310)

            timezone_list = [timezone.time_zone for timezone in TimeZone.select()]

            timezone = ttk.Combobox(add_win,values=timezone_list)
            timezone.place(x=510,y=330,width=200,height=20)

            Label(add_win,text='Товарная матрица',background='white',foreground='black').place(x=10,y=390)

            item_matric_list = [item_matric.name for item_matric in Product_matrix.select()]

            item_matric = ttk.Combobox(add_win,values=item_matric_list)
            item_matric.place(x=10,y=410,width=200,height=20)

            Label(add_win,text='Шаблон крит. значений',background='white',foreground='black').place(x=260,y=390)

            pattern_crit = ttk.Combobox(add_win,values=['1','2','3'])
            pattern_crit.place(x=260,y=410,width=200,height=20)

            Label(add_win,text='Шаблон уведомлений',background='white',foreground='black').place(x=510,y=390)

            pattern_sign = ttk.Combobox(add_win,values=['1','2','3'])
            pattern_sign.place(x=510,y=410,width=200,height=20)

            Label(add_win,text='Клиент',background='white',foreground='black').place(x=10,y=470)

            client_list = [client.name for client in Client.select()]

            client = ttk.Combobox(add_win,values=client_list)
            client.place(x=10,y=490,width=200,height=20)

            Label(add_win,text='Менеджер',background='white',foreground='black').place(x=260,y=470)

            manager_list = [manager.name for manager in Manager.select()]

            manager = ttk.Combobox(add_win,values=manager_list)
            manager.place(x=260,y=490,width=200,height=20)

            Label(add_win,text='Инженер',background='white',foreground='black').place(x=510,y=470)

            ingener_list = [ingener.name for ingener in Ingener.select()]

            ingener = ttk.Combobox(add_win,values=ingener_list)
            ingener.place(x=510,y=490,width=200,height=20)

            Label(add_win,text='Техник-оператор',background='white',foreground='black').place(x=10,y=550)

            op_list = [op.name for op in Operator.select()]

            tech_op = ttk.Combobox(add_win,values=op_list)
            tech_op.place(x=10,y=570,width=200,height=20)

            Label(add_win,text='Платежные системы',background='white',foreground='black').place(x=260,y=550)
            enabled_m = IntVar()
            enabled_c = IntVar()
            enabled_n = IntVar()
            enabled_q = IntVar()
            system = Frame(add_win,highlightthickness=1,highlightbackground='black')
            system.place(x=260,y=570,width=450,height=21)

            money_pr = ttk.Checkbutton(system,text='Монетопр', variable=enabled_m)
            money_pr.place(x=1,y=0,width=80,height=19)

            cup_pr = ttk.Checkbutton(system,text='Купюропр', variable=enabled_c)
            cup_pr.place(x=81,y=0,width=85,height=19)

            nfc = ttk.Checkbutton(system,text='Модуль б/н оплаты', variable=enabled_n)
            nfc.place(x=166,y=0,width=140,height=19)

            qr = ttk.Checkbutton(system,text='QR - платежи', variable=enabled_q)
            qr.place(x=306,y=0,width=100,height=19)

            Label(add_win,text='RFID карты обслуживания',background='white',foreground='black').place(x=10,y=630)

            rfid_ob = ttk.Entry(add_win)
            rfid_ob.place(x=10,y=650,width=200,height=20)

            Label(add_win,text='RFID карты инкассации ',background='white',foreground='black').place(x=260,y=630)

            rfid_inc = ttk.Entry(add_win)
            rfid_inc.place(x=260,y=650,width=200,height=20)

            Label(add_win,text='RFID карты загрузки',background='white',foreground='black').place(x=510,y=630)

            rfid_dow = ttk.Entry(add_win)
            rfid_dow.place(x=510,y=650,width=200,height=20)

            Label(add_win,text='id кассы Kit online\n(только в случае жесткой привязки)',background='white',foreground='black').place(x=10,y=695)

            id_casse = ttk.Entry(add_win)
            id_casse.place(x=10,y=730,width=200,height=20)

            Label(add_win,text='Приоритет обслуживания ',background='white',foreground='black').place(x=260,y=710)

            priority_list = [pr.name for pr in Priority.select()]

            prior = ttk.Combobox(add_win,values=priority_list)
            prior.place(x=260,y=730,width=200,height=20)

            Label(add_win,text='Модем',background='white',foreground='black').place(x=510,y=710)

            modem = ttk.Entry(add_win)
            modem.place(x=510,y=730,width=200,height=20)


            def data(event):
                nonlocal add_win, enabled_c, enabled_m, enabled_n, enabled_q
                children = dict(add_win.children)
                entrys = {}
                for name, widget in children.items():
                    if name.startswith('!entry') or isinstance(widget, (ttk.Entry, Entry)):
                        entrys[name] = widget.get()

                entrys['монетопр'] = enabled_m.get()
                entrys['купюроп'] = enabled_c.get()
                entrys['б/н оплата'] = enabled_n.get()
                entrys['qr'] = enabled_q.get()
                firma_name = Firma.get(Firma.name == entrys['!combobox'])
                model_name = Model.get(Model.name == entrys['!combobox2'])
                type_work_name=Type_work.get(Type_work.name==entrys['!combobox3'])
                time_zone_name = TimeZone.get(TimeZone.time_zone == entrys['!combobox4'])
                matrix_name = Product_matrix.get(Product_matrix.name==entrys['!combobox5'])
                client_name = Client.get(Client.name==entrys['!combobox8'])
                manager_name = Manager.get(Manager.name==entrys['!combobox9'])
                ingener_name = Ingener.get(Ingener.name==entrys['!combobox10'])
                operator_name = Operator.get(Operator.name==entrys['!combobox11'])
                casse_name=Casse.create(id=entrys['!entry9'])
                type_pay = Type_apparat_pay.create(mo=entrys['монетопр'],cu=entrys['купюроп'],be=entrys['б/н оплата'],qr=entrys['qr'])
                pri = Priority.get(Priority.name==entrys['!combobox12'])
                status = Status_apparate.get(Status_apparate.name == 'рабоатает')
                
                try:
                    Vendigovskiy_apparats.create(
                        name=entrys['!entry'],
                        firma=firma_name,
                        model=model_name,
                        type_work=type_work_name,
                        adres=entrys["!entry4"],
                        location=entrys['!entry5'],
                        coords=entrys['!entry6'],
                        number_ser=entrys['!entry7'],
                        time_work = entrys['!entry8'],
                        time_zone = time_zone_name,
                        matrix = matrix_name,
                        crit_znac = entrys['!combobox6'],
                        sign = entrys['!combobox7'],
                        client=client_name,
                        manager=manager_name,
                        ingener=ingener_name,
                        op=operator_name,
                        type_pay = type_pay,
                        rfid_dow=1,
                        rfid_ob=1,
                        rfid_inc=1,
                        casse=casse_name,
                        priority=pri,
                        modem=entrys['!entry13'],
                        status=status,
                        action=Action.create(edit=True,block=True,delete=True),
                        date_input_system=datetime.datetime.now(),
                        company='Нет компании'
                        )
                except Exception as e:
                    showerror(title="Добавление ТА", message="Произошла ошибка")  
                showinfo(title="Добавление ТА", message='Успешно добавлен новый ТА')
                add_win.destroy()
                draw_tree()
                
            add_buttonTA = Button(add_win,background='white',text='Создать')
            add_buttonTA.place(x=330,y=850)
            add_buttonTA.bind('<Button-1>',data)


        def export_VA():
            ta = []
            for ap in Vendigovskiy_apparats.select():
                ta.append(ap.__data__)
            with open('TA.csv', 'w', encoding='utf-8') as file:
                for i in ta:
                    res = ''
                    for v in i:
                        res+=str(i[v])+','
                    file.write(res+"\n")
                

        add_button = Button(frame_under_label,background='white',text='Добавить',command=add_VA)
        add_button.place(x=(1920-480)//2-100,y=5)
        export_button = Button(frame_under_label,background='white',text='Экспорт',command=export_VA)
        export_button.place(x=(1920-480)//2-100,y=40)
        total_avtomat = Vendigovskiy_apparats.select().order_by(Vendigovskiy_apparats.id.desc()).get()
        Label(frame_under_label,text=f'Всего найдено {total_avtomat} шт.',bg='#F7F7F7').place(x=20,y=40)

        frame_hat = Frame(canvas_admin,bg='white',width=(1920-480)//2-2,height=75)
        frame_hat.place(x=0,y=80)

        

        def claim_filter():
            global tree
            count = None
            filt = None
            try: 
                count = int(count_rows.get().lstrip()) if count_rows.get().lstrip() else None
            except ValueError:
                print("Значение должно быть числом")
            filt = filter.get().lstrip() if filter.get().lstrip() else None
            tree.destroy()

            draw_tree(count=count,filter=filt)

        Label(frame_hat,text='Показать',bg='white',foreground='black').place(x=5,y=30)
        
        count_rows = Entry(frame_hat)
        count_rows.place(x=75,y=30,width=50,height=20)

        Label(frame_hat,text='записей',bg='white',foreground='black').place(x=140,y=30)
        
        pokazat = Button(frame_hat,text='Применить',command=claim_filter)
        pokazat.place(x=600,y=30)

        filter = Entry(frame_hat)
        filter.place(x=275,y=25,width=150,height=30)


        def draw_tree(count=None,filter=None):
            global tree
            avtomat = []

            for appar in Vendigovskiy_apparats.select():

                actions = []
                edit = appar.action.__data__['edit']
                block = appar.action.__data__['block']
                delete = appar.action.__data__['delete']
                if edit:
                    actions.append('edit')
                if block:
                    actions.append('block')
                if delete:
                    actions.append('delete')    
                
                avtomat.append((appar.id,appar.name,appar.model,appar.company,appar.modem,appar.location,appar.date_input_pretpri9tie,actions))
            
            columns = ('ID','Название автоматов','Модель','Компания','Модем','Адрес/Место','В работе с','Действие')
            
            tree = ttk.Treeview(canvas_admin,columns=columns, show="headings")
            tree.place(x=5,y=160,height=1080-115)

            def sort(col, reverse):
                l = [(tree.set(k, col), k) for k in tree.get_children("")]
                l.sort(reverse=reverse)
                for index,  (_, k) in enumerate(l):
                    tree.move(k, "", index)
                tree.heading(col, command=lambda: sort(col, not reverse))

            tree.heading("ID", text="ID", command=lambda: sort(0, False))
            tree.column("ID",width=15)
            tree.heading("Название автоматов", text="Название автоматов", command=lambda: sort(1, False))
            tree.column("Название автоматов",width=130)
            tree.heading("Модель", text="Модель", command=lambda: sort(2, False))
            tree.column("Модель",width=55)
            tree.heading("Компания", text="Компания", command=lambda: sort(3, False))
            tree.column("Компания",width=80)
            tree.heading("Модем", text="Модем", command=lambda: sort(4, False))
            tree.column("Модем",width=100)
            tree.heading("Адрес/Место", text="Адрес/Место", command=lambda: sort(5, False))
            tree.column("Адрес/Место",width=90)
            tree.heading("В работе с", text="В работе с", command=lambda: sort(6, False))
            tree.column("В работе с",width=130)
            tree.heading("Действие", text="Действие", command=lambda: sort(7, False))
            tree.column("Действие",width=110)

            if filter:
                av = []
                for i in range(len(avtomat)):
                    if filter.lower() in avtomat[i][1].lower():
                        av.append(avtomat[i])
                    else:
                        continue
                avtomat = av[:]
            
            avtomat = avtomat[:count]

            s = ttk.Style()
            s.configure('Treeview', rowheight=40) 

            for a in avtomat:
                tree.insert('',END,values=a)
            

        draw_tree()


        

Pattenr.main()

img_mon = PIL.Image.open('i.png')
img_mon = img_lupa.resize((50,50))
photo_mon = PIL.ImageTk.PhotoImage(img_lupa)

button_mon_ta = Button(frame_left_side,image=photo_mon,text="Монитор ТА",background='#142733',compound=LEFT,foreground="White",font=(...,22),anchor="w")
button_mon_ta.place(x=5,y=105,width=1920//4,height=50)

img_det = PIL.Image.open('i.png')
img_det = img_lupa.resize((50,50))
photo_det = PIL.ImageTk.PhotoImage(img_lupa)

button_det_ot = Button(frame_left_side,image=photo_mon,text="Детальные отчеты",background='#142733',compound=LEFT,foreground="White",font=(...,22),anchor="w")
button_det_ot.place(x=5,y=155,width=1920//4,height=50)

button_det_ot = Button(frame_left_side,image=photo_mon,text="Учет ТМЦ",background='#142733',compound=LEFT,foreground="White",font=(...,22),anchor="w")
button_det_ot.place(x=5,y=205,width=1920//4,height=50)

button_det_ot = Button(frame_left_side,image=photo_mon,text="Администрирование",background='#142733',compound=LEFT,foreground="White",font=(...,22),anchor="w")
button_det_ot.place(x=5,y=255,width=1920//4,height=50)

def switch(event):
    global canvas_right_side
    canvas_right_side.destroy()
    canvas_right_side = Canvas(root)
    canvas_right_side.place(x=480,y=50,width=1920-480,height=1080-115)

    Label(canvas_right_side,text='ООО Торговые автоматы',background='#142733',foreground='white',font=(...,22),anchor=W).place(x=5,y=5,width=1920-480, height=50)
    
    button = event.widget.cget('text')
    if button == "Главная":
        Pattenr.main()
    if button == "Администрирование":
        Pattenr.admin()

button_main.bind('<Button-1>',switch)
button_mon_ta.bind('<Button-1>',switch)
button_det_ot.bind('<Button-1>',switch)
root.mainloop()