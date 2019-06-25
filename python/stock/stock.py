#!/usr/bin/python3

#-*-coding=utf-8-*-

import requests
import os
import re

import datetime
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import matplotlib
from matplotlib.widgets import Button
from matplotlib.widgets import TextBox
from matplotlib.widgets import RadioButtons
import pandas as pd
from matplotlib.dates import MONDAY, DateFormatter, DayLocator, WeekdayLocator

from mpl_finance import candlestick_ohlc    

#import zh font
zhfont = matplotlib.font_manager.FontProperties(fname='./fonts/msyh.ttf')

#global var
get_str=''
stock_code=''
data_path='./data/'
fig, ax = plt.subplots()


def get_stock_name(stock_code):
	if stock_code=='':
		return
	url='http://hq.sinajs.cn/list={}'.format(stock_code)
	req = requests.request('GET',url)
	str1=req.text.split('="',1)[1]
	if len(str1)<5:
		print('get stock details failed')
		return
	str1=str1.split(',')[0]
	print ('get stock name:'+str1)
	return str1
	
def get_stock_data(stock_code,scale=240,datalen=30,mode='w',header=True):
	dic={}
	if stock_code=='':
		return False
	url='http://money.finance.sina.com.cn/quotes_service/api/json_v2.php/CN_MarketData.getKLineData?symbol={}&scale={}&datalen={}'.format(stock_code,scale,datalen)
	print (url)
	req = requests.request('GET',url)
	if req.text == 'null':
		print('get stock data failed')
		return False
	strlist=req.text.replace('[{','')
	strlist=strlist.replace('}]','')
	strlist=strlist.split('},{')  
	for strl in strlist:
		str1=strl.split(',')
		for s in str1:
			t=s.split(':',1)
			if 	t[0] in dic:
				dic[t[0]].append(t[1].replace('"',''))
			else:
				dic[t[0]]=[t[1].replace('"','')]
	df = pd.DataFrame(dic)
	#print (df)
	df.to_csv(data_path+'{}.csv'.format(stock_code),mode=mode,index=False,header=header)
	print ('write data to file')
	return True

def write_buy_sell_to_file(string):
	if string =='':
		return
	dic={'day':'','buy':'','sell':''}
	str1=re.split(',| ',string)
	for stri in str1:
		if stri=='':
			continue
		if stri[0]=='d':
			dic['day']=stri.replace('d','')
		elif stri[0]=='b':
			dic['buy']=stri.replace('b','')
		elif stri[0]=='s':
			dic['sell']=stri.replace('s','')
		else:
			print ('input error')
			return
	if dic['day']=='':
		dic['day']=datetime.datetime.now().strftime('%Y-%m-%d')
	print (dic)
	df = pd.DataFrame(dic,index=[0])
	if os.path.exists(data_path+'{}-bs.csv'.format(stock_code)):
		df.to_csv(data_path+'{}-bs.csv'.format(stock_code),mode='a',index=False,header=False)
	else:
		df.to_csv(data_path+'{}-bs.csv'.format(stock_code),mode='w',index=False)

def get_data_and_display(stock_code,startdate=(datetime.date.today()-datetime.timedelta(1)).strftime('%Y-%m-%d'),datalen=60):
	global ax
	if stock_code=='':
		return
	if not os.path.exists(data_path+'{}.csv'.format(stock_code)):
		print ('not exists')
		if not get_stock_data(stock_code,datalen=60):
			return
	# plot_day_summary(ax, quotes, ticksize=3)
	print ('read scv {}'.format(stock_code))
	ax.cla()
	ax.set_title(get_stock_name(stock_code),fontproperties=zhfont)
	ax.xaxis.set_major_locator(mondays)
	ax.xaxis.set_minor_locator(alldays)
	ax.xaxis.set_major_formatter(weekFormatter)
	ax.xaxis_date()
	ax.autoscale_view()
	if os.path.exists(data_path+'{}-bs.csv'.format(stock_code)):
		bs = pd.read_csv(data_path+'{}-bs.csv'.format(stock_code),index_col=0,parse_dates=True,infer_datetime_format=True)
		ax.plot(mdates.date2num(bs.index.to_pydatetime()),bs['buy'],'mo')
		ax.plot(mdates.date2num(bs.index.to_pydatetime()),bs['sell'],'c^')
	if os.path.exists(data_path+'{}.csv'.format(stock_code)):
		print ('get csv data')
		quotes = pd.read_csv(data_path+'{}.csv'.format(stock_code),index_col=0,parse_dates=True,infer_datetime_format=True)
		cutlen=len(quotes)
		print('{} {}'.format(quotes.last_valid_index(),startdate))
		quotes = quotes[quotes.index <= startdate]
		cutlen-=len(quotes)
		if (quotes.last_valid_index().strftime('%Y-%m-%d')<startdate or len(quotes)<datalen):
			get_stock_data(stock_code,datalen=datalen+cutlen)
			quotes = pd.read_csv(data_path+'{}.csv'.format(stock_code),index_col=0,parse_dates=True,infer_datetime_format=True)
			quotes = quotes[quotes.index <= startdate]
		#print (quotes.at_time('2019-06-20'))
		quotes = quotes.tail(datalen)
		print(quotes)
		ax.plot(mdates.date2num(quotes.index.to_pydatetime()),quotes['ma_price5'],'k-')
		ax.plot(mdates.date2num(quotes.index.to_pydatetime()),quotes['ma_price10'],'m-')
		ax.plot(mdates.date2num(quotes.index.to_pydatetime()),quotes['ma_price30'],'b-')
		candlestick_ohlc(ax, zip(mdates.date2num(quotes.index.to_pydatetime()),
				                 quotes['open'], quotes['high'],
				                 quotes['low'], quotes['close']),
				         width=0.6,colorup='r', colordown='g')
	else:
		raise

#button
def bdspl_handle(event):
	global stock_code
	lens=60
	date1=(datetime.date.today()-datetime.timedelta(1)).strftime('%Y-%m-%d')
	str1=re.split(',| ',get_str)
	for stri in str1:
		if stri[0:2]=='sh' or stri[0:2]=='sz':
			stock_code=stri
			get_data_and_display(stock_code)
		elif stri[0:3]=='len':			
			lens=int(stri[3:])
		elif stri[0:4]=='date':
			date1=stri[4:]
		else:
			print ('input error')
			return
	get_data_and_display(stock_code,date1,lens)
			

def b_s_handle(event):
	print ('buy-sell')
	write_buy_sell_to_file(get_str)
	get_data_and_display(stock_code)
	#ax.plot(mdates.date2num(datetime.datetime(2019, 5, 22, 0, 0)),30,'bo')

###text###
def submit(text):
	global get_str
	get_str=text



if __name__=='__main__':
	if not os.path.exists(data_path): 
		os.makedirs(data_path)
	if not os.path.exists('setup.txt'): 
		os.mknod('setup.txt')
	f=open('setup.txt','r')
	stock_code=f.readline().strip('\n')
	f.close()

		
	axdspl = plt.axes([0.81, 0.05, 0.1, 0.075])
	bdspl = Button(axdspl, 'stock')
	bdspl.on_clicked(bdspl_handle)
	
	axb_s = plt.axes([0.7, 0.05, 0.1, 0.075])
	bb_s = Button(axb_s, 'buy-sell')
	bb_s.on_clicked(b_s_handle)
		
	axbox = plt.axes([0.1, 0.05, 0.2, 0.075])
	text_box = TextBox(axbox, 'input', initial='')
	text_box.on_submit(submit)
	
	mondays = WeekdayLocator(MONDAY)        # major ticks on the mondays
	alldays = DayLocator()              # minor ticks on the days
	weekFormatter = DateFormatter('%b %d')  # e.g., Jan 12
	dayFormatter = DateFormatter('%d')      # e.g., 12

	# select desired range of dates
	#quotes = quotes[(quotes.index >= date1) & (quotes.index <= date2)]
	fig.subplots_adjust(bottom=0.2)
	#fig.subplots_adjust(left=0.2)

	#display the one last software close 
	get_data_and_display(stock_code)

	plt.setp(plt.gca().get_xticklabels(), rotation=45, horizontalalignment='right')

	plt.show()      

	print ('save setup')
	f=open('setup.txt','w')
	print (stock_code)
	f.write(stock_code)
	f.close()



