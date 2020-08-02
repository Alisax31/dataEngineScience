#coding: utf-8
import requests as rq
import pandas as pd
import time
from bs4 import BeautifulSoup

#通过request获取页面内容并转换为beautifulsoup类型
def get_url_content(url,headers,timeout):
    html =  rq.get(url,headers,timeout=timeout).text
    soap = BeautifulSoup(html,'html.parser')
    return soap

#通过解析bs文档，获取页面内容
def convert_content(df,html_soap):
    #解析获取class为search-result-list-item的div
    search_result_list = html_soap.find_all('div', class_='search-result-list-item')
    #遍历div结果集
    for item in search_result_list:
        #需要的文字内容都存在<p>标签里，find_all找出所有
        item_list = item.find_all('p')
        name, price = item_list[0].string, item_list[1].string
        price_split = price.split('-')
        #需要的图片内容都存在<img>标签里，find_all找出所有
        pic_list = item.find_all('img')
        pic_href = 'http:' + pic_list[0].get('src')
        #对price字符串进行‘-’分割，并且有价格暂无单独处理
        if len(price_split) == 1:
            lowest_price, highest_price = '暂无', '暂无'
        else:
            lowest_price, highest_price = price_split[0] + '万', price_split[1]
        #生成dataframe
        temp = {}
        temp['名称'], temp['最低价格'], temp['最高价格'], temp['产品图片链接']=name, lowest_price, highest_price, pic_href
        df = df.append(temp, ignore_index=True)
    return df

if __name__ == '__main__':
    base_url = 'http://car.bitauto.com/xuanchegongju/?l=8&mid=8'
    headers = "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36"
    vw_car_list = pd.DataFrame(columns=['名称','最低价格','最高价格','产品图片链接'])
    timeout = 100
    html_soap = get_url_content(base_url, headers, timeout)
    vw_car_list = convert_content(vw_car_list, html_soap)
    #最终结果导出excel
    vw_car_list.to_csv('project_a_result.csv', encoding='gbk')