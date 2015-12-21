# Cleaning this code to run on the 5th republican debate
# Using python 3
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
		print ("Run: python repub_debate.py < Input csv> ")
		sys.exit(1)

	data = pd.read_csv(sys.argv[1])
	print(data)

	#data = data [~data.Speaker.isin(['MALE','SANTELLI','(UNKNOWN)','UNIDENTIFIED MALE','HARMAN', 'HARWOOD','CRAMER','EPPERSON','QUICK','QUINTANILLA'])]
	#Filter list for 4th republican debate
	data = data [data.Speaker.isin(["SANDERS","CLINTON","O'MALLEY"])]
	
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
	def getWords(speaker):
		global stopwordshearing
		speakerData = data[data.Speaker == speaker]
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
		wcdf.columns = ["word",speaker]
		return wcdf
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
	df_dict ={}
	i=1
	for name in data.Speaker.unique():
		df_dict[name] = getWords(name)
		#print df_dict[name].head()
		if i == 1:
			rdwc = df_dict[name]
		else:
			rdwc = pd.merge(rdwc, df_dict[name], on = "word", how='outer')
		i += 1
	df_dict["Total"] = getTotalWords()
	rdwc = pd.merge(rdwc,df_dict["Total"], on = "word", how='outer')
	print (rdwc.head())
	rdwc=rdwc.fillna(0)
	rdwc.to_csv("wordfreq.csv")
	def getAllText(speaker):
		global stopwordshearing
		speakerData = data[data.Speaker == speaker]
		allText = ""
		for index, row in speakerData.iterrows():
			#s.translate(table, string.punctuation)
			allText += str(row['Text']).lower().translate(table)+" "
		allText = allText.replace("e-mail","email")
		allText = allText.replace("e- mail","email")
		allText = allText.replace("op-ed","oped")
		
		return allText
#Calculate using countvectorizer and also calculate the consine similarities
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
	dtm = dtm.toarray()
	vocab = np.array(vocab)
	dist = 1 - cosine_similarity(dtm)
	np.round(dist, 2)
	print(dist[0,1])
	print(dist[0,2])
	mds = MDS(n_components=2, dissimilarity="precomputed", random_state=1)
	pos = mds.fit_transform(dist)  # shape (n_components, n_samples)
	xs, ys = pos[:, 0], pos[:, 1]
	for x, y, name in zip(xs, ys, speaker_list):
		color = 'orange' if "CLINTON" in name else 'skyblue'
		plt.scatter(x, y, c=color)
		plt.text(x, y, name)
	plt.show()
	mds = MDS(n_components=3, dissimilarity="precomputed", random_state=1)
	pos = mds.fit_transform(dist)
	from mpl_toolkits.mplot3d import Axes3D
	fig = plt.figure()
	ax = fig.add_subplot(111, projection='3d')
	ax.scatter(pos[:, 0], pos[:, 1], pos[:, 2])
	for x, y, z, s in zip(pos[:, 0], pos[:, 1], pos[:, 2], speaker_list):
		ax.text(x, y, z, s)
	plt.show()
	
	from scipy.cluster.hierarchy import ward, dendrogram
	linkage_matrix = ward(dist)
	names = speaker_list
	dendrogram(linkage_matrix, labels=names)
	plt.tight_layout() 
	plt.show()
if __name__ == "__main__":
	repub_debate()
