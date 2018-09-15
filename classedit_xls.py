# coding=utf-8

import xlrd  #编辑xls
import time  #时间戳相关
import datetime  #Datetime相关
import random  #生成随机数
import string  #生成随机UID相关
import re  #多字符分割字符相关
import os
import codecs

DELIMITER_0 = "◇|\n"
DELIMITER_1 = "◇"  #用于各个部分的分割
DELIMITER_2 = "("  #分割周数与课程节次
DELIMITER_3 = ","
#分割课程节次（然并卵），主要是用于分析单个Slice有几个周区间
DELIMITER_4 = "-|,"  #分割周区间
#规定分割课表的几个常量，可以根据课表格式更改
#分割格式示例：大学英语◇1-16(1,2节)◇教1-137◇教师名

DELIMITER_5 = "("
DELIMITER_6 = "："
#分割班级名


UID = "1234567890abcdefghijklmnopqrstuvwxyz\
ABCDEFGHIJKLMNOPQRSTUVWXYZ!@#$%^&*"
#UID备选列表

def begin_time():
	ver = 0
	while ver == 0:
	#循环检查输入是否有误，ver为1为有误，1为正确
		ver = 1

		try:
			time = input ()
			date_time = datetime.datetime.strptime(time, "%Y-%m-%d-%H-%M")
			#输入日期并转换成datetime

		except:
			print ("\n输入有误，请重新输入：\n")
			ver = 0
	return date_time
#获取时间并转化成datetime

def time_verification(date_time, num):
	while date_time - start_list[num] < datetime.timedelta(minutes = 1):
		print ("\n输入时间早于课程开始时间，请检查并重新输入：\n")
		
		time = input ()
		date_time = datetime.datetime.strptime(time, "%Y-%m-%d-%H-%M")

	return date_time
#验证时间早晚

start_list = [i for i in range(0, 13)]
#课程开始时间list
end_list = [i for i in range(0, 13)]
#课程结束时间list

print ("\n请输入第一周星期一上午第一节课上课日期和时间\n")
print ("（无论第一节有没有课），\n")
print ("格式为「年-月-日-时-分」（24小时制，不足两位请补0），\n")
print ("例如：2001-01-01-09-59。\n")
print ("请输入：\n")
#start_list[1] = begin_time()
start_list[1] = datetime.datetime.strptime("2018-09-10-08-30", "%Y-%m-%d-%H-%M")

print ("\n好的！下面再输入星期一下午第一节课的上课日期和时间，\n")
print ("也就是第五节课，\n")
print ("格式相同。\n")
#start_list[5] = time_verification(begin_time(), 1)
start_list[5] = datetime.datetime.strptime("2018-09-10-13-40", "%Y-%m-%d-%H-%M")

print ("\n最后，再输入星期一晚上第一节课的上课日期和时间，\n")
print ("我没记错的话，应该就是第九节课，\n")
print ("格式依然相同。\n")
#start_list[9] = time_verification(begin_time(), 5)
start_list[9] = datetime.datetime.strptime("2018-09-10-18-20", "%Y-%m-%d-%H-%M")

print("\n好的，请稍等……\n")


def plus_60(time):
	time_after = time + datetime.timedelta(minutes = 60)
	return time_after

def plus_50(time):
	time_after = time + datetime.timedelta(minutes = 50)
	return time_after

def plus_45(time):
	time_after = time + datetime.timedelta(minutes = 45)
	return time_after

def plus_day(time, day):
	time_after = time + datetime.timedelta(days = day)
	return time_after

def plus_week(time, week):
	time_after = time + datetime.timedelta(weeks = week)
	return time_after


for i in range(0, 3):
	start_list[2+4*i] = plus_50(start_list[1+4*i])
	start_list[3+4*i] = plus_60(start_list[2+4*i])
	start_list[4+4*i] = plus_50(start_list[3+4*i])
	for l in range(1,5):
		end_list[l+4*i] = plus_45(start_list[l+4*i])
#推算每节课的时间


def uid_born():
        uid_list = []
        for i in range(0,20):
                uid_list.append(random.choice(UID))
                uid = "".join(uid_list)
        return uid
#随机生成UID


