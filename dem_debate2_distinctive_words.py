#This code has been rewritten for Python3
#Trying to find distinctive words

#Used the following link to learn:
# https://de.dariah.eu/tatom/feature_selection.html

#The purpose of this code is to 
# Read input from debate transcript
# Parse the debate transcript into the following fields:
# 1. Sentence No. 2. Paragraph No. 3. Speaker 4. Conversation Text


from __future__ import division
import codecs
import re
import operator
import sys
import json
import csv
import pandas as pd
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
from os import path
from PIL import Image, ImageFile
import numpy as np
import matplotlib.pyplot as plt
from transcript import *
import re, string

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import euclidean_distances
from sklearn.metrics.pairwise import cosine_similarity

import os
from sklearn.manifold import MDS
import nltk

table = str.maketrans("","",string.punctuation)

from sklearn.feature_extraction import text 

stop_words = text.ENGLISH_STOP_WORDS.union(["mr","go","said","one","two","three","clip",
	"four","know","want","time","think","now","u","say","let","will","well","says","ph","ask","crosstalk","applause",
	'did','does','just','lot','look','going','end','day', 'secretary','senator','thats','actually','john','weve','come','tell'])

stopwordshearing = set(["mr","go","said","one","two","three","clip",
	"four","know","want","time","think","now","u","say","let","will","well","says","ph","ask","CROSSTALK","APPLAUSE"])


def repub_debate():
	if len(sys.argv) < 2:
		print ("Run: python dem_debate2.py < csv file from get speakers>")
		sys.exit(1)
	data = pd.read_csv(sys.argv[1])
	print(data)
	#data = data [~data.Speaker.isin(['MALE','SANTELLI','(UNKNOWN)','UNIDENTIFIED MALE','HARMAN', 'HARWOOD','CRAMER','EPPERSON','QUICK','QUINTANILLA'])]
	#Filter list for 4th republican debate
	data = data [~data.Speaker.isin(['ANNOUNCER','MAJOR GARRETT','CORDES','OBRADOVICH','COONEY', 'DICKERSON'])]
	
	print (('Unique Speakers: ', sorted(list(data.Speaker.unique()))))
	#Count the number of words each speaker spoke
	def countWords(speaker):
		speakerData = data[data.Speaker == speaker]
		allText = ""
		for index, row in speakerData.iterrows():
			allText += str(row['Text'])+" "

		words_all = len(allText.split())
		print (('Total words:   ',speaker,': ', words_all))
		
	for name in data.Speaker.unique():
		countWords(name);
		
	def generatewordcloud(speaker, inputImageFileName, outputImageFileName):

		speakerData = data[data.Speaker == speaker]
		allText = ""
		for index, row in speakerData.iterrows():
			allText += str(row['Text'])+" "
	
		#print (allText)
		ImageFile.LOAD_TRUNCATED_IMAGES = True

		img = Image.open(inputImageFileName)
		img = img.resize((980,1080), Image.ANTIALIAS)

		speakerArray = np.array(img)
		sl = STOPWORDS | stopwordshearing
		
		wc = WordCloud(background_color="white", max_words=500, mask=speakerArray, stopwords=sl)
		wc.generate(allText)
		# create coloring from image
		image_colors = ImageColorGenerator(speakerArray)
		wc.recolor(color_func=image_colors)
		wc.to_file(outputImageFileName)
