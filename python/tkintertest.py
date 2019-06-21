#-*-coding:utf-8 -*-
import Tkinter
import thread
import time
import random

# 实例化
top = Tkinter.Tk()
#窗口名称
top.title('tkinter test')
#窗口尺寸
top.geometry('500x300')

var1=Tkinter.StringVar()
var2=Tkinter.StringVar()
var3=Tkinter.StringVar()
var4=Tkinter.StringVar()
var5=Tkinter.StringVar()
var6=Tkinter.StringVar()
var7=Tkinter.StringVar()
var8=Tkinter.StringVar()
#实例化按钮
btn1 = Tkinter.Button(top,textvariable=var1,bg='red',)
btn2 = Tkinter.Button(top,textvariable=var2,bg='green',)
btn3 = Tkinter.Button(top,textvariable=var3,bg='blue',)
btn4 = Tkinter.Button(top,textvariable=var4,bg='cyan',fg='black')
btn5 = Tkinter.Button(top,textvariable=var5,bg='yellow',fg='black')
btn6 = Tkinter.Button(top,textvariable=var6,bg='purple',)
btn7 = Tkinter.Button(top,textvariable=var7,bg='orange',fg='black')
btn8 = Tkinter.Button(top,textvariable=var8,bg='Violet',fg='black')

def car_run(x1,y1,button,delay,speed,before,var):
    time.sleep(delay)
    dt_res=0.04
    step = 2
    cnt=0 
    flag=0; 
    while 1:
        deltax = before.winfo_rootx()-button.winfo_rootx()
        deltay = before.winfo_rooty()-button.winfo_rooty()
       
        if (abs(deltax)+abs(deltay))<40:
            dt = 0.1
            var.set('{}'.format('xx'))
        else:
            dt = dt_res
            var.set('{}'.format(int(step/dt)))
        if flag==0:
            x1+=step
            if x1>450:
                flag=1
        elif flag==1:
            y1+=step
            if y1>250:
                flag=2
        elif flag==2:
            x1-=step
            if x1<25:
                flag=3
        elif flag==3:
            y1-=step
            if y1<25:
                flag=0
    
        if cnt>=(5//dt_res):
            dt_res=random.uniform(0.02,0.1)
            print dt_res
            cnt=0
        cnt+=1

        button.place(x=x1,y=y1)
        time.sleep(dt)
    #endof while
#endof car_run
thread.start_new_thread(car_run,(0,0,btn1,0,2,btn8,var1))
thread.start_new_thread(car_run,(0,0,btn2,1,2,btn1,var2))
thread.start_new_thread(car_run,(0,0,btn3,2,2,btn2,var3))
thread.start_new_thread(car_run,(0,0,btn4,3,2,btn3,var4))
thread.start_new_thread(car_run,(0,0,btn5,4,2,btn4,var5))
thread.start_new_thread(car_run,(0,0,btn6,5,2,btn5,var6))
thread.start_new_thread(car_run,(0,0,btn7,6,2,btn6,var7))
thread.start_new_thread(car_run,(0,0,btn8,7,2,btn7,var8))
top.mainloop()