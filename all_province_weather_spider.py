import requests
import pandas as pd
from bs4 import BeautifulSoup

# 报文头伪装
heads = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36'}

begin_year = 2020  # 开始年份
end_year = 2023  # 结束年份+1


# 获取对应城市的数据
def get_city(city, province):
    print("===================正在爬取{}中=====================".format(city))
    # 批量创建列表存储对应数据
    province_list, city_list, years_list, month_list, average_max_temperature, average_min_temperature, max_temperature, min_temperature, max_air_quality, min_air_quality = [
        list() for x in range(10)]
    # 遍历需要爬去数据的年份
    for year in range(begin_year, end_year):
        # 遍历12个月
        for mon in range(1, 13):
            # 得出时间如202001
            times = year * 100 + mon
            # 去除province两侧的 '/'
            province_list.append(province[1:-1])
            # 去除city两侧的 '/'
            city_list.append(city[1:-1])
            years_list.append(str(year))
            month_list.append(str(mon))
            # 装填对应url
            url_city = "https://m.tianqi.com/lishi{}{}.html".format(city, times)
            # 将得到数据转换成二进制
            res = requests.get(url_city, headers=heads).content.decode()
            # 用lxml解析对应数据
            soup = BeautifulSoup(res, 'lxml')
            # 查找属性 class = 'count_temp'
            class_count_temp = soup.find_all(attrs={'class': 'count_temp'})
            # 查找标签 td
            list_td = class_count_temp[0].find_all('td')
            list_h5 = []
            for t in list_td:
                list_h5.append(t.h5.text)
            average_max_temperature.append(list_h5[0])
            average_min_temperature.append(list_h5[1])
            max_temperature.append(list_h5[2])
            min_temperature.append(list_h5[3])
            max_air_quality.append(list_h5[4])
            min_air_quality.append(list_h5[5])
    # 将数据流存储到datas中
    datas = pd.DataFrame(
        {'省份': province_list, '城市': city_list, '年份': years_list, '月份': month_list, '平均高温': average_max_temperature,
         '平均低温': average_min_temperature, '极端高温': max_temperature, '极端低温': min_temperature, '空气最好': max_air_quality,
         '空气最差': min_air_quality})
    # 导出数据
    datas.to_csv('D:\one.csv', encoding='utf_8_sig', mode='a')


# 获取对应省份的数据
def get_province(province):
    # 打印省份名
    print("=============={}================".format(province))
    # 填充url
    url = 'https://m.tianqi.com{}/'.format(province)
    # 获取网页
    res = requests.get(url, headers=heads).content.decode()
    # 解析网页
    soup = BeautifulSoup(res, 'lxml')
    # 查找标签
    ci = soup.find_all(attrs={'class': 'more_weather2'})
    # 查找标签
    list_a = ci[0].find_all('a')
    # 该省份所拥有的城市list
    list_city = []
    for w in list_a:
        # 提取城市名
        list_city.append(w.get('href')[0:-7])
    # 遍历城市
    for t in list_city:
        get_city(t, province)


if __name__ == '__main__':
    # 获取网页
    response = requests.get('https://m.tianqi.com/lishi/', headers=heads).content.decode()
    # 解析网页 得到文档树
    soup = BeautifulSoup(response, 'lxml')
    # 得到a标签列表
    list_a = soup.find_all('a')
    # 用于装省份名的列表
    all_province_list = []
    province_city_list = ["/beijing", "/tianjin", "/chongqing", "/shanghai", "/hongkong", "/aomen"]
    for i in range(44, 78):
        all_province_list.append(list_a[i].get('href'))
    # ==================================预处理完成===================================

    # 遍历全国省份（含台湾）
    for i in all_province_list:
        tmp = i[6:]
        # 如果是直辖市continue
        if tmp in province_city_list:
            continue
        get_province(tmp)

    # 遍历全国直辖市（含港澳）
    for i in province_city_list:
        temp = i + "/"
        get_city(temp, temp)

print("*************执行结束****************")
# get_province("/taiwan")
# get_city("/beijing/", "/beijing/")