#Commenting out generating word cloud as I am testin gsomething else now
#	 generatewordcloud('KASICH', "images/kasich.png", "images/wc_kasich.png");
#	 generatewordcloud("HUCKABEE", "images/huckabee.png", "images/wc_huckabee.png");
#	 generatewordcloud("BUSH", "images/bush.png", "images/wc_bush.png");
#	 generatewordcloud("RUBIO", "images/rubio.png", "images/wc_rubio.png");
#	 generatewordcloud("TRUMP", "images/trump.png", "images/wc_trump.png");
#	 generatewordcloud("CARSON", "images/carson.png", "images/wc_carson.png");
#	 generatewordcloud("FIORINA", "images/fiorina.png", "images/wc_fiorina.png");
#	 generatewordcloud("CRUZ", "images/cruz.png", "images/wc_cruz.png");
#	 generatewordcloud("CHRISTIE", "images/christie.png", "images/wc_christie.png");
#	 generatewordcloud("PAUL", "images/paul.png", "images/wc_paul.png");
	def generateoverallwordcloud(inputImageFileName, outputImageFileName):

		allText = ""
		for index, row in data.iterrows():
			allText += str(row['Text'])+" "
	
		#print (allText)
		ImageFile.LOAD_TRUNCATED_IMAGES = True

		img = Image.open(inputImageFileName)
		img = img.resize((980,1080), Image.ANTIALIAS)

		speakerArray = np.array(img)
		sl = STOPWORDS | stopwordshearing
		
		wc = WordCloud(background_color="white", max_words=500, mask=speakerArray, stopwords=sl)
		wc.generate(allText)
		# create coloring from image
		image_colors = ImageColorGenerator(speakerArray)
		wc.recolor(color_func=image_colors)
		wc.to_file(outputImageFileName)
	#generateoverallwordcloud("images/RepublicanLogo.png", "images/wc_rep_debate3.png");
	
	#Count the number of words by each party member
	def getAllText(speaker):

		speakerData = data[data.Speaker == speaker]
		allText = ""
		for index, row in speakerData.iterrows():
			#s.translate(table, string.punctuation)
			allText += str(row['Text']).lower().translate(table)+" "
		allText = allText.replace("e-mail","email")
		allText = allText.replace("e- mail","email")
		allText = allText.replace("op-ed","oped")
		
		return allText
	def getOverAllText():

		speakerData = data
		allText = ""
		for index, row in speakerData.iterrows():
			#s.translate(table, string.punctuation)
			allText += str(row['Text']).lower().translate(table)+" "
		allText = allText.replace("e-mail","email")
		allText = allText.replace("e- mail","email")
		allText = allText.replace("op-ed","oped")
		
		return allText
		#Count the number of words in the entire transcript
	def getTotalWords():
		global stopwordshearing
		speakerData = data
		allText = ""
		for index, row in speakerData.iterrows():
			#s.translate(table, string.punctuation)
			allText += str(row['Text']).lower().translate(table)+" "
		allText = allText.replace("e-mail","email")
		allText = allText.replace("e- mail","email")
		allText = allText.replace("op-ed","oped")
		sl = STOPWORDS | stopwordshearing
		wc = WordCloud(background_color="white", max_words=2000,  stopwords=sl,
				random_state=42)
		
		wc.generate(allText)
		wcdf = pd.DataFrame(wc.words_)
		wcdf.columns = ["word","Total"]
		return wcdf
	# Separate dataframes by Republican and Democrat's word frequencies
	df_list =[]
	speaker_list=[]
	i=1
	for name in data.Speaker.unique():
		df_list.append(getAllText(name))
		speaker_list.append(name)
	#print(df_dict)
	vectorizer = CountVectorizer(input='content',stop_words=stop_words)
	dtm = vectorizer.fit_transform(df_list)
	vocab = vectorizer.get_feature_names()
	
	candidates_count = pd.DataFrame(dtm.A, columns=vocab).transpose()
	
	candidates_count.columns=speaker_list
	#candidates_count['word'] = candidates_count.index


	print(candidates_count)
	
	dtm = dtm.toarray()
	vocab = np.array(vocab)
	rates = 100 * dtm / np.sum(dtm, axis=1, keepdims=True)	
	
	print(rates[:, 100:105])
	print(vocab[100:105])
	
	#Get overall frequencies for the entire debate transcript
	total_df_list = []
	total_df_list.append(getOverAllText())
	dtm1 = vectorizer.fit_transform(total_df_list)
	vocab1 = vectorizer.get_feature_names()
	
	total_count = pd.DataFrame(dtm1.A, columns=vocab1).transpose()
	total_count.columns = ['Total']
	#print(total_count)
	word_count = pd.concat([candidates_count,total_count], axis=1)
	
	cols = list(word_count.columns)
	print(cols)
	word_count['common']=1
	for name in cols:
		word_count[name+'_perc']= word_count[name]/word_count[name].sum()
		word_count['common'] = word_count['common']*word_count[name]
	for name in cols:
		word_count[name+'_index']= word_count[name+'_perc']-word_count['Total_perc']
		
	print(word_count)
	word_count['word']=word_count.index
	def generatewordcloud(freqTable, inputImageFileName, outputImageFileName):
		ImageFile.LOAD_TRUNCATED_IMAGES = True
		img = Image.open(inputImageFileName)
		img = img.resize((980,1080), Image.ANTIALIAS)
		sl = STOPWORDS | stopwordshearing
		speakerArray = np.array(img)
		wc = WordCloud(background_color="white", max_words=1000, prefer_horizontal =1,mask=speakerArray, stopwords=sl,
			random_state=42)
	
		wc.generate_from_frequencies(freqTable)
	#print wc.words_
	# create coloring from image
		image_colors = ImageColorGenerator(speakerArray)
		wc.recolor(color_func=image_colors)
		wc.to_file(outputImageFileName)

	def printTopWords():
			for name in speaker_list:
				clinton_condn = word_count[(word_count['common'] > 0)&(word_count[name]>3) &(word_count[name+'_index']>0)&(word_count[name+'_perc']>=0.003)]
				clinton_condn = clinton_condn.sort([name+'_index'], ascending=False)
				dfreq = clinton_condn[['word',name]]
				print(name)
				print (list(clinton_condn.sort([name+'_index'], ascending=False).head(20).word))
				dtuples = [tuple(x) for x in dfreq.values]
				#print(dtuples)
				generatewordcloud(dtuples, 'images/'+str.lower(name)+'.png', 'images/wc_'+str.lower(name)+'2.png');
			dem_wc = word_count.sort(['Total'],ascending=False)
			dfreq = dem_wc[['word','Total']]
			dtuples = [tuple(x) for x in dfreq.values]
			generatewordcloud(dtuples, 'images/DemocraticLogo.png', 'images/wc_DemocraticLogo2.png');


	printTopWords()
	dtm1 = dtm1.toarray()
	vocab1 = np.array(vocab1)
	rates1 = 100 * dtm1 / np.sum(dtm1, axis=1, keepdims=True)	
	print(rates1[:, 100:105])
	print(vocab1[100:105])
	
	
	
	sanders_indices, clinton_indices, omalley_indices = [], [],[]
	for index, fn in enumerate(speaker_list):
		if "SANDERS" in fn:
			sanders_indices.append(index)
		elif "CLINTON" in fn:
			clinton_indices.append(index)
		elif "OMALLEY" in fn:
			omalley_indices.append(index)
	sanders_rates = rates[sanders_indices, :]
	clinton_rates = rates[clinton_indices, :]
	omalley_rates = rates[omalley_indices, :]
	
	sanders_rates_avg = np.mean(sanders_rates, axis=0)
	clinton_rates_avg = np.mean(clinton_rates, axis=0)
	omalley_rates_avg = np.mean(omalley_rates, axis=0)
	
	distinctive_indices = (sanders_rates_avg * clinton_rates_avg * omalley_rates_avg) == 0
	#print(np.count_nonzero(distinctive_indices))
	ranking = np.argsort(sanders_rates_avg[distinctive_indices] + clinton_rates_avg[distinctive_indices] + omalley_rates_avg[distinctive_indices])[::-1]  # from highest to lowest; [::-1] reverses order.
	#print(vocab[distinctive_indices][ranking])
	
	#Removing these indices from the corpus
	
	dtm = dtm[:, np.invert(distinctive_indices)]
	rates = rates[:, np.invert(distinctive_indices)]
	vocab = vocab[np.invert(distinctive_indices)]
	#Recalucate the rates
	sanders_rates = rates[sanders_indices, :]
	clinton_rates = rates[clinton_indices, :]
	omalley_rates = rates[omalley_indices, :]

	sanders_rates_avg = np.mean(sanders_rates, axis=0)
	clinton_rates_avg = np.mean(clinton_rates, axis=0)
	omalley_rates_avg = np.mean(omalley_rates, axis=0)

if __name__ == "__main__":
	repub_debate()
