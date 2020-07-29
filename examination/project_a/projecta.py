#coding: utf-8
import requests as rq
import pandas as pd
import time
from bs4 import BeautifulSoup

def get_url_content(url,headers,timeout):
    html =  rq.get(url,headers,timeout=timeout).text
    soap = BeautifulSoup(html,'html.parser')
    return soap

def convert_content(df,html_soap):
    search_result_list = html_soap.find_all('', class_='search-result-list-item')
    for item in search_result_list:
        item_list = item.find_all('p')
        name, price = item_list[0].string, item_list[1].string
        price_split = price.split('-')
        pic_list = item.find_all('img')
        pic_href = 'http:' + pic_list[0].get('src')
        if len(price_split) == 1:
            lowest_price, highest_price = '暂无', '暂无'
        else:
            lowest_price, highest_price = price_split[0] + '万', price_split[1]
        temp = {}
        temp['名称'], temp['最低价格'], temp['最高价格'], temp['产品图片链接']=name, lowest_price, highest_price, pic_href
        print(temp)
        df = df.append(temp, ignore_index=True)
        print(df)
    return df

if __name__ == '__main__':
    base_url = 'http://car.bitauto.com/xuanchegongju/?l=8&mid=8'
    headers = "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36"
    vw_car_list = pd.DataFrame(columns=['名称','最低价格','最高价格','产品图片链接'])
    timeout = 100
    html_soap = get_url_content(base_url, headers, timeout)
    vw_car_list = convert_content(vw_car_list, html_soap)
    vw_car_list.to_csv('project_a_result.csv', encoding='gbk')