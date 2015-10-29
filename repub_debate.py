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

stopwordshearing = set(["mr","go","said","one","two","three","clip",
	"four","know","want","time","think","now","u","say","let","will","well","says","ph","ask","CROSSTALK","APPLAUSE"])


def repub_debate():
    if len(sys.argv) < 2:
        print "Run: python main.py < Input TextFileName>  <Output csv filename>[regex. patterns]"
        sys.exit(1)
    c = Transcript(sys.argv[1], sys.argv[2])
    c.open_file()
    c.feed_lists()
    c.write_transcript()
    data = pd.read_csv(sys.argv[2])
    print(data)
    # Print all the unique speakers to clean up any unwanted sentences and only keep speakers
    print(c.get_speakers())
    data = pd.read_csv(sys.argv[2])
    data = data [~data.Speaker.isin(['MALE','SANTELLI','(UNKNOWN)','UNIDENTIFIED MALE','HARMAN', 'HARWOOD','CRAMER','EPPERSON','QUICK','QUINTANILLA'])]
    print 'Unique Speakers: ', sorted(list(data.Speaker.unique()))
    #Count the number of words each speaker spoke
    def countWords(speaker):
        speakerData = data[data.Speaker == speaker]
        allText = ""
        for index, row in speakerData.iterrows():
        	allText += str(row['Text'])+" "

        words_all = len(allText.split())
        print 'Total words:   ',speaker,': ', words_all
    	
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

    generatewordcloud('KASICH', "images/kasich.png", "images/wc_kasich.png");
    generatewordcloud("HUCKABEE", "images/huckabee.png", "images/wc_huckabee.png");
    generatewordcloud("BUSH", "images/bush.png", "images/wc_bush.png");
    generatewordcloud("RUBIO", "images/rubio.png", "images/wc_rubio.png");
    generatewordcloud("TRUMP", "images/trump.png", "images/wc_trump.png");
    generatewordcloud("CARSON", "images/carson.png", "images/wc_carson.png");
    generatewordcloud("FIORINA", "images/fiorina.png", "images/wc_fiorina.png");
    generatewordcloud("CRUZ", "images/cruz.png", "images/wc_cruz.png");
    generatewordcloud("CHRISTIE", "images/christie.png", "images/wc_christie.png");
    generatewordcloud("PAUL", "images/paul.png", "images/wc_paul.png");
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
    generateoverallwordcloud("images/RepublicanLogo.png", "images/wc_rep_debate3.png");
    
    #Count the number of words by each party member
    def getWords(speaker):
        global stopwordshearing
        speakerData = data[data.Speaker == speaker]
        allText = ""
        for index, row in speakerData.iterrows():
        	allText += str(row['Text']).lower()+" "
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
	# Separate dataframes by Republican and Democrat's word frequencies
    df_dict ={}
    for name in data.Speaker.unique():
        df_dict[name] = getWords(name)
        print df_dict[name].head()
    #dwc = getWords("D")
    
if __name__ == "__main__":
    repub_debate()
