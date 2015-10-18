# Collapse the individual sentence
#Group them in sequences of multiple sentences and sentiments for each sentence
import pandas as pd
debate = pd.read_csv("dem_debate.csv")
sentiment = pd.read_csv("dem_debate_sentiment.csv")
data = pd.merge(debate,sentiment,on='SentenceNo')

data1=data.groupby(['SequenceNo'])['Score'].mean().reset_index()
data2=data.groupby(['SequenceNo'])['Text'].apply(lambda x: ','.join(x)).reset_index()
data3 = data.drop_duplicates(['SequenceNo','Speaker'])[['SequenceNo','Speaker']]
print(data1)
print(data2.head(5))
data12 = pd.merge(data1,data2,on='SequenceNo')
data = pd.merge(data3, data12, on ='SequenceNo')
print(data)

data.to_csv("final.csv", index_col = False)
# 
# 
# clinton = data[data.speaker == "CLINTON"]
# 
# print(clinton.text)
# 
# cs = ""
# for index, row in clinton.iterrows():
# 	cs += str(row['text'])+" "
#     
# print (cs)
# 
# 
# 
# from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
# from os import path
# from PIL import Image
# import numpy as np
# import matplotlib.pyplot as plt
# 
# from PIL import ImageFile
# ImageFile.LOAD_TRUNCATED_IMAGES = True
# 
# img = Image.open("hc.png")
# img = img.resize((980,1080), Image.ANTIALIAS)
# 
# 
# hcmask = np.array(img)
# #hcmask = scipy.ndimage.zoom(hcmask, 2, order=3)
# print(STOPWORDS)
# #wc = WordCloud(background_color="white", max_words=2000, mask=hcmask, stopwords=STOPWORDS)
# wc = WordCloud(background_color="white", max_words=2000, mask=hcmask, stopwords=STOPWORDS)
# wc.generate(cs)
# wc.to_file("wc2.png")
# 
# 
# #For Bernie Sanders
# 
# 
# clinton = data[data.speaker == "SANDERS"]
# 
# print(clinton.text)
# 
# cs = ""
# for index, row in clinton.iterrows():
# 	cs += str(row['text'])+" "
#     
# print (cs)
# 
# 
# 
# from wordcloud import WordCloud
# from wordcloud import STOPWORDS
# from os import path
# from PIL import Image
# import numpy as np
# import matplotlib.pyplot as plt
# 
# from PIL import ImageFile
# ImageFile.LOAD_TRUNCATED_IMAGES = True
# 
# img = Image.open("Untitled.png")
# img = img.resize((980,1080), Image.ANTIALIAS)
# 
# 
# hcmask = np.array(img)
# #hcmask = scipy.ndimage.zoom(hcmask, 2, order=3)
# print(STOPWORDS)
# #wc = WordCloud(background_color="white", max_words=2000, mask=hcmask, stopwords=STOPWORDS)
# wc = WordCloud(background_color="white", max_words=2000, mask=hcmask, stopwords=STOPWORDS)
# wc.generate(cs)
# wc.to_file("wc_sanders.png")
# 
# 
# #For Webb
# 
# 
# clinton = data[data.speaker == "WEBB"]
# 
# print(clinton.text)
# 
# cs = ""
# for index, row in clinton.iterrows():
# 	cs += str(row['text'])+" "
#     
# print (cs)
# 
# 
# 
# from wordcloud import WordCloud
# from wordcloud import STOPWORDS
# from os import path
# from PIL import Image
# import numpy as np
# import matplotlib.pyplot as plt
# 
# from PIL import ImageFile
# ImageFile.LOAD_TRUNCATED_IMAGES = True
# 
# img = Image.open("images/webb_photocopy.png")
# img = img.resize((980,1080), Image.ANTIALIAS)
# 
# 
# hcmask = np.array(img)
# #hcmask = scipy.ndimage.zoom(hcmask, 2, order=3)
# print(STOPWORDS)
# #wc = WordCloud(background_color="white", max_words=2000, mask=hcmask, stopwords=STOPWORDS)
# wc = WordCloud(background_color="white", max_words=2000, mask=hcmask, stopwords=STOPWORDS)
# wc.generate(cs)
# 
# # create coloring from image
# #image_colors = ImageColorGenerator(hcmask)
# #wc.recolor(color_func=image_colors)
# wc.to_file("images/wc_webb.png")