import requests
import pandas as pd
from bs4 import BeautifulSoup

heads = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36'}


def get_w(c, y):
    print("===================程序运行中=====================")
    a1 = []
    a2 = []
    a3 = []
    a4 = []
    a5 = []
    a6 = []
    a7 = []
    a8 = []
    a9 = []
    a10 = []
    for year in range(2020, 2023):
        for mon in range(1, 13):
            time = year * 100 + mon
            a1.append(y[1:-1])
            a2.append(c[1:-1])
            a3.append(str(year))
            a4.append(str(mon))
            # time = 202001
            url_c = "https://m.tianqi.com/lishi{}{}.html".format(c, time)
            res = requests.get(url_c, headers=heads).content.decode()
            s = BeautifulSoup(res, 'lxml')
            ci = s.find_all(attrs={'class': 'count_temp'})
            if ci[0] is None:
                continue
            list_a = ci[0].find_all('td')

            list_ans = []

            for t in list_a:
                list_ans.append(t.h5.text)
            a5.append(list_ans[0])
            a6.append(list_ans[1])
            a7.append(list_ans[2])
            a8.append(list_ans[3])
            a9.append(list_ans[4])
            a10.append(list_ans[5])
    datas = pd.DataFrame(
        {'省份': a1, '城市': a2, '年份': a3, '月份': a4, '平均高温': a5,
         '平均低温': a6, '极端高温': a7, '极端低温': a8, '空气最好': a9, '空气最差': a10})
    datas.to_csv('D:\one.csv', encoding='utf_8_sig', mode='a')


def get_sheng(c):
    url = 'https://m.tianqi.com{}/'.format(c)
    res = requests.get(url, headers=heads).content.decode()
    s = BeautifulSoup(res, 'lxml')
    ci = s.find_all(attrs={'class': 'more_weather2'})
    list_a = ci[0].find_all('a')
    list_city = []
    for w in list_a:
        # print(w.get('href'))
        list_city.append(w.get('href')[0:-7])
    # 一会改成城市循环
    for t in list_city:
        # print(t)
        get_w(t, c)


response = requests.get('https://m.tianqi.com/lishi/', headers=heads).content.decode()
soup = BeautifulSoup(response, 'lxml')
a = soup.find_all('a')
k = 0
city = []
ts = ["/beijing", "/tianjin", "/chongqing", "/shanghai", "/hongkong", "/aomen"]
for i in range(44, 78):
    city.append(a[i].get('href'))
# 全国省份（含台湾）
for i in city:
    tmp = i[6:]
    if tmp in ts:
        continue
    print(tmp)
    get_sheng(tmp)
# get_sheng("/taiwan")

# 全国直辖市（含港澳）
for i in ts:
    temp = i + "/"
    print(temp)
    get_w(temp, temp)
# get_w("/beijing/", "/beijing/")

print("执行结束")
