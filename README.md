# YouTube Statistics Analysis with Spark

In this work, we perform a measurement study of the statistics YouTube videos with Spark in 2017. Previouse work [4] is out-of-date. We also develop a tool to get video data from YouTube server using the latest YouTube API. 
![Alt text](https://raw.githubusercontent.com/qyynuaa/YouTube-Statistics-Analysis-with-Spark/pic/platform.png)
We are trying to answer the following questions.

1. How to get the video info from YouTube?

2. How to analyze the data via spark?

3. What is the statistics of YouTube videos?

4. What is the relationship among YouTube video metrics?

First, we build a platform with YouTube API (v3) to collect the video information from YouTube server. Next we analyze those data via spark. Then we got statistics features of YouTube video and user behaviors. Finally, we analyze the relationship between YouTube metrics. We found that there is linear relation among like, dislike and comments.

The source code include the YouTube data crawler in python and data processing script with Spark.

References:

[1] http://spark.apache.org/

[2] https://developers.google.com/youtube/v3/getting-started

[3] http://netsg.cs.sfu.ca/youtubedata/

[4] Cheng, Xu, Cameron Dale, and Jiangchuan Liu. "Statistics and social network of youtube videos." Quality of Service, 2008. IWQoS 2008. 16th International Workshop on. IEEE, 2008.
