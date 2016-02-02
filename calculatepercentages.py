# Calculate the sum and row percentages 

import pandas as pd
import matplotlib.pyplot as plt


def processdf(df):
	
	df = df[df.Speaker.isin(['CARSON','FIORINA','PAUL','TRUMP','CHRISTIE','KASICH','BUSH','CRUZ',"O'MALLEY",'RUBIO','SANDERS','CLINTON'])]

	df['Sum'] = df['VeryNegative'] + df['Negative'] + df['Neutral'] + df['Positive'] + df['VeryPositive']
	df['VeryNegative'] /= df['Sum'] 
	df['Negative'] /= df['Sum'] 
	df['Neutral'] /= df['Sum'] 
	df['Positive'] /= df['Sum'] 
	df['VeryPositive'] /= df['Sum'] 
	df['N'] = df['VeryNegative']+df['Negative']
	df['P'] = df['VeryPositive']+df['Positive']
	#Deleting (dropping) certain columns from the dataframe
	del df['Sum']

	df = df.sort_values( by = ['P'])
	return df
	
polaritySummary = pd.read_csv("output/polaritySummary.csv")
polaritySummary = processdf(polaritySummary)
polaritySummary.to_csv("javascript/polaritySummary.csv", index = False)


NBSummary = pd.read_csv("output/NBSummary.csv")
NBSummary = processdf(NBSummary)
NBSummary.to_csv("javascript/NBSummary.csv", index = False)


SNLPSummary = pd.read_csv("output/SNLPSummary.csv")
SNLPSummary = processdf(SNLPSummary)
SNLPSummary.to_csv("javascript/SNLPSummary.csv", index = False)



