#!/usr/bin/python

import MySQLdb
from apiclient.discovery import build #pip install google-api-python-client
from apiclient.errors import HttpError #pip install google-api-python-client
from oauth2client.tools import argparser #pip install oauth2client
from Queue import *
from re import findall
def insertToDB(m_id,db, cursor):   
    # Prepare SQL query to INSERT a record into the database.
    sql = "INSERT IGNORE INTO VIDEO(ID, \
       CHANNELID) \
       VALUES ('%s', '%s' )" % \
       (m_id, 'xxxxx')
    try:
    # Execute the SQL command
      cursor.execute(sql)
    # Commit your changes in the database
      db.commit()
    except:
    # Rollback in case there is any error
      db.rollback()
    return cursor.rowcount
	
def getVideoInfo(youtube, m_id):
    # get video info;
	#m_id = 'w9ekuLueVN0'
    video_response = youtube.videos().list(
      id=m_id, 
	  part='contentDetails, snippet, statistics'
      ).execute()
    video_response
    temp = video_response.get("items", [])
    info = []
    if temp:
      if not temp[0]["statistics"].get("commentCount",[]):
       commentCount = -1
      else:
       commentCount = temp[0]["statistics"]["commentCount"]
      if not temp[0]["statistics"].get("likeCount",[]):
       likeCount = -1
      else:
       likeCount = temp[0]["statistics"]["likeCount"]
      if not temp[0]["statistics"].get("dislikeCount",[]):
       dislikeCount = -1
      else:
       dislikeCount = temp[0]["statistics"]["dislikeCount"]
      if not temp[0]["statistics"].get("viewCount",[]):
       viewCount = -1
      else:
       viewCount = temp[0]["statistics"]["viewCount"]
      #print m_id
      m_duration=iso8601_duration_as_seconds(temp[0]["contentDetails"]["duration"])
      
      info = [m_id, 
        temp[0]["snippet"]["publishedAt"],
        temp[0]["snippet"]["channelId"],
        m_duration,
        temp[0]["snippet"]["categoryId"],
        viewCount,
        commentCount, # comment is disabled
        likeCount, 
        dislikeCount]
      #print info
    return info
	
def getRelatedVideo(youtube, m_id,max_results):	
	search_response = youtube.search().list(
	#q=options.q,
	type="video",
	part="id",
	relatedToVideoId=m_id,
	maxResults=max_results
	).execute()
	temp = []
	for search_result in search_response.get("items", []):
		if search_result["id"]["kind"] == "youtube#video":
			temp.append(search_result["id"]["videoId"])
			#print(search_result["id"]["videoId"])
	return temp
def getPopularVideo(youtube, pbDate, pdEnd,max_results):	
	search_response = youtube.search().list(
	#q=options.q,
	type="video",
	part="id",
	order="rating",
	publishedAfter= pbDate,
    publishedBefore=pdEnd,
	maxResults=max_results
	).execute()
	temp = []
    #print search_response
	for search_result in search_response.get("items", []):
		if search_result["id"]["kind"] == "youtube#video":
			temp.append(search_result["id"]["videoId"])
			#print(search_result["id"]["videoId"])
	return temp	
	
def goToNextLayer(input_queue,youtube,max_results,cursor,db,f):
    q = Queue()
    while not input_queue.empty():
        vid = input_queue.get()
        info = getVideoInfo(youtube,vid)
        print(info)
        if info:
            for i in info:
                f.write(str(i)+'\t')
            
            rvset= getRelatedVideo(youtube,vid, max_results)
            for i in rvset:
                f.write(str(i)+'\t')    
                if (insertToDB(i,db,cursor) != 0):
                    q.put(i)
            f.write('\n')
    return q

def iso8601_duration_as_seconds( d ):
    if d[0] != 'P':
        raise ValueError('Not an ISO 8601 Duration string')
    seconds = 0
    # split by the 'T'
    for i, item in enumerate(d.split('T')):
        for number, unit in findall( '(?P<number>\d+)(?P<period>S|M|H|D|W|Y)', item ):
            # print '%s -> %s %s' % (d, number, unit )
            number = int(number)
            this = 0
            if unit == 'Y':
                this = number * 31557600 # 365.25
            elif unit == 'W': 
                this = number * 604800
            elif unit == 'D':
                this = number * 86400
            elif unit == 'H':
                this = number * 3600
            elif unit == 'M':
                # ambiguity ellivated with index i
                if i == 0:
                    this = number * 2678400 # assume 30 days
                    # print "MONTH!"
                else:
                    this = number * 60
            elif unit == 'S':
                this = number
            seconds = seconds + this
    return seconds
		
