#Run this program for every debate

#Running the program on python 3

#python sentimentByTextBlob.py dem_debate3_output.csv sentiments/dem_debate3_textblob_sent.csv

#python sentimentByTextBlob.py rep_debate1_output.csv sentiments/rep_debate1_textblob_sent.csv

from textblob import TextBlob
import pandas as pd
import sys
from TextBlobSentiment import *

def score_sentiment():
	if len(sys.argv) < 3:
		print ("Run: python sentimentByTextBlob.py <Input csv file>  <Output csv filename>")
		sys.exit(1)
	s = TextBlobSentiment(sys.argv[1], sys.argv[2])
	#Calculating sentiment based on the patternanalyzer
	s.calculatePatternAnalyzerSentiments()
if __name__ == "__main__":
	score_sentiment()



########### Code snippet to test a sentence or 2 ##########
# 
# text = '''
# A majority of the candidates on this stage have supported amnesty. I have never supported amnesty, and I led the fight against Chuck Schumer's gang of eight amnesty legislation in the Senate.
# '''
# blob = TextBlob(text)
# print(blob.tags)
# print(blob.noun_phrases)
# for sentence in blob.sentences:
# 	print(sentence.sentiment.polarity)