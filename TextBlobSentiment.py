#This is the TextBlob Sentiment Class used
from textblob import TextBlob
from textblob.sentiments import NaiveBayesAnalyzer
import pandas as pd

class TextBlobSentiment():
	def __init__(self, inputFileName,outputFileName):
		self.inputFileName = inputFileName
		self.outputFileName = outputFileName
		# TextBlob has 2 types of sentiment analysis implementations: PatternAnalyzer and NaiveBayesAnalyzer
#http://textblob.readthedocs.org/en/latest/advanced_usage.html#sentiment-analyzers

	#Calculate sentiments based on PatternAnalyzer
	def calculatePatternAnalyzerSentiments(self):
		debate = pd.read_csv(self.inputFileName)
		debate['PolarityPAScore']=0
		for index, row in debate.iterrows():
			text = str(row['Text'])
			blob = TextBlob(text)
			longest = 0
			mainSentiment = 0
			#If there are multiple sentences within a line, take the sentiment of the longest sentence 
			for sentence in blob.sentences:
				polarity =sentence.sentiment.polarity
				if (len(sentence)>longest):
					mainSentiment = polarity
					longest = len(sentence)
			debate.ix[index,'PolarityPAScore']= mainSentiment
		#Debug printing
		#print(debate.PolarityScore)
		print(debate.head(5))
		# Removed the index column, which appears as unnamed column if left True
		debate.to_csv(self.outputFileName, index = False)
	#Calculate sentiments based on NaiveBayesAnalyzer
	def calculateNBSentiments(self):
		debate = pd.read_csv(self.inputFileName)
		#Probability that it is a positive
		debate['Prob_Pos']=0
		debate['NB_Sent']='NA'
		for index, row in debate.iterrows():
			text = str(row['Text'])
			print(index, text)
			blob = TextBlob(text,analyzer = NaiveBayesAnalyzer())
			longest = 0
			mainSentiment = 0
			mainClassification = 'NA'
			#If there are multiple sentences within a line, take the sentiment of the longest sentence 
			for sentence in blob.sentences:
				p_pos =sentence.sentiment.p_pos
				classification = sentence.sentiment.classification
				
				if (len(sentence)>longest):
					mainSentiment = p_pos
					mainClassification = classification
					longest = len(sentence)
			debate.ix[index,'Prob_Pos']= mainSentiment
			debate.ix[index,'NB_Sent']= mainClassification
		#Debug printing
		print(debate.head(5))
		# Removed the index column, which appears as unnamed column if left True
		debate.to_csv(self.outputFileName, index = False)