def classedit_xls(data_slice_1, y, x):		
	global write_text
	#引入全局变量 write_text

	week_list = [0,"MO", "TU", "WE", "TH", "FR", "SA", "SU"]

	print (list(data_slice_1))

	name = data_slice_1[0]
	name = " ".join(name.split())  #去掉课程名字前的空格
	week = week_list[x-1]		
	ver_2 = 1
	ver_3 = 1
	try:
		location = data_slice_1[2]
	except:
		ver_2 = 0
	try:
		description = "教师：" + data_slice_1[3]
	except:
		ver_3 = 0
	#验证是否有地点和教师

	data_slice_2 = data_slice_1[1].split(DELIMITER_2)
		
	loop = data_slice_1[1].count(DELIMITER_3)
	for i in range(0, loop):
		data_slice_3 = re.split(DELIMITER_4, data_slice_2[0])
			
		start_week = int(data_slice_3[0+2*i]) - 1
		duration_week = int(data_slice_3[1+2*i]) - start_week
		
		start_lesson = plus_week(start_list[y-2], start_week)
		start_lesson = plus_day(start_lesson, x-2)
		end_lesson = plus_45(start_lesson)
		start_lesson = start_lesson.strftime("%Y%m%dT%H%M%S")
		end_lesson = end_lesson.strftime("%Y%m%dT%H%M%S")

		write_text.append("BEGIN:VEVENT")
		write_text.append("UID:" + uid_born() + "@github.com/smilonely")
		write_text.append("DTSTART;TZID=Asia/Shanghai:" + start_lesson)
		write_text.append("DTEND;TZID=Asia/Shanghai:0" + end_lesson)
		write_text.append("RRULE:FREQ=WEEKLY;WKST=SU;COUNT=" + \
			str(duration_week) + ";BYDAY=" + week)
		if ver_2 == 1:
			write_text.append("LOCATION:" + location)
		if ver_3 == 1:
			write_text.append("DESCRIPTION:" + description)
		write_text.append("STATUS:CONFIRMED")
		write_text.append("SUMMARY:" + name)
		write_text.append("TRANSP:OPAQUE")
		write_text.append("END:VEVENT\n")
#添加一个EVENT的内容进list write_text，但是不合并


data_raw = xlrd.open_workbook("1.xls")
table = data_raw.sheets()[0]
class_name = table.cell(1, 0).value
class_name = class_name.split(DELIMITER_5)
class_name = class_name[0].split(DELIMITER_6)
class_name = class_name[1]
semester = table.cell(1, 7).value
#找到班级和学期名字

new_ics = codecs.open(class_name + "课程表.ics", "w","utf-8")
new_ics.write(
"BEGIN:VCALENDAR\n"
"VERSION:2.0\n"
"PRODID:-//DANGEL//Class Schedule//CN\n"
"NAME:" + semester + "课程表\n"
"X-WR-CALNAME:" + semester + "课程表\n"
"DESCRIPTION:" + class_name + "班" + semester + "课程表\n"
"X-WR-CALDESC:" + class_name + "班" + semester + "课程表\n"
"CALSCALE:GREGORIAN\n"
"METHOD:PUBLISH\n"
"X-WR-TIMEZONE:Asia/Shanghai\n"
"BEGIN:VTIMEZONE\n"
"TZID:Asia/Shanghai\n"
"X-LIC-LOCATION:Asia/Shanghai\n"
"BEGIN:STANDARD\n"
"TZOFFSETFROM:+0800\n"
"TZOFFSETTO:+0800\n"
"TZNAME:CST\n"
"DTSTART:19700101T000000\n"
"END:STANDARD\n"
"END:VTIMEZONE)\n")
#写入各项信息

for y in range(3, 9):
	for x in range(2, 9):
		number = (table.cell(y, x).value).count(DELIMITER_1)
		#数一数分隔符
		data = table.cell(y, x).value
		data_slice = re.split(DELIMITER_0, data)
		write_text = []
		
		if number <= 3 and number > 0:
			classedit_xls(data_slice, y, x)
			write_done = "\n".join(write_text)
			new_ics.write(write_done)
			#直接将一个EVENT合并并写入

		if number > 3:
			j = number//3

			for k in range(0, j):
				data_slice_0 = data_slice[0+k*j:4+k*j]
				classedit_xls(data_slice_0, y, x)

			write_done = "\n".join(write_text)
			new_ics.write(write_done)
			#将多个EVENT合并并写入
			
		write_text = ["\n"]
		#初始化变量以重复写入

		if number == 0:
			break
#三重循环，最为致命（雾）。三个循环来遍历单元格

new_ics.write(u"END:VCALENDAR")
new_ics.close()

print ("\n完成了！\n")
input()
