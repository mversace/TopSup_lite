# -*- coding: utf-8 -*-
import win32gui
import time
from PIL import ImageGrab
from PIL import Image
from common import ocr, methods
from threading import Thread
"""
hWndList = []
win32gui.EnumWindows(lambda hWnd, param:param.append(hWnd), hWndList)
for i in hWndList:
    title = win32gui.GetWindowText(i)
    clsName = win32gui.GetClassName(i)
    if ('腾讯' in title):
        print(title, clsName)
"""

#切割图片，取出问题与选项图片
#腾讯手游助手模拟器--冲顶大会
def TryAnalyseImgCD(img):
    #返回图片列表
    imgList = {}
    #查找问题区域、选项区域
    yPox = []
    pixData = img.load()
    w, h = img.size

    #题目开始的高度
    top = 250
    
    #题目区域left和right
    left = 30
    right = 700
    
    #查找选项区域，关键像素为横线196，196，196
    red = 196
    green = 196
    blue = 196
    for y in range(h):
        find = True
        for i in range(w):
            if (i < w / 2 - 50 or i > w / 2 + 50):
                continue
            if (pixData[i, y][0] != red and pixData[i, y][1] != green and pixData[i, y][2] != blue):
                find = False
                break
            if (y < h-1 and pixData[i, y + 1][0] != red and pixData[i, y + 1][1] != green and pixData[i, y + 1][2] != blue):
                find = False
                break
        if find:
            yPox.append(y)
    
    if (len(yPox) == 0):
        return
    
    q = img.crop((left,top,right,yPox[0]))
    imgList['q'] = q;
    #q.save('C:\\Users\\44780\\Desktop\\q.png', 'png')

    #选项
    choice = []
    for i in range(len(yPox)):
        if i % 2 == 0:
            x = img.crop((left,yPox[i]+2,right,yPox[i+1]))
            choice.append(x)
            #x.save('C:\\Users\\44780\\Desktop\\r%d.png'%i, 'png')
    imgList['c'] = choice
    #print("图片截取分割成功")
    return imgList

# 获取腾讯模拟器截图，并分析
# 模拟器分辨率-1280*720，DPI-320
def TryTencent():
    hWin = win32gui.FindWindow("TXGuiFoundation", "腾讯手游助手【标准引擎】")
    if hWin:
        #t1 = time.clock()
        print("搜索到腾讯模拟器......")
        l,t,r,b = win32gui.GetWindowRect(hWin)
        img = ImageGrab.grab((l,t,r,b))
        #img = img.crop((l,t,r,b))
        #img.save('C:\\Users\\44780\\Desktop\\t.png', 'png')
        #t2 = time.clock()
        #print("截取模拟器截图耗时:", t2-t1)
        imgList = TryAnalyseImgCD(img)
        if (imgList is None or len(imgList) < 2):
            print("没有到答题时间或者查不到关键像素")
            return
        #t3 = time.clock()
        #print("图片裁剪耗时:", t3-t2)
        question, choices = ocr.ocr_img(imgList)
        print('Question: '+question)
        if ('不是' in question) or ('不属于' in question) or ('不包含' in question) or ('不可能' in question):
            print('*****请注意此题为否定题*****')

        #t4 = time.clock()
        #print("图片识别耗时:", t4-t3)
        # 将问题与选项一起搜索方法，并获取搜索到的结果数目
        m0 = Thread(methods.run_algorithm(0, question, choices))
        m1 = Thread(methods.run_algorithm(1, question, choices))
        # 用选项在问题页面中计数出现词频方法
        m2 = Thread(methods.run_algorithm(2, question, choices))
        m0.start()
        m1.start()
        m2.start()

while True:
    t = time.clock()
    TryTencent()
    end_time = time.clock()
    print("搜索耗时: ",end_time - t)
    go = input('\n输入回车继续运行,输入 n 回车结束运行: ')
    if go == 'n':
        break

    print('------------------------')
