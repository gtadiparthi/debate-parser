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
del sentiment3['SequenceNo']

data = pd.merge(sentiment1,sentiment2,on=['Party', 'DebateNo', 'SentenceNo'])
data = pd.merge(data,sentiment3, on = ['Party', 'DebateNo', 'SentenceNo'])


data['Polarity_Sent']="VeryNegative"
data['NB_Sent']="VeryNegative"
data['SNLP_Sent']="VeryNegative"
def assignLabels():
	# If a sentence has less than 3 words, force it to be neutral
	for index, row in data.iterrows():
		polarityScore = row['PolarityPAScore']
		nbScore = row['Prob_Pos']
		snlpScore = row['Score']
	
		if (-0.6<polarityScore <= -0.2):
			data.ix[index,'Polarity_Sent'] = "Negative"
		elif (-0.2<polarityScore <= +0.2):
			data.ix[index,'Polarity_Sent'] = "Neutral"
		elif (+0.2<polarityScore <= +0.6):
			data.ix[index,'Polarity_Sent'] = "Positive"
		elif (+0.6<polarityScore <= 1):
			data.ix[index,'Polarity_Sent'] = "VeryPositive"
		
		if (0.2< nbScore  <= 0.4):
			data.ix[index,'NB_Sent'] = "Negative"
		elif (0.4< nbScore  <= +0.6):
			data.ix[index,'NB_Sent'] = "Neutral"
		elif (+0.6< nbScore  <= +0.8):
			data.ix[index,'NB_Sent'] = "Positive"
		elif (+0.8< nbScore  <= 1):
			data.ix[index,'NB_Sent'] = "VeryPositive"
		
		if (snlpScore == 1):
			data.ix[index,'SNLP_Sent'] = "Negative"
		elif (snlpScore == 2):
			data.ix[index,'SNLP_Sent'] = "Neutral"
		elif (snlpScore == 3):
			data.ix[index,'SNLP_Sent'] = "Positive"
		elif (snlpScore == 4 or snlpScore == 5):
			data.ix[index,'SNLP_Sent'] = "VeryPositive"
		#print index, " ", text, " ",wordcount
		#print (data.ix[index,'Polarity_Sent'])

assignLabels()
# Now, get the aggregate percentage

colSequence = ['VeryNegative','Negative','Neutral','Positive','VeryPositive']
polaritySummary = data.pivot_table(index='Speaker', columns='Polarity_Sent', aggfunc = 'size', fill_value=0)
polaritySummary = polaritySummary.reindex(columns=colSequence)
print(polaritySummary.describe())
print(polaritySummary.head(5))

NBSummary = data.pivot_table(index='Speaker', columns='NB_Sent', aggfunc = 'size', fill_value=0)
NBSummary = NBSummary.reindex(columns=colSequence)

SNLPSummary = data.pivot_table(index='Speaker', columns='SNLP_Sent', aggfunc = 'size', fill_value=0)
SNLPSummary = SNLPSummary.reindex(columns=colSequence)
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
#Remember that you need an index inthe pivottable
polaritySummary.to_csv("output/polaritySummary.csv")
NBSummary.to_csv("output/NBSummary.csv")
SNLPSummary.to_csv("output/SNLPSummary.csv")

data.to_csv("all_debates_all_sents.csv", index = False)

