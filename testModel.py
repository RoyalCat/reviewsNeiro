import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.autograd import Variable
import codecs
import re
import pandas as pd
import random as rng
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

class Net(nn.Module):

    def __init__(self, dicSize):
        super(Net, self).__init__()

        self.fc1 = nn.Linear(dicSize, int(dicSize/64))
        self.fc3 = nn.Linear(int(dicSize/64), 2)
   
    def forward(self, x):
        x = F.relu(self.fc1(x))
        x = self.fc3(x)
        return F.log_softmax(x)


model = torch.load("net.model")
model.eval()


def predict_review(review_text):
    input = Variable(review_text).to(device)
    output = model(input)
    index = output.data.cpu().numpy().argmax()
    return index

dic = list()
with codecs.open('vectorDic.txt', 'rb', 'utf-8') as fp:
    for line in fp:
        dic.append(line[0:-1])


from sklearn.feature_extraction.text import CountVectorizer
vectoriser = CountVectorizer(min_df=0, lowercase=True, vocabulary=dic)

test_df = pd.read_csv("./reviewsdfs/reviewdf2.csv")
print(test_df)
predict_result_total = 0


for index, review in test_df.iterrows():
    review_text = review['text']
    review_text = review_text.lower()
    review_text = re.sub(r'<.{1,}>', ' ', review_text)
    review_text = re.sub(r'[^\w]', ' ', review_text)
    review_vector = vectoriser.transform([review_text]).toarray()
    #print(review['text'])
    review_tensor = torch.Tensor(review_vector)
    predicted_result = predict_review(review_tensor)
    #print("Predicted: " + str(predicted_result))
    #print("Real: " + str(review['opinion']))
    #wait = input()
    if predicted_result == review['opinion']:
        predict_result_total += 1

print("Acc: " + str((predict_result_total/test_df.shape[0])))