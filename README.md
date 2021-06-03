# crawler_for_university
用python爬取江苏几大高校的就业网站，并提供3种方式通知给用户，分别是通过微信发送、命令行直接输出、windows气泡通知。
===========================

# 环境依赖
wxpy,requests,bs4等库

# 功能描述
该项目基于python，通过爬虫爬各高校的就业信息网，爬取招聘信息并存储，如果碰到新的信息，则输出，提供3种输出方式：
## 微信发送消息
微信发消息基于网页版微信实现，使用wxpy库，使用该库的同时，不能使用电脑版或pad版微信，否则会挤下线。
并非所有用户都能使用该功能，查询自己能否使用该功能，需要打开<https://wx.qq.com/>。检测能否扫码登录，如果可以，则能使用。
## 直接命令行输出
如果不能使用，可以直接命令行输出爬取后的信息。
## windows下利用气泡通知
windows下提供操作中心显示通知，可以在windows的操作中心查看消息。

## 重要代码描述
该函数用以爬取url的信息
```Python
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
```

该函数输入大学简称，对网页内容进行爬取，筛选，然后发送通知。
```Python
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
```
# 使用方法
下载main文件，安装所需要的库，在命令行下面代码进行运行
```
python main.py
```
