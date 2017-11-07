


data1 = read.table("Downloads/newdata.txt", header = TRUE)
str(data1)
data.use = data1[, -c(1, 3)]
str(data.use)
colnames(data.use) = c("uploadtime", "videoDuration", "categoryId", "viewCount", "commentCount", "likeCount", "dislikeCount")
#try plot
#videoDuration v.s. category
par(mar=c(7,5,1,1))
boxplot(log(videoDuration+2)~categoryId, data.use, xlab = "categoryId", ylab = "log(videoDuration)", main = "videoDuration v.s. category")
#viewcount v.s. category
boxplot(log(viewCount+2)~categoryId, data.use, xlab = "categoryId", ylab = "log(viewCount)", main = "viewcount v.s. category")

#covariance
cor(data.use[, -3])
# viewcount:likecount
plot(data.use$viewCount, data.use$likeCount, xlab = "viewcount", ylab = "likecount", main = "viewcount:likecount")
# commentCount:dislikeCount
plot(log(data.use$commentCount+2), log(data.use$dislikeCount+2), xlab = "log(commentCount)", ylab = "log(dislikeCount)", main = "commentCount:dislikeCount")


summary(data.use)
#seperate into uploadtime group div
data.use$timegroup = data.use$uploadtime %/% 500



ggplot(data=data.use,aes(x=log(videoDuration+1), group=timegroup, fill=timegroup)) + 
  geom_density(adjust=1.5 , alpha=0.2)
boxplot(log(videoDuration+1)~timegroup, data = data.use)


# Add a linear trend :
ggplot(data.use, aes(x=viewCount, y=likeCount)) +    geom_point(shape=1) +  geom_smooth(method=lm , color="red", se=FALSE)  # Add linear regression line 

ggplot(data.use, aes(x=log(data.use$commentCount+2), y=log(data.use$dislikeCount+2))) +    geom_point(shape=1) +  geom_smooth(method=lm , color="red", se=TRUE)  # Add linear regression line 


kk <- kmeans(data.use, centers = 6)
summary(kk)
summary(data1[data1$`kk$cluster`==5, ])

boxplot(V6~`kk$cluster`, data = data1)
hist(data1$V1)
cor(data1)
plot(data1$V3, data1$V5)



# ggplot2 library
library(ggplot2)

# Let's use the diamonds dataset
data(diamonds)
head(diamonds)
# ggplot(data=diamonds,aes(x=price, group=cut, fill=cut)) + 
#   geom_density(adjust=1.5)
ggplot(data=diamonds,aes(x=price, group=cut, fill=cut)) + 
  geom_density(adjust=1.5 , alpha=0.2)
