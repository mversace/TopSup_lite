# -*- coding: utf-8 -*-

# @Author  : Skye
# @Time    : 2018/1/9 19:34
# @desc    :

from PIL import Image
import pytesseract

# 二值化算法,大于给定像素的设置为白色
def binarizing(img,threshold):
    pixdata = img.load()
    w, h = img.size
    for y in range(h):
        for x in range(w):
            if pixdata[x, y] < threshold:
                pixdata[x, y] = 0
            else:
                pixdata[x, y] = 255
    return img


# 去除干扰线算法
def depoint(img):   #input: gray image
    pixdata = img.load()
    w,h = img.size
    for y in range(1,h-1):
        for x in range(1,w-1):
            count = 0
            if pixdata[x,y-1][0] > 245 and pixdata[x,y-1][1] > 245 and pixdata[x,y-1][2] > 245:
                count = count + 1
            if pixdata[x,y+1][0] > 245 and pixdata[x,y+1][1] > 245 and pixdata[x,y+1][2] > 245:
                count = count + 1
            if pixdata[x-1,y][0] > 245 and pixdata[x-1,y][1] > 245 and pixdata[x-1,y][2] > 245:
                count = count + 1
            if pixdata[x+1,y][0] > 245 and pixdata[x+1,y][1] > 245 and pixdata[x+1,y][2] > 245:
                count = count + 1
            if count > 2:
                pixdata[x,y] = 255
    return img

def ocr_img(imageList):
    question_im = imageList['q']
    choices_im = imageList['c']

    # 转化为灰度图
    # 把图片变成二值图像。
    question_im = question_im.convert('L')
    question_im = binarizing(question_im, 190)
    
    for i in range(len(choices_im)):
        choices_im[i] = choices_im[i].convert('L')
        choices_im[i] = binarizing(choices_im[i], 190)


    # tesseract 路径
    pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files (x86)\\Tesseract-OCR\\tesseract'
    # 语言包目录和参数
    tessdata_dir_config = '--tessdata-dir "C:\\Program Files (x86)\\Tesseract-OCR\\tessdata" --psm 6'

    # lang 指定中文简体
    question = pytesseract.image_to_string(question_im, lang='chi_sim', config=tessdata_dir_config)
    question = question.replace("\n", "")[2:]
    question = question.replace("′", ",")
    question = question.replace(" ", "")

    choices = []
    for i in range(len(choices_im)):
        c = pytesseract.image_to_string(choices_im[i], lang='chi_sim', config=tessdata_dir_config)
        c = c.replace("\n", "")
        c = c.replace("′", ",")
        c = c.replace(" ", "")
        c = c.replace("\\", "")
        choices.append(c)

    return question, choices
