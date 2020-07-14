from wordcloud import WordCloud
from nltk.tokenize import word_tokenize
import pandas as pd
import numpy as py
import nltk
import os

def create_word_cloud(path):
    try:
        print(path)
        df = pd.read_csv(path, header=None)
        data = []
        for i in range(df.shape[0]):
            for j in range(df.shape[1]):
                if str(df.values[i,j]) != 'nan':
                    data.append(df.values[i,j])
        f = " ".join(data)
        cut_text = word_tokenize(f)
        cut_text = " ".join(cut_text)
        wc = WordCloud(max_words=100,width=2000,height=1200,)
        wordcloud = wc.generate(cut_text)
        bath_path = os.path.dirname(__file__)
        src = '/static/image/wordcloud.jpg'
        wordcloud.to_file(bath_path + src)
        return src
    except:
       return None
    finally:
       pass