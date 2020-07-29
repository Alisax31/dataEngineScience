#coding: utf-8
import pandas as pd
from efficient_apriori import apriori
from mlxtend.frequent_patterns import apriori as apr
from mlxtend.frequent_patterns import association_rules

#针对efficient_apriori进行transcation生成
def transcation1_generate(path):
    #读取CSV
    data = pd.read_csv(path, encoding='gbk')
    #截取所需要数据
    data = data[['客户ID','产品名称']]
    #转换格式为series
    data_series = data.set_index('客户ID')['产品名称']
    #针对Index排序
    data_series = data_series.sort_index(ascending=False)
    transcation = []
    #获取第一个index值
    temp_index = data_series.index[0]
    temp_set = set()
    #循环整个series，通过判断客户ID(index)进行处理生成transcation
    for i,v in data_series.items():
        #如果客户ID不相等
        if i != temp_index:
            #清除之前的set
            temp_set = set()
            #更新临时变量用于下一步处理
            temp_index = i
            #将不相等的值存入临时set
            temp_set.add(v)
            #将临时set存入transcation
            transcation.append(temp_set)
        else:
            temp_set.add(v)
    return transcation

#mlxtend_apriori的transcation生成
def transcation2_generate(path):
    data = pd.read_csv(path, encoding='gbk')
    #进行hotcode编码
    hot_encoded_df = data.groupby(['客户ID','产品名称'])['产品名称'].count().unstack().fillna(0).reset_index().set_index('客户ID')
    hot_encoded_df = hot_encoded_df.applymap(lambda x:0 if x<=0 else 1 )
    return hot_encoded_df

#封装相关efficient_apriori实现
def efficient_apriori(transcation, min_support, min_confidence):
    itemsets, rules = apriori(transcation, min_support=min_support, min_confidence=min_confidence)
    print("-"*60)
    print('efficient_apriori:')
    print("频繁项集：", itemsets)
    print("关联规则：", rules)
    print("-"*60)

#封装相关mlxtend_apriori实现
def mlxtend_apriori(transcation, min_surpport, min_threshold):
    frequent_itemsets = apr(transcation, min_support=min_surpport, use_colnames=True)
    rules = association_rules(frequent_itemsets, metric="lift", min_threshold=min_threshold)
    print("-"*60)
    print('mlxtend_apriori:')
    print("频繁项集：", frequent_itemsets)
    print("关联规则：", rules[ (rules['lift'] >= 1) & (rules['confidence'] >= 0.5) ])
    print("-"*60)

if __name__ == '__main__':
    path = r'./订单表.csv'
    min_support = 0.05
    min_confidence = 0.45
    min_threshold = 0.45
    efficient_apriori(transcation1_generate(path), min_support, min_confidence)
    mlxtend_apriori(transcation2_generate(path), min_support, min_threshold)