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

stopwordshearing = set(["mr","go","said","one","two","three","clip",
	"four","know","want","time","think","now","u","say","let","will","well","says","ph","ask"])
class Transcript():
    def __init__(self, inputFileName,outputFileName):
        self.inputFileName = inputFileName
        self.outputFileName = outputFileName
        self.raw_messages = []
        self.speakerlist = []
        self.messagelist = []
        self.paragraphList = []

    def open_file(self):
        arq = codecs.open(self.inputFileName, "r", "utf-8-sig")
        content = arq.read()
        arq.close()
        lines = content.split("\n")
        lines = [l for l in lines if len(l) > 4]
        for l in lines:
            self.raw_messages.append(l.encode("utf-8"))

    def feed_lists(self):
        lineNo = 0
        seqNo = 0
        for l in self.raw_messages:
			#Typically, the transcript is in the following order: 
			# speaker:<space> message
            speaker, sep, message = l.partition(": ")
            lineNo += 1
            if message:
                self.speakerlist.append(speaker)
                self.messagelist.append(message)
                # store the previous speaker so that you can use it to print when there is only a line
                prevSender = speaker
                seqNo +=1
            else:
                self.speakerlist.append(prevSender)
                self.messagelist.append(l)
            self.paragraphList.append(seqNo)

    def write_transcript(self, end=0):
        if end == 0:
            end = len(self.messagelist)
        writer = csv.writer(open(self.outputFileName, 'w'))
        writer.writerow(["SentenceNo","SequenceNo","Speaker","Text"])
        for i in range(len(self.messagelist[:end])):
            writer.writerow([i,self.paragraphList[i],self.speakerlist[i], self.messagelist[i]])

    def get_speakers(self):
        speakers_set = set(self.speakerlist)
        return [e for e in speakers_set]

def read_hearing():
    if len(sys.argv) < 2:
        print "Run: python read_hearing.py < Input TextFileName>  <Output csv filename>[regex. patterns]"
        sys.exit(1)
    print ("I am here")
    c = Transcript(sys.argv[1], sys.argv[2])
    c.open_file()
    c.feed_lists()
    c.write_transcript()
    # Print all the unique speakers to clean up any unwanted sentences and only keep speakers
    print(c.get_speakers())
    data = pd.read_csv(sys.argv[2])
    print(data.Speaker.unique())
    
    party = pd.DataFrame({'Speaker':['GOWDY', 'CUMMINGS', 'CLINTON', 'ROSKAM', 'REP. DARRELL ISSA, R-CALIF.' ,'BROOKS' ,'DUCKWORTH' ,'ROBY' ,'SMITH', 'WESTMORELAND', 'POMPEO', 'SANCHEZ', 'ANDREA MITCHELL, MSNBC ANCHOR', 'MITCHELL', 'JORDAN' ,'SCHIFF', '(UNKNOWN)', 'CLERK' ,'UNKNOWN', 'ISSA'],
    						'Party':['R','D','O','R','O','R','D','R','D','R','R','D','O','O','R','D','O','O','O','R']})
    print(party)
    
    data = pd.merge(data, party, on = 'Speaker')
    def countWords(speaker):

        speakerData = data[data.Speaker == speaker]
        allText = ""
        for index, row in speakerData.iterrows():
        	allText += str(row['Text'])+" "

        words_all = sum([len(line.split()) for line in allText])
        print 'Total words:   ',speaker,': ', words_all
    	
    for name in data.Speaker.unique():
    	countWords(name);
    def countWordsParty(party):

        speakerData = data[data.Party == party]
        allText = ""
        for index, row in speakerData.iterrows():
        	allText += str(row['Text']).lower()+" "
        allText.replace("e-mail","email")
        words_all = sum([len(line.split()) for line in allText])
        print 'Total words:   ',party,': ', words_all
    	
    for name in data.Party.unique():
    	countWordsParty(name);
    	
# Code for wordclouds
    def getWords(party):
        global stopwordshearing
        speakerData = data[data.Party == party]
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
        wcdf.columns = ["word",party]
        return wcdf
        
    rwc = getWords("R")
    dwc = getWords("D")
    rdwc = pd.merge(rwc, dwc, on = "word", how='outer')
    rdwc=rdwc.fillna(0)
    print 'Top 5 Repub words'
    print rdwc.sort(['R'],ascending=0).head(5)
    print 'Top 5 Dem words'
    print rdwc.sort(['D'],ascending=0).head(5)
    print rdwc.D.median()
    print rdwc.R.median()
    
    RMedian = rdwc.R.median()
    DMedian = rdwc.D.median()
    
    cond1 = rdwc['R'] > RMedian 
    cond2 = rdwc['D'] < DMedian 
    
    rfreq = rdwc[cond1 & cond2][['word','R']]
    cond1 = rdwc['R'] < RMedian 
    cond2 = rdwc['D'] > DMedian 
    dfreq = rdwc[cond1 & cond2][['word','D']]

    print 'Top 5 Repub only words'
    print rfreq.sort(['R'],ascending=0).head(5)
    print 'Top 5 Dem only words'
    print dfreq.sort(['D'],ascending=0).head(5)
    #Convert dataframe to array of tuples
    rtuples = [tuple(x) for x in rfreq.values]
    dtuples = [tuple(x) for x in dfreq.values]
    #Code for wordclouds
    def generatewordcloud(freqTable, inputImageFileName, outputImageFileName):
        global stopwordshearing
        
        ImageFile.LOAD_TRUNCATED_IMAGES = True

        img = Image.open(inputImageFileName)
        img = img.resize((980,1080), Image.ANTIALIAS)
        sl = STOPWORDS | stopwordshearing
        speakerArray = np.array(img)
        wc = WordCloud(background_color="white", max_words=1000, mask=speakerArray, stopwords=sl,
                random_state=42)
        
        wc.generate_from_frequencies(freqTable)
        #print wc.words_
        # create coloring from image
        image_colors = ImageColorGenerator(speakerArray)
        wc.recolor(color_func=image_colors)
        wc.to_file(outputImageFileName)

    #For Hillary Clinton
    generatewordcloud(rtuples, "images/RepublicanLogo.png", "images/wc_RepublicanLogo.png");
    generatewordcloud(dtuples, "images/DemocraticLogo.png", "images/wc_DemocraticLogo.png");
    def generatewordcloud(speaker, inputImageFileName, outputImageFileName):
        global stopwordshearing
        speakerData = data[data.Speaker == speaker]
        allText = ""
        for index, row in speakerData.iterrows():
        	allText += str(row['Text']).lower()+" "
        allText = allText.replace("e-mail","email")
        allText = allText.replace("e- mail","email")
        allText = allText.replace("op-ed","oped")
        #print (allText)
        ImageFile.LOAD_TRUNCATED_IMAGES = True

        img = Image.open(inputImageFileName)
        img = img.resize((980,1080), Image.ANTIALIAS)

        speakerArray = np.array(img)
        sl = STOPWORDS | stopwordshearing
        wc = WordCloud(background_color="white", max_words=1000, mask=speakerArray,stopwords=sl,
                random_state=42)
        wc.generate(allText)
        # create coloring from image
        image_colors = ImageColorGenerator(speakerArray)
        wc.recolor(color_func=image_colors)
        wc.to_file(outputImageFileName)

    #For Hillary Clinton
    #generatewordcloud("CLINTON", "images/clinton.png", "images/wc_clinton_hearing.png");
if __name__ =="__main__":
    read_hearing()