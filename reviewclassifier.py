import pandas as pd
import numpy as np
import torch
import os
import codecs
from torch.utils import data

print("loading dataframes")
df1 = pd.read_csv("./reviewsdfs/reviewdfTOP.csv")

if os.path.isfile('vectorReviews.npy') == False:
    print("generating vectors")
    from sklearn.feature_extraction.text import CountVectorizer
    vectoriser = CountVectorizer(min_df=0, lowercase=True)
    vectorMatrix = vectoriser.fit_transform(df1['text'])
    vectorArray = vectorMatrix.toarray()

    print("saving vector")
    np.save('vectorReviews', vectorArray)
    with codecs.open('vectorDic.txt', 'w', 'utf-8') as f:
        feature_names = vectoriser.get_feature_names()
        for item in feature_names:
            f.write(item + "\n")
else:
    print("loading Vectors")
    vectorArray = np.load('vectorReviews.npy')

print("generting dataset")
reviewsTensor = torch.Tensor(vectorArray)
opinionsArray = df['opinion'].tolist()

print("saving")
opinionsTensor = torch.Tensor(opinionsArray)
reviewDataset = data.TensorDataset(reviewsTensor, opinionsTensor)
torch.save(reviewDataset, "reviewsDataset")