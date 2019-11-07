import pandas as pd
import numpy as np
import torch
import os
import codecs
from torch.utils import data

df1 = pd.read_csv("./reviewsdfs/reviewdf1.csv")
df2 = pd.read_csv("./reviewsdfs/reviewdf2.csv")

if os.path.isfile('vectorReviews.npy') == False:
    from sklearn.feature_extraction.text import CountVectorizer
    vectoriser = CountVectorizer(min_df=0, lowercase=True)
    vectoriser.fit(df2['text'])
    vectorMatrix = vectoriser.fit_transform(df1['text'])
    vectorArray = vectorMatrix.toarray()
    np.save('vectorReviews', vectorArray)
    with codecs.open('vectorDic.txt', 'w', 'utf-8') as f:
        feature_names = vectoriser.get_feature_names()
        print(feature_names)
        for item in feature_names:
            f.write(item + "\n")
else:
    vectorArray = np.load('vectorReviews.npy')

vectorArray = np.insert(vectorArray, 0, 0, axis=0)
print(vectorArray)
reviewsTensor = torch.Tensor(vectorArray)
opinionsArray = df1['opinion'].tolist()
opinionsArray.insert(0, 0)
print(opinionsArray)
opinionsTensor = torch.Tensor(opinionsArray)
reviewDataset = data.TensorDataset(reviewsTensor, opinionsTensor)
torch.save(reviewDataset, "reviewsDataset")