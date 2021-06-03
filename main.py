import wxpy
import requests
import time
from bs4 import BeautifulSoup
import platform
import random

flag = False
if platform.system() == 'Windows':
    import windows
    import winsound

    duration = 500  # millisecond
    freq = 440  # Hz
    message = windows.TestTaskbarIcon()
    flag = True
else:
    import os

    print('该系统不支持气泡通知!')


def get_url(url, kv):
    '''
    用以爬取网站内容的函数
    :param url:输入url
    :param kv:headers信息
    :return:返回爬取到的内容
    '''
    try:
        r = requests.get(url, headers=kv)
        r.raise_for_status()
        return r
    except:
        try:
            time.sleep(3)
            r = requests.get(url, headers=kv)
            r.raise_for_status()
            return r
        except:
            return 0


def get_job(university):
    '''
    用来获取各大学的就业信息网的内容
    :param university:输入学校简称
    :return:无
    '''
    global url_list, send_target
    job_url = 'http://' + university + '.91job.org.cn/campus'  # 生成url
    r = get_url(url=job_url, kv={'User-Agent': 'Mozilla/5.0'})
    soup = BeautifulSoup(r.text, 'lxml')
    r_soup = soup.find_all(attrs={'class': 'infoList'})  # 解析网页找到对应的内容

    for i in r_soup:  # 遍历每个结果
        temp = i.find(attrs={'class': 'span7'}).find(name='a').get('href')  # 找到通知对应的网站
        url = job_url + temp[7:]  # 生成招聘信息对应的网站
        if url not in url_list:  # 如果这条信息之前并未存储
            with open("url_list.txt", "a+") as f:  # 打开文件，并添加招聘信息
                f.write(url + '\n')
            url_list.append(url)  # 本地list里面也添加信息
            message_title = university_list[university] + '有一条招聘消息：'  # 标题
            message_text = i.get_text() + url  # 内容
            if 1 in model_choose:  # 模式1，直接print
                print('*' * 100)
                print(message_title + message_text)
            if 2 in model_choose:  # 模式2，给微信好友发消息
                send_target.send(message_title + message_text)
            if 3 in model_choose:  # 模式3，windows气泡消息
                if flag:
                    message.show_msg(message_title, message_text, 1)
            if flag:  # 提示音
                winsound.Beep(freq, duration)
            else:
                os.system('play --no-show-progress --null --channels 1 synth %s sine %f' % (duration / 1000, freq))


if __name__ == '__main__':

    model_choose = [1, 2, 3]  # 通知方式选择，通知方式1为直接print输出，通知方式2为发送微信消息到指定目标，通知方式3为Windows下的气泡通知。

    # 仅支持使用就业网站http://xxxx.91job.org.cn/格式的大学，其中xxxx为大学简称
    university_list = {'seu': '东南大学',
                       'nuaa': '南京航空航天大学',
                       'njust': '南京理工大学',
                       'njupt': '南京邮电大学',
                       'nuist': '南京信息工程大学',
                       'njtech': '南京工业大学',
                       'hhu': '河海大学',
                       'njfu': '南京林业大学',
                       'njau': '南京农业大学',
                       'njmu': '南京医科大学',
                       'njucm': '南京中医药科大学',
                       'njnu': '南京师范大学',
                       'njue': '南京财经大学'}

    # 读取url_list
    url_list = []
    with open("url_list.txt", "r") as f:  # 打开文件
        data = f.readlines()  # 读取文件
        for i in data:
            url_list.append(i.strip('\n'))

    # 构建微信机器人
    bot = wxpy.Bot(cache_path=True, console_qr=False)
    bot.enable_puid()

    # send_target = bot.file_helper  # 发送目标为文件传输助手
    send_target = bot.self  # 发送目标设定为自己
    # send_target = bot.friends().search(name='张张张')[0]  # 搜索微信好友名称为'张张张'的好友
    # send_target = bot.friends().search(puid='664612a6')[0]
    # 搜索微信好友puid为'664612a6'的用户，该模块具体使用方法参考https://wxpy.readthedocs.io/zh/latest/chats.html#id5

    while True:  # 循环爬学校
        for university_english, university_chinese in university_list.items():
            get_job(university_english)
            time.sleep(random.random() * 30 + 20)  # 随机休息20~50s，再访问下一个学校。
