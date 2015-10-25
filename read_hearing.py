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
    #print(data)
    

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
        wc = WordCloud(background_color="white", max_words=1000, mask=speakerArray, stopwords=STOPWORDS)
        wc.generate(allText)
        print (wc.words_)
        # create coloring from image
        image_colors = ImageColorGenerator(speakerArray)
        wc.recolor(color_func=image_colors)
        wc.to_file(outputImageFileName)
    generatewordcloud("CLINTON", "images/clinton.png", "images/test_clinton.png");
if __name__ =="__main__":
    read_hearing()