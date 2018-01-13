# -*- coding: utf-8 -*-

# @Author  : Skye
# @Time    : 2018/1/9 10:39
# @desc    :

import requests
import webbrowser

def open_webbrowser(question,choices):
    print('\n-- 题目+选项 百度 搜索结果计数法 --')
    counts = []
    for i in range(len(choices)):
        # 请求
        try:
            req = requests.get(url='http://www.baidu.com/s', params={'wd': question + choices[i]}, timeout=3)
            content = req.text
            index = content.find('百度为您找到相关结果约') + 11
            content = content[index:index+50]
            index = content.find('个')
            count = content[:index].replace(',', '')
            counts.append(count)
            #print(choices[i] + " : " + count)
        except:
            print("搜索超时")
            return
    output(choices, counts)

def open_webbrowser_count(question,choices):
    print('\n-- 题目+选项 搜狗 搜索结果计数法 --')
    counts = []
    for i in range(len(choices)):
        # 请求
        try:
            req = requests.get(url='http://www.sogou.com/web', params={'query': question + choices[i]}, timeout=3)
            content = req.text
            index = content.find('搜狗已为您找到约') + 8
            content = content[index:index+50]
            index = content.find('条')
            count = content[:index].replace(',', '')
            counts.append(count)
            #print(choices[i] + " : " + count)
        except:
            print("搜索超时")
            return
    output(choices, counts)

def count_base(question,choices):
    print('\n-- 题目 选项出现的词频 --')
    # 请求
    try:
        req = requests.get(url='http://www.baidu.com/s', params={'wd':question}, timeout=3)
        #req = requests.get(url='http://www.sogou.com/web', params={'query': question}, timeout=5)
        content = req.text
        counts = []
        for i in range(len(choices)):
            counts.append(content.count(choices[i]))
    except:
        print("搜索超时")
        return
    output(choices, counts)

def output(choices, counts):
    counts = list(map(int, counts))
    for i in range(len(choices)):
        print("%s:\t%d" % (choices[i], counts[i]))


def run_algorithm(al_num, question, choices):
    if al_num == 0:
        open_webbrowser(question, choices)
    elif al_num == 1:
        open_webbrowser_count(question, choices)
    elif al_num == 2:
        count_base(question, choices)

if __name__ == '__main__':
    question = '新装修的房子通常哪种化学物质含量会比较高?'
    choices = ['甲醛', '苯', '甲醇']
    run_algorithm(1, question, choices)


