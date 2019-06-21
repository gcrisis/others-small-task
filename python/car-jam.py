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
winx = 200
winy = 100
winwidth=500
winheight=300
top.geometry('{}x{}+{}+{}'.format(winwidth,winheight,winx,winy))

var1=Tkinter.StringVar()
var2=Tkinter.StringVar()
var3=Tkinter.StringVar()
var4=Tkinter.StringVar()
var5=Tkinter.StringVar()
var6=Tkinter.StringVar()
var7=Tkinter.StringVar()
var8=Tkinter.StringVar()


class car:
    def __init__(self,tk,delay,bg='red',fg='white'):
        self.delay=delay
        self.var=Tkinter.StringVar()
        self.btn = Tkinter.Button(tk,textvariable=self.var,bg=bg,fg=fg)

    def run(self,before):
        time.sleep(self.delay)
        dt_res=0.04
        step = 2
        cnt=0 
        flag=1
        x1=0
        y1=0
        while 1:
            deltax = before.btn.winfo_rootx()-self.btn.winfo_rootx()
            deltay = before.btn.winfo_rooty()-self.btn.winfo_rooty()
        
            if (abs(deltax)+abs(deltay))<40 and \
                ((abs(flag)==1 and flag*deltax>0) or (abs(flag)==2 and flag*deltay>0)):
                dt = 0.1
                self.var.set('{}'.format('xx'))
            else:
                dt = dt_res
                self.var.set('{}'.format(int(step/dt)))
            if flag==1:
                x1+=step
                if x1>winwidth-50:
                    flag=2
            elif flag==2:
                y1+=step
                if y1>winheight-100:
                    flag=-1
            elif flag==-1:
                x1-=step
                if x1<25:
                    flag=-2
            elif flag==-2:
                y1-=step
                if y1<25:
                    flag=1
        
            if cnt>=(5//dt_res):
                dt_res=random.uniform(0.02,0.1)
                print dt_res
                cnt=0
            cnt+=1

            self.btn.place(x=x1,y=y1)
            time.sleep(dt)
        #endof while
    #endof car_run



def add_btn_handle(): 
    thread.start_new_thread(car(top,0,).run,(b,))
#实例化功能按钮
btn_add = Tkinter.Button(top,text='add',bg='Indigo',command=add_btn_handle)
btn_del = Tkinter.Button(top,text='del',bg='Indigo',)

btn_add.place(x=winwidth-100,y=winheight-50)
btn_del.place(x=winwidth-50,y=winheight-50)
#实例化car
btn1 = Tkinter.Button(top,textvariable=var1,bg='red',)
btn2 = Tkinter.Button(top,textvariable=var2,bg='green',)
btn3 = Tkinter.Button(top,textvariable=var3,bg='blue',)
btn4 = Tkinter.Button(top,textvariable=var4,bg='cyan',fg='black')
btn5 = Tkinter.Button(top,textvariable=var5,bg='yellow',fg='black')
btn6 = Tkinter.Button(top,textvariable=var6,bg='purple',)
btn7 = Tkinter.Button(top,textvariable=var7,bg='orange',fg='black')
btn8 = Tkinter.Button(top,textvariable=var8,bg='Violet',fg='black')

a=car(top,0,)
b=car(top,4,)
thread.start_new_thread(a.run,(b,))
thread.start_new_thread(b.run,(a,))
'''
thread.start_new_thread(car_run,(0,0,btn2,1,2,btn1,var2))
thread.start_new_thread(car_run,(0,0,btn3,2,2,btn2,var3))
thread.start_new_thread(car_run,(0,0,btn4,3,2,btn3,var4))
thread.start_new_thread(car_run,(0,0,btn5,4,2,btn4,var5))
thread.start_new_thread(car_run,(0,0,btn6,5,2,btn5,var6))
thread.start_new_thread(car_run,(0,0,btn7,6,2,btn6,var7))
thread.start_new_thread(car_run,(0,0,btn8,7,2,btn7,var8))
'''
top.mainloop()