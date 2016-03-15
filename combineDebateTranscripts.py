#Combine all debate transcripts into one single dataset and calculate sentiments 
#Use venv3 to run this code

# This dataset can be uniformly processed for sentiments or any other text processing

import pandas as pd
import matplotlib.pyplot as plt
import sys
from TextBlobSentiment import *

import matplotlib
matplotlib.style.use('ggplot')

dem1 = pd.read_csv("output/dem_debate1_output.csv")
dem2 = pd.read_csv("output/dem_debate2_output.csv")
dem3 = pd.read_csv("output/dem_debate3_output.csv")
dem4 = pd.read_csv("output/dem_debate4_output.csv")
dem5 = pd.read_csv("output/dem_debate5_output.csv")
dem6 = pd.read_csv("output/dem_debate6_output.csv")
dem7 = pd.read_csv("output/dem_debate7_output.csv")
dem8 = pd.read_csv("output/dem_debate8_output.csv")
print(dem1.head(5))
print(dem2.head(5))


rep1 = pd.read_csv("output/rep_debate1_output.csv")
rep2 = pd.read_csv("output/rep_debate2_output.csv")
rep3 = pd.read_csv("output/rep_debate3_output.csv")
rep4 = pd.read_csv("output/rep_debate4_output.csv")
rep5 = pd.read_csv("output/rep_debate5_output.csv")
rep6 = pd.read_csv("output/rep_debate6_output.csv")
rep7 = pd.read_csv("output/rep_debate7_output.csv")
rep8 = pd.read_csv("output/rep_debate8_output.csv")
rep9 = pd.read_csv("output/rep_debate9_output.csv")
rep10 = pd.read_csv("output/rep_debate10_output.csv")
rep11 = pd.read_csv("output/rep_debate11_output.csv")
rep12 = pd.read_csv("output/rep_debate12_output.csv")

dem1['Party'] = 'dem'
dem1['DebateNo'] = '1'
dem2['Party'] = 'dem'
dem2['DebateNo'] = '2'
dem3['Party'] = 'dem'
dem3['DebateNo'] = '3'
dem4['Party'] = 'dem'
dem4['DebateNo'] = '4'
dem5['Party'] = 'dem'
dem5['DebateNo'] = '5'
dem6['Party'] = 'dem'
dem6['DebateNo'] = '6'
dem7['Party'] = 'dem'
dem7['DebateNo'] = '7'
dem8['Party'] = 'dem'
dem8['DebateNo'] = '8'


rep1['Party'] = 'rep'
rep1['DebateNo'] = '01'
rep2['Party'] = 'rep'
rep2['DebateNo'] = '02'
rep3['Party'] = 'rep'
rep3['DebateNo'] = '03'
rep4['Party'] = 'rep'
rep4['DebateNo'] = '04'
rep5['Party'] = 'rep'
rep5['DebateNo'] = '05'
rep6['Party'] = 'rep'
rep6['DebateNo'] = '06'
rep7['Party'] = 'rep'
rep7['DebateNo'] = '07'
rep8['Party'] = 'rep'
rep8['DebateNo'] = '08'
rep9['Party'] = 'rep'
rep9['DebateNo'] = '09'
rep10['Party'] = 'rep'
rep10['DebateNo'] = '10'
rep11['Party'] = 'rep'
rep11['DebateNo'] = '11'
rep12['Party'] = 'rep'
rep12['DebateNo'] = '12'

dem = dem1.append(dem2,ignore_index=True)
print(dem.head(5))
dem = dem.append(dem3,ignore_index=True)
dem = dem.append(dem4,ignore_index=True)
dem = dem.append(dem5,ignore_index=True)
dem = dem.append(dem6,ignore_index=True)
dem = dem.append(dem7,ignore_index=True)
dem = dem.append(dem8,ignore_index=True)



rep = rep1.append(rep2,ignore_index=True)
rep = rep.append(rep3,ignore_index=True)
rep = rep.append(rep4,ignore_index=True)
rep = rep.append(rep5,ignore_index=True)
rep = rep.append(rep6,ignore_index=True)
rep = rep.append(rep7,ignore_index=True)
rep = rep.append(rep8,ignore_index=True)
rep = rep.append(rep9,ignore_index=True)
rep = rep.append(rep10,ignore_index=True)
rep = rep.append(rep11,ignore_index=True)
rep = rep.append(rep12,ignore_index=True)

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
