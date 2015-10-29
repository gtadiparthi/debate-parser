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
    print 'Unique Speakers: ', sorted(list(data.Speaker.unique()))
    #Count the number of words each speaker spoke
    def countWords(speaker):

        speakerData = data[data.Speaker == speaker]
        allText = ""
        for index, row in speakerData.iterrows():
        	allText += str(row['Text'])+" "

        words_all = sum([len(line.split()) for line in allText])
        print 'Total words:   ',speaker,': ', words_all
    	
    for name in data.Speaker.unique():
    	countWords(name);
    	
    def generatewordcloud(speaker, inputImageFileName, outputImageFileName):

        speakerData = data[data.Speaker == speaker]
        allText = ""
        for index, row in speakerData.iterrows():
        	allText += str(row['Text'])+" "
    
        print (allText)
        ImageFile.LOAD_TRUNCATED_IMAGES = True

        img = Image.open(inputImageFileName)
        img = img.resize((980,1080), Image.ANTIALIAS)

        speakerArray = np.array(img)
        wc = WordCloud(background_color="white", max_words=1000, mask=speakerArray, stopwords=STOPWORDS)
        wc.generate(allText)
        # create coloring from image
        image_colors = ImageColorGenerator(speakerArray)
        wc.recolor(color_func=image_colors)
        wc.to_file(outputImageFileName)

    #For Hillary Clinton
    #generatewordcloud("CLINTON", "images/clinton.png", "images/wc_clinton.png");
    #For Bernie Sanders
    #generatewordcloud("SANDERS", "images/sanders.png", "images/wc_sanders.png");
    #For Webb
    #generatewordcloud("WEBB", "images/webb.png", "images/wc_webb.png");
    #For Chafee
    #generatewordcloud("CHAFEE", "images/chafee.png", "images/wc_chafee.png");
    #For O'MALLEY
    #generatewordcloud("O'MALLEY", "images/omalley.png", "images/wc_omalley.png");

if __name__ == "__main__":
    repub_debate()
