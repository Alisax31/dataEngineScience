#coding: utf-8
#891 513 505
import pandas as pd
from sklearn import preprocessing
from sklearn.cluster import KMeans
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import silhouette_score
from . import pyult as ult
import matplotlib.pyplot as plt

#数据从csv导入
def data_import(importpath):
    df = pd.read_csv(importpath)
    return df
#数据训练
def data_tran(df):
    #去除不需要的字段
    tran_x = df.drop(['car_ID','CarName'], axis=1)
    #将数据标签化
    le = LabelEncoder()
    tran_x['fueltype'] = le.fit_transform(tran_x['fueltype'])
    tran_x['aspiration'] = le.fit_transform(tran_x['aspiration'])
    tran_x['doornumber'] = le.fit_transform(tran_x['doornumber'])
    tran_x['carbody'] = le.fit_transform(tran_x['carbody'])
    tran_x['drivewheel'] = le.fit_transform(tran_x['drivewheel'])
    tran_x['enginelocation'] = le.fit_transform(tran_x['enginelocation'])
    tran_x['enginetype'] = le.fit_transform(tran_x['enginetype'])
    tran_x['cylindernumber'] = le.fit_transform(tran_x['cylindernumber'])
    tran_x['fuelsystem'] = le.fit_transform(tran_x['fuelsystem'])
    #数据0-1标准化
    min_max_scaler = preprocessing.MinMaxScaler()
    tran_x = min_max_scaler.fit_transform(tran_x)
    return tran_x
#手肘法
def sse(tran_x, path):
    sse = []
    for k in range(2,50):
        kmeans = KMeans(n_clusters=k)
        kmeans.fit(tran_x)
        sse.append(kmeans.inertia_)
    x = range(2,50)
    plt.xlabel('k')
    plt.ylabel('SSE')
    plt.plot(x,sse,'o-')
    imgsrc = path + '/sse.png'
    plt.savefig(imgsrc)
    # plt.show()
#轮廓系数
def sc_scores(tran_x, path):
    sc_scores = []
    for k in range(2,50):
        kmeans = KMeans(n_clusters=k)   
        kmeans_model = kmeans.fit(tran_x)
        sc_score = silhouette_score(tran_x, kmeans_model.labels_, metric='euclidean')
        sc_scores.append(sc_score)
        k = range(2,50)
    plt.xlabel('k')
    plt.ylabel('SCS')
    plt.plot(k,sc_scores, '*-')
    imgsrc = path + '/sc_scores.png'
    plt.savefig(imgsrc)
    # plt.show()
#通过手肘法，轮廓系数确定K值
# def confirmK(df):
#     tran_x = data_tran(df)
#     sse(tran_x)
#     sc_scores(tran_x)
#生成结果集
def generate_result(data, predict_y):
    #直接生成预测结果总表
    data['predict_y'] = predict_y
    path = ult.generate_abspath(__file__, 'download')
    data.to_csv(path+'/project_c_result.csv', encoding='utf-8')
    return path
    # #通过找到有vw关键字的车辆对应的预测值进行分类输出
    # data_list_containvw = data.loc[data['CarName'].str.contains('vw')]
    # vw_predict_y = data_list_containvw['predict_y'].to_list()
    # vw_predict_y_nodup = []
    # reuslt = []
    # #如果vw车辆在同一分组输出同一分组内所有数据
    # #如果vw车辆不在同一分组输出VW车辆所在不同分组内所有数据
    # for item in vw_predict_y:
    #     if item not in vw_predict_y_nodup:
    #         vw_predict_y_nodup.append(item)
    # #分组输出
    # for i in range(0,len(vw_predict_y_nodup)):
    #     #定义临时路径
    #     temp_dir = ult.generate_abspath(__file__, 'download')+'project_c_cluster_'+str(vw_predict_y[i])+'.csv'
    #     #找到和vw车辆同一个预测值对应数据集并输出csv
    #     reuslt.append('project_c_cluster_'+str(vw_predict_y[i])+'.csv')
    #     data.loc[data['predict_y']==vw_predict_y[i]].to_csv(temp_dir, encoding='utf-8')
    # return reuslt

def kmeans(k,tran_x):
    kmeans = KMeans(n_clusters=k)
    kmeans.fit(tran_x)
    predict_y = kmeans.predict(tran_x)
    return predict_y
# if __name__ == '__main__':
#     path = r'./CarPrice_Assignment.csv'
#     data = data_import(path)
#     tran_x = data_tran(data)
#     confirmK(data)
#     #通过手肘法，轮廓系数确认K值
#     k = input('请输入K值：')
#     kmeans = KMeans(n_clusters=k)
#     kmeans.fit(tran_x)
#     predict_y = kmeans.predict(tran_x)
#     generate_result(data, predict_y)
