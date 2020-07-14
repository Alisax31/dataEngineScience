#coding: utf-8
import time
import os
import pandas as pd
import numpy as np
#import fptools as fp
import pyfpgrowth as fp
from efficient_apriori import apriori
from mlxtend.frequent_patterns import apriori as apr
from mlxtend.frequent_patterns import association_rules

#transcation生成器
def transcationGenerator(df, option):
    if option == "efficient":
        col = df.shape[1]
        row = df.shape[0]
        transcation = []
        print("开始处理数据")
        start_time = time.time()
        for row_i in range(0,row):
            transcation_temp = []
            for col_i in range(0,col):
                if str(df.values[row_i, col_i]) != 'nan':
                    transcation_temp.append(str(df.values[row_i, col_i]))
            transcation.append(transcation_temp)
        end_time = time.time()
        print("数据处理完毕，处理时间：",end_time-start_time)
        return transcation
    if option == "non-efficient":
        df.fillna('', inplace=True)
        for i in range(0,df.shape[0]):
            for j in range(0,df.shape[1]):
                if df.values[i,j] != '' and j != 0:
                    df.values[i,0] = df.values[i,0] + "/" + df.values[i,j] 
                    df.values[i,j] = ''
        transcation = df[0].str.get_dummies("/")
        return transcation
#efficient_apriori
def apriori_one(transcation, **kwargs):
    if len(kwargs) == 0 :
        itemsets, rules = apriori(transcation, min_support=0.1, min_confidence=0.5)
        print("频繁项集：", itemsets)
        print("-"*30)
        print("关联规则：", rules)
    else:
        itemsets, rules = apriori(transcation, min_support=float(kwargs['support']), min_confidence=float(kwargs['confidence']))
        print("频繁项集：", itemsets)
        print("-"*30)
        print("关联规则：", rules)

def apriori_two(transcation, min_support, metric, min_threshold):
    itemsets = apr(transcation, use_colnames=True, min_support=min_support)
    itemsets = itemsets.sort_values(by="support", ascending=False)
    print(itemsets)
    rules = association_rules(itemsets, metric=metric, min_threshold=min_threshold)
    rules = rules.sort_values(by=metric, ascending=False)
    pd.options.display.max_columns = 100
    print(rules)

def main():
    df = pd.read_csv(r"MarketBasket/Market_Basket_Optimisation.csv", header=None)
    transcation_efficient = transcationGenerator(df, "efficient")
    transcation_non_efficient = transcationGenerator(df, "non-efficient")
    print('-'*20, 'Apriori', '-'*20)
    apriori_one(transcation_efficient, support=0.05, confidence=0.3)
    print('-'*20, 'Apriori', '-'*20)
    apriori_two(transcation_non_efficient, 0.05,"confidence", 0.3)
    print('-'*20, 'FP-GROWTH', '-'*20)
    patterns = fp.find_frequent_patterns(transcation_efficient, 20)
    rules = fp.generate_association_rules(patterns, 0.3)
    print('关联规则：', '\n', rules)    

if __name__ == "__main__":
    main()