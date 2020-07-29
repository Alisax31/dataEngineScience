#coding: utf-8
import pandas as pd
from efficient_apriori import apriori
data = pd.read_csv(r'./订单表.csv', encoding='gbk')
print(data.head())
data = data[['产品名称','客户ID']]

data = data.sort_values(by='客户ID', ascending=False)
customer_id = data.values[0,1]
transcation = []
transcation_temp = []

for i in range(0,data.shape[0]):
    if customer_id == data.values[i,1]:
        transcation_temp.append(data.values[i,0])
    else:
        customer_id = data.values[i,1]
        transcation.append(transcation_temp)
        transcation_temp = []
        transcation_temp.append(data.values[i,0])

itemsets, rules = apriori(transcation, min_support=0.1, min_confidence=0.45)
print("频繁项集：", itemsets)
print("-"*30)
print("关联规则：", rules)