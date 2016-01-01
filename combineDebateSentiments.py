import pandas as pd
import matplotlib.pyplot as plt

import matplotlib
matplotlib.style.use('ggplot')

dem1 = pd.read_csv("sentiments/dem_debate1_textblob_sent.csv")
dem2 = pd.read_csv("sentiments/dem_debate2_textblob_sent.csv")
dem3 = pd.read_csv("sentiments/dem_debate3_textblob_sent.csv")
print(dem1.head(5))
print(dem2.head(5))


rep1 = pd.read_csv("sentiments/rep_debate1_textblob_sent.csv")
rep2 = pd.read_csv("sentiments/rep_debate2_textblob_sent.csv")
rep3 = pd.read_csv("sentiments/rep_debate3_textblob_sent.csv")
rep4 = pd.read_csv("sentiments/rep_debate4_textblob_sent.csv")
rep5 = pd.read_csv("sentiments/rep_debate5_textblob_sent.csv")

dem1['Type'] = 'dem1'
dem2['Type'] = 'dem2'
dem3['Type'] = 'dem3'

rep1['Type'] = 'rep1'
rep2['Type'] = 'rep2'
rep3['Type'] = 'rep3'
rep4['Type'] = 'rep4'
rep5['Type'] = 'rep5'

dem = dem1.append(dem2,ignore_index=True)
print(dem.head(5))
dem = dem.append(dem3,ignore_index=True)
rep = rep1.append(rep2,ignore_index=True)
rep = rep.append(rep3,ignore_index=True)
rep = rep.append(rep4,ignore_index=True)
rep = rep.append(rep5,ignore_index=True)

rep.to_csv("sentiments/rep_debates.csv", index = False)

alldebates = rep.append(dem,ignore_index=True)
alldebates.to_csv("sentiments/all_debates.csv",index = False)