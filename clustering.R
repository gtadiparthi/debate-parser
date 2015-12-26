
rm(list = ls())
graphics.off()

setwd("/Users/gopalakrishnatadiparthi/Documents/PythonPrograms/debate-parser")
mydata = read.csv("wordfreq.csv")

word = mydata$word;
mydata$word = NULL
rownames(mydata)<-word
mydata1 = t(mydata)
mydata = mydata1
d = dist(mydata,method="euclidean")
fit = hclust(d, method="ward")

colLab <- function(n){
  if (is.leaf(n)){
    a<- attributes(n)
    attr(n, "label")<- substr(a$label, 1, 10)
    attr(n, "nodePar")<- c(a$nodePar, lab.col ='red')
  }
  n
}
require(graphics)
clusdendro = as.dendrogram(fit)
clusdendro = dendrapply(clusdendro, colLab)
op = par(mar=par("mar")+c(0,0,2))
plot(clusdendro)

groups <- cutree(fit , k =3)
rect.hclust(fit,k=3,border="red")
clusterdf = data.frame(groups)
table(clusterdf$groups)
