import pandas as pd
import numpy as np
import torch
import os
import codecs
from torch.utils import data

print("loading dataframes")
df = pd.read_csv("./reviewsdfs/reviewdfTOP.csv")

if os.path.isfile('vectorReviews.npy') == False:
    print("generating vectors")
    from sklearn.feature_extraction.text import CountVectorizer
    vectoriser = CountVectorizer(min_df=0, lowercase=True, dtype=np.int8)
    vectorMatrix = vectoriser.fit_transform(df['text'])
    vectorArray = vectorMatrix.toarray()

    print("saving vector")
    np.savez('vectorReviews', vectorArray)
    with codecs.open('vectorDic.txt', 'w', 'utf-8') as f:
        feature_names = vectoriser.get_feature_names()
        for item in feature_names:
            f.write(item + "\n")
else:
    print("loading vectors")
    vectorArray = np.load   ('vectorReviews.npy')

print("generting dataset")
reviewsTensor = torch.ByteTensor(vectorArray)

opinionsArray = df['opinion'].tolist()
opinionsTensor = torch.ByteTensor(opinionsArray)

reviewDataset = data.TensorDataset(reviewsTensor, opinionsTensor)

print("saving")
torch.save(reviewDataset, "reviewsDataset")