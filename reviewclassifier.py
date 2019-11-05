import pandas as pd
import numpy as np
import torch
import os
from torch.utils import data

df = pd.read_csv("reviewdf.csv")

if os.path.isfile('vectorReviews') == False:
    from sklearn.feature_extraction.text import CountVectorizer
    vectoriser = CountVectorizer(min_df=0, lowercase=True)
    vectorMatrix = vectoriser.fit_transform(df['text'])
    vectorArray = vectorMatrix.toarray()
    np.save('vectorReviews', vectorArray)
else:
    vectorArray = np.load('vectorReviews.npy')

vectorArray = np.insert(vectorArray, 0, 0, axis=0)
print(vectorArray)
reviewsTensor = torch.Tensor(vectorArray)
opinionsArray = df['opinion'].tolist()
opinionsArray.insert(0, 0)
print(opinionsArray)
opinionsTensor = torch.Tensor(opinionsArray)
reviewDataset = data.TensorDataset(reviewsTensor, opinionsTensor)
torch.save(reviewDataset, "reviewsDataset")