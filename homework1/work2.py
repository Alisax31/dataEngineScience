#coding: utf-8
import numpy as np
scoretype = np.dtype({ 'names':['name', 'chinese', 'math', 'english'], 'formats':['S32', 'i', 'i', 'i']})
students = np.array([('zhangfei',68,65,30),('guanyu',95,76,98),('liubei',98,86,88),('dianwei',90,88,77),('xuzhu',80,90,90)],dtype=scoretype)
chScoreTotal = students[:]['chinese']
maScoreTotal = students[:]['math']
engScoreTotal = students[:]['english']
dt = {} 
chineseMeanScore = np.mean(chScoreTotal)
print("语文平均成绩: %d"%chineseMeanScore)
mathMeanScore = np.mean(maScoreTotal)
print("数学平均成绩：%d"%mathMeanScore)
englishMeanScore = np.mean(engScoreTotal)
print("英语平均成绩：%d"%englishMeanScore)
chineseMaxScore = np.max(chScoreTotal)
print("语文最好成绩：%d"%chineseMaxScore)
mathMaxScore = np.max(maScoreTotal)
print("数学最好成绩：%d"%mathMaxScore)
englishMaxScore = np.max(engScoreTotal)
print("英语最好成绩：%d"%englishMaxScore)
chineseMinScore = np.min(chScoreTotal)
print("语文最差成绩：%d"%chineseMinScore)
mathMinScore = np.min(maScoreTotal)
print("数学最差成绩：%d"%mathMinScore)
englishMinScore = np.min(engScoreTotal)
print("英语最差成绩：%d"%englishMinScore)
chineseVarScore = np.var(chScoreTotal)
print("语文成绩方差：%f"%chineseVarScore)
mathVarScore=np.var(maScoreTotal)
print("数学成绩方差：%f"%mathVarScore)
englishStdScore=np.std(engScoreTotal)
print("英语成绩方差：%f"%englishStdScore)
chineseStdScore = np.std(chScoreTotal)
print("语文成绩标准差：%f"%chineseStdScore)
mathStdScore=np.std(maScoreTotal)
print("数学成绩标准差：%f"%mathStdScore)
englishStdScore=np.std(engScoreTotal)
print("英语成绩标准差：%f"%englishStdScore)
#print(students.reshape(5,4))

for i in range(0,students.shape[0]):
    sum = students[i][1]+students[i][2]+students[i][3]
    dt[students[i][0]]=sum
dt= sorted(dt.items(), key=lambda dt:dt[1], reverse = True)
print(dt)
