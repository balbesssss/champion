from tkinter import * 
import PIL.Image
import PIL.ImageTk
from db import Vendigovskiy_apparats, Status_apparate

root = Tk()
root.geometry('1920x1080')

frame_for_hat = Frame(root,background='white',width=1920-150,height=50)
frame_for_hat.place(x=0,y=0)

frame_auth = Button(root,background='white' ,width=150)
frame_auth.place(x=1920-150+2,y=0,height=50)

select = False

def auth(event):
    global select, auth_canvas
    if not select:

        auth_canvas = Canvas(root, width=150,height=200,background="white")
        auth_canvas.place(x=1920-150+2,y=60)

        but_profile = Button(auth_canvas,background="white",text="Мой профиль")
        but_profile.place(x=0,y=25,width=150,height=50)

        but_session = Button(auth_canvas,background="white",text="Мои сессии")
        but_session.place(x=0,y=75,width=150,height=50)

        but_exit = Button(auth_canvas,background="white",text="Выход")
        but_exit.place(x=0,y=125,width=150,height=50)

        select = True
    else:
        auth_canvas.destroy()
        select = False
        

frame_auth.bind("<Button-1>",auth)

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

canvas_right_side = Canvas(root,background='gray')
canvas_right_side.place(x=480,y=50,width=1920-480,height=1080-115)

Label(canvas_right_side,text='ООО Торговые автоматы',background='#142733',foreground='white',font=(...,22),anchor=W).place(x=5,y=5,width=1920-480, height=50)

Label(canvas_right_side,text='Личный кабинет. Главная',background='gray',foreground='black',font=(...,22),anchor=W).place(x=45,y=100,width=350, height=50)

effe_network = Frame(canvas_right_side,background='white',width=(1920-480)//3-50, height=200)
effe_network.place(x=70,y=200)

working_apparat = 0
all_ven_app = 0
stat_work = Status_apparate.get(Status_apparate.name == "рабоатает")

for apparat in Vendigovskiy_apparats.select():
    if apparat.status == stat_work:
        working_apparat+=1
    all_ven_app = apparat.id

label_for_effe = Label(effe_network, text=f"Работающих автоматов {(working_apparat/all_ven_app)*100}",foreground='black',background="white",font=(...,11))
label_for_effe.place(x=120,y=170,width=225,height=15)

Label(effe_network,text="Эффективность сети",background='gray',foreground='black',font=(...,18),anchor=W).place(x=5,y=5,width=(1920-480)//3-65, height=50)

status_network = Frame(canvas_right_side,background='white',width=(1920-480)//3-50, height=200)
status_network.place(x=535,y=200)

Label(status_network,text="Состояние сети",background='gray',foreground='black',font=(...,18),anchor=W).place(x=5,y=5,width=(1920-480)//3-65, height=50)

info = Frame(canvas_right_side,background='white',width=(1920-480)//3-50, height=200)
info.place(x=535+460,y=200)

Label(info,text="Сводка",background='gray',foreground='black',font=(...,18),anchor=W).place(x=5,y=5,width=(1920-480)//3-65, height=50)

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

Label(news,text="Новости",background='gray',foreground='black',font=(...,18),anchor=W).place(x=5,y=5,width=(1920-480)//3-65, height=50)

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

root.mainloop()