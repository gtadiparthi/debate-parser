#Combine all debate transcripts into one single dataset and calculate sentiments 
#Use venv3 to run this code

# This dataset can be uniformly processed for sentiments or any other text processing

import pandas as pd
import matplotlib.pyplot as plt
import sys
from TextBlobSentiment import *

import matplotlib
matplotlib.style.use('ggplot')

dem1 = pd.read_csv("dem_debate1_output.csv")
dem2 = pd.read_csv("dem_debate2_output.csv")
dem3 = pd.read_csv("dem_debate3_output.csv")
dem4 = pd.read_csv("dem_debate4_output.csv")
print(dem1.head(5))
print(dem2.head(5))


rep1 = pd.read_csv("rep_debate1_output.csv")
rep2 = pd.read_csv("rep_debate2_output.csv")
rep3 = pd.read_csv("rep_debate3_output.csv")
rep4 = pd.read_csv("rep_debate4_output.csv")
rep5 = pd.read_csv("rep_debate5_output.csv")
rep6 = pd.read_csv("rep_debate6_output.csv")

dem1['Party'] = 'dem'
dem1['DebateNo'] = '1'
dem2['Party'] = 'dem'
dem2['DebateNo'] = '2'
dem3['Party'] = 'dem'
dem3['DebateNo'] = '3'
dem4['Party'] = 'dem'
dem4['DebateNo'] = '4'

rep1['Party'] = 'rep'
rep1['DebateNo'] = '1'
rep2['Party'] = 'rep'
rep2['DebateNo'] = '2'
rep3['Party'] = 'rep'
rep3['DebateNo'] = '3'
rep4['Party'] = 'rep'
rep4['DebateNo'] = '4'
rep5['Party'] = 'rep'
rep5['DebateNo'] = '5'
rep6['Party'] = 'rep'
rep6['DebateNo'] = '6'

dem = dem1.append(dem2,ignore_index=True)
print(dem.head(5))
dem = dem.append(dem3,ignore_index=True)
dem = dem.append(dem4,ignore_index=True)
rep = rep1.append(rep2,ignore_index=True)
rep = rep.append(rep3,ignore_index=True)
rep = rep.append(rep4,ignore_index=True)
rep = rep.append(rep5,ignore_index=True)
rep = rep.append(rep6,ignore_index=True)

alldebates = rep.append(dem,ignore_index=True)

#Change the order of columns in the pandas dataframe
columnsOrder = ['Party','DebateNo','SentenceNo',	'SequenceNo',	'Speaker',	'Text']
alldebates = alldebates.reindex(columns=columnsOrder)	

alldebates.to_csv("all_debates.csv",index = False)


#Calculate Sentiments

s = TextBlobSentiment("all_debates.csv", "all_debates_PAsent.csv")
#Calculating sentiment based on the patternanalyzer
s.calculatePatternAnalyzerSentiments()


s = TextBlobSentiment("all_debates.csv", "all_debates_NBsent.csv")
#Calculating sentiment based on the patternanalyzer
s.calculateNBSentiments()