def goToLeafLayer(input_queue,youtube,cursor,db,f):
    while not input_queue.empty():
       vid = input_queue.get()
       info = getVideoInfo(youtube,vid)
       #print(info)
       if info:
         for i in info:
           f.write(str(i)+'\t')
         f.write('\n')
	
def main():
  # my code here
  KEYS =["AIzaSyAOBdqXlr4wxFU4vlzY0dG7bY","AIzaSyBDhjab1cT1GSm5L3yt7GTb3C-X9-CSo",
                 "AIzaSyBtX-HPEtBHbiT2xSmnME84fDuxZtezNM","99",
		 "AIzaSyBBOZom7Tph_BzcScZ0","AIzaSyDbCcpV8w7pOpacs0Ysh_DFyPgQs",
		 "AIzaSyDwpYRmE8CUVwU7nN0Q","AIzaSyB0Ci1K6rK4nZiKG8u_QQZivPA",
		 "AIzaSyA0qXKPDamaX3pgFmOv5qGs","AIzaSyAP4myIa3S0fejctLpuWj9c",
                 "AIzaSyB-ciwiXOoono2jIzpglPvs"]
  DEVELOPER_KEY = KEYS[0] 
  YOUTUBE_API_SERVICE_NAME = "youtube"
  YOUTUBE_API_VERSION = "v3"
  
  search_max_results = 45
  relatedToVideo_max_results = 45
  depth = 2
  
  # Open database connection
  db = MySQLdb.connect("localhost","qyy","password","testdb" )
  cursor = db.cursor()
  # Drop table if it already exist using execute() method.
  #cursor.execute("DROP TABLE IF EXISTS VIDEO")
  # Create table as per requirement
  #sql = "CREATE TABLE VIDEO (\
  #       ID  CHAR(11) NOT NULL,\
#		 CHANNELID CHAR(11),\
 #        PRIMARY KEY (ID) )"
  #cursor.execute(sql)
  # prepare a cursor object using cursor() method
  pbDateToday = "2017-04-27T00:00:00Z"
  pbDateMonth = "2017-04-01T00:00:00Z"
  pbDateThisYear = "2017-01-01T00:00:00Z"
  pbDateOneYear="2016-01-01T00:00:00Z"
  pbDateTwoYear="2015-01-01T00:00:00Z"
  pbDateThreeYear="2014-01-01T00:00:00Z"
  pbDateFourYear="2013-01-01T00:00:00Z"
  pdDataFiveYear="2012-01-01T00:00:00Z"
  pbDateSixYear="2011-01-01T00:00:00Z"
  pbDateAllTheTime = "2005-02-14T00:00:00Z"
  Dates=[pbDateToday,pbDateMonth,pbDateThisYear,pbDateOneYear,pbDateTwoYear,pbDateThreeYear,pbDateFourYear,pdDataFiveYear,pbDateSixYear,pbDateAllTheTime]
  f = open('resultfile.txt', 'a')
  for mindex in range(0,len(Dates)-1):
    endTime = Dates[mindex]
    startTime=Dates[mindex+1] 
    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=KEYS[mindex])	
    seedList = getPopularVideo(youtube, startTime, endTime,search_max_results)
    resultQueue = Queue()
    for m_id in seedList:
       #m_id = 'wjyZzVxS5sY'
       #result = getVideoInfo(youtube,m_id)
       insertToDB(m_id,db,cursor)
       #print result
       resultQueue.put(m_id)  
    for i in range(depth):
      resultQueue = goToNextLayer(resultQueue,youtube,relatedToVideo_max_results,cursor,db,f)
      print resultQueue.qsize()
    goToLeafLayer(resultQueue,youtube,cursor,db,f)
  f.closed 		
  db.close()
  
if __name__ == "__main__":
  main()
