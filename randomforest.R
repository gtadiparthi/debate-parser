
rm(list = ls())
graphics.off()

library(rpart)
library(rpart.plot)
library(randomForest)

setwd("/Users/gopalakrishnatadiparthi/Documents/PythonPrograms/debate-parser")
mydata = read.csv("wordfreq.csv")
word = mydata$word;
mydata$X=NULL
mydata$word = NULL
labels = colnames(mydata)

mydata1 = t(mydata)
mydata = as.data.frame(mydata1)

colnames(mydata) = paste("w",word,sep="_")


mydata$speaker = as.factor(labels)

rf1 = randomForest(speaker ~., data = mydata)
varImpPlot(rf1)

importance(rf1)
partialPlot(rf1, mydata,w_youll, speaker)

imp <- importance(rf1)
impvar <- rownames(imp)[order(imp[, 1], decreasing=TRUE)]
op <- par(mfrow=c(2, 3))
for (i in 1:10) {
  partialPlot(rf1, mydata, impvar[i], "TRUMP", xlab=impvar[i],
              main=paste("Partial Dependence on", impvar[i]))
} 
par(op)
