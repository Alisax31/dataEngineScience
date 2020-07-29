#coding: utf-8
#891 513 505
import pandas as pd
from sklearn import preprocessing
from sklearn.cluster import KMeans
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import silhouette_score
import matplotlib.pyplot as plt

def data_import(importpath):
    df = pd.read_csv(importpath)
    return df
#数据训练
def data_tran(df):
    tran_x = df.drop(['car_ID','CarName'], axis=1)
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
    min_max_scaler = preprocessing.MinMaxScaler()
    tran_x = min_max_scaler.fit_transform(tran_x)
    return tran_x
#手肘法
def sse(tran_x):
    sse = []
    for k in range(2,50):
        kmeans = KMeans(n_clusters=k)
        kmeans.fit(tran_x)
        sse.append(kmeans.inertia_)
    x = range(2,50)
    plt.xlabel('k')
    plt.ylabel('SSE')
    plt.plot(x,sse,'o-')
    plt.show()
#轮廓系数
def sc_scores(tran_x):
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
    plt.show()

def confirmK(df):
    tran_x = data_tran(df)
    sse(tran_x)
    sc_scores(tran_x)

# def kmeansfit(k, tran_x):
#     kmeans = KMeans(n_clusters=k)
#     kmeans.fit(tran_x)
#     return kmeans
def generate_result(data, predict_y):
    data['predict_y'] = predict_y
    data.to_csv('project_c_result.csv', encoding='utf-8')
    data_list_containvw = data.loc[data['CarName'].str.contains('vw')]
    vw_predict_y = data_list_containvw['predict_y'].to_list()
    vw_predict_y_nodup = []
    for item in vw_predict_y:
        if item not in vw_predict_y_nodup:
            vw_predict_y_nodup.append(item)
    for i in range(0,len(vw_predict_y_nodup)):
        temp_dir = 'project_c_cluster_'+str(vw_predict_y[i])+'.csv'
        data.loc[data['predict_y']==vw_predict_y[i]].to_csv(temp_dir, encoding='utf-8')

if __name__ == '__main__':
    path = r'./CarPrice_Assignment.csv'
    data = data_import(path)
    tran_x = data_tran(data)
    confirmK(data)
    k = input('请输入K值：')
    kmeans = KMeans(n_clusters=k)
    kmeans.fit(tran_x)
    predict_y = kmeans.predict(tran_x)
    generate_result(data, predict_y)
