import os
import time
import random
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from PIL import Image

def get_phone_info():
	print ('check devices')
	print (os.popen("adb devices").read())
	print ('screen:')
	print (os.popen('adb shell wm size').read())
	print ('density:')
	print (os.popen('adb shell wm density').read())
	print ('ddetail:')
	print (os.popen('adb shell getprop ro.product.device').read())
	print ('os:')
	print (os.popen('adb shell getprop ro.build.version.release').read())

def pull_screenshot():
	print ('screencap')
	os.system('adb shell screencap -p /sdcard/autojump.png')
	print('get png')
	os.system('adb pull /sdcard/autojump.png .')
	
def jump(distance):
    press_time = distance * 1.35
    press_time = int(press_time)
    x1=740+random.randint(-20,20)
    y1=1500+random.randint(-20,20)
    x2=750+random.randint(-20,20)
    y2=1510+random.randint(-20,20)
    cmd = 'adb shell input swipe {} {} {} {} '.format(x1,y1,x2,y2) + str(press_time)
    print(cmd)
    os.system(cmd)	

cord=[]
update = True
def updatefig(*args):
	global update
	global im
	if update:
		pull_screenshot()
		img=np.array(Image.open('autojump.png'))
		im = plt.imshow(img, animated=True)
		update = False
	return im,
    
def on_click(event):
	global cord
	global update
	cor = (event.xdata,event.ydata)
	cord.append(cor)
	if len(cord)==2:
		cord1=cord.pop()
		cord2=cord.pop()
		distance = ((cord1[0]-cord2[0])**2+(cord1[1]-cord2[1])**2)**0.5
		print (distance)
		jump(distance)
		time.sleep(0.5)
		update=True
		
def on_key_press(event):
	global update
	print ('get key {}'.format(event.key))
	cord.clear()
	if event.key == 'r':
		update=True	
	
get_phone_info()
fig = plt.figure()
fig.canvas.mpl_connect('button_press_event', on_click)
fig.canvas.mpl_connect('key_press_event', on_key_press)
ani = animation.FuncAnimation(fig, updatefig, interval=50, blit=True)
plt.show()
