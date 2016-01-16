## Collapse the individual sentence
#Group them in sequences of multiple sentences and sentiments for each sentence
import pandas as pd
import matplotlib.pyplot as plt

import matplotlib
matplotlib.style.use('ggplot')

sentiment1 = pd.read_csv("all_debates_PAsent.csv")
sentiment2 = pd.read_csv("all_debates_NBsent.csv")
#Deleting (dropping) certain columns from the dataframe
del sentiment2['Text']
del sentiment2['Speaker']
del sentiment2['SequenceNo']

sentiment3 = pd.read_csv("all_debates_snlpsent.csv")

data = pd.merge(sentiment1,sentiment2,on=['Party', 'DebateNo', 'SentenceNo'])
data = pd.merge(data,sentiment3, on = ['Party', 'DebateNo', 'SentenceNo'])

data['wc'] = 0
# If a sentence has less than 3 words, force it to be neutral
# for index, row in data.iterrows():
#     score1 = row['Score']
#     text = str(row['Text'])
#     wordcount = len(text.split(None)) 
#     #print index, " ", text, " ",wordcount
# #    print data.ix[index,'wc']
#     data.ix[index,'wc']= wordcount
#     if wordcount < 4 and score1 <2:
#     	data.ix[index,'Score']= 2

#Combining the raw scores for each sentence and aggregate into a paragraph
# data1=data.groupby(['SequenceNo'])['Score'].mean().reset_index()
# data2=data.groupby(['SequenceNo'])['Text'].apply(lambda x: ','.join(x)).reset_index()
# data3 = data.drop_duplicates(['SequenceNo','Speaker'])[['SequenceNo','Speaker']]
# 
# print(data1)
# print(data2.head(5))
# data12 = pd.merge(data1,data2,on='SequenceNo')
# data = pd.merge(data3, data12, on ='SequenceNo')
#data = data [~data.Speaker.isin(['MALE','SANTELLI','(UNKNOWN)','UNIDENTIFIED MALE','HARMAN', 'HARWOOD','CRAMER','EPPERSON','QUICK','QUINTANILLA'])]
#print(data)
#ax = data.boxplot(column='Score', by = 'Speaker')
#fig = ax.get_figure()
#fig.savefig('figure.png')
data.to_csv("all_debates_all_sents.csv", index = False)

