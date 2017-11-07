// 
// awVJCNMw1To	JessCLevengood	1004	Music	367	71376	4.83	207	253	Xk8Yo4pzhWs	R14VRaaBFNM	Cne6pwjyQVk	wrWamyL4Azc	mPAeOlTvcmo	-ejKyQlwIaI	vUiLjtPtcmQ	mo3FQ4iBSpc	FOchEMY1K3w	fHA5SyyiU38	sd0C_Us31kk	_grJcfnCdMM	XrSsWqOxi2c	jJ3Jc6dxJ38

// find the top 10 rated videos in YouTube
val textFile = sc.textFile("4.txt")
val counts = textFile.filter{ x => {if(x.toString().split("\t").length >= 6) true else false} }.map(line=>{line.toString().split("\t")})
val pairs = counts.map(x => {(x(0),x(6).toDouble)})
val res=pairs.reduceByKey(_+_).map(item => item.swap).sortByKey(false).take(10)
val res=pairs.map(item => item.swap).sortByKey(false).take(10)

// find the top rated videos in YouTube
val textFile = sc.textFile("4.txt")
val counts = textFile.filter{ x => {if(x.toString().split("\t").length >= 6) true else false} }.map(line=>{line.toString().split("\t")})
val newcounts = counts.filter{x=> {if (x(2).replace(" ", "").toInt >1) true else false}}.map(line=>{(line(2).replace(" ", "").toInt,line(5).toInt)})
newcounts.coalesce(1).saveAsTextFile("qyyresult0")


// figure1 get distribution of categories of videos uploaded
val textFile = sc.textFile("4.txt")
val counts = textFile.filter{ x => {if(x.toString().split("\t").length >= 6) true else false} }.map(line=>{line.toString().split("\t")})
val pairs = counts.map(line=>{(line(3), 1)})
val res=pairs.reduceByKey(_+_).map(item => item.swap).sortByKey(false)
res.coalesce(1).saveAsTextFile("qyyresult1")

// figure2 get the uploading trend of YouTube videos
val textFile = sc.textFile("4.txt")
val counts = textFile.filter{ x => {if(x.toString().split("\t").length >= 6) true else false} }.map(line=>{line.toString().split("\t")})
val pairs = counts.map(line=>{(line(2).replace(" ", "").toInt, 1)})
val temp = pairs.map(x=>{((x._1/7).toInt,x._2)})
val res=temp.reduceByKey(_+_).sortByKey(false)
res.coalesce(1).saveAsTextFile("qyyresult2")

// figure3 get the distribution of YouTube video length
val textFile = sc.textFile("4.txt")
val counts = textFile.filter{ x => {if(x.toString().split("\t").length >= 6) true else false} }.map(line=>{line.toString().split("\t")})
val pairs = counts.map(line=>{(line(4).replace(" ", "").toInt, 1)})
val res=pairs.reduceByKey(_+_).sortByKey(false)
res.coalesce(1).saveAsTextFile("qyyresult3")

// figure 4 get the distribution of YouTube video length for most four popular categories
val textFile = sc.textFile("4.txt")
val counts = textFile.filter{ x => {if(x.toString().split("\t").length >= 6) true else false} }.map(line=>{line.toString().split("\t")})
val pairs = counts.map(line=>{(line(3),line(4).replace(" ", "").toInt, 1)})
val p1 = pairs.filter{x=>{if (x._1 == "Music") true else false}}.map(x=>{(x._2,x._3)})
val p2 = pairs.filter{x=>{if (x._1 == "Entertainment") true else false}}.map(x=>{(x._2,x._3)})
val p3 = pairs.filter{x=>{if (x._1 == "Comedy") true else false}}.map(x=>{(x._2,x._3)})
val p4 = pairs.filter{x=>{if (x._1 == "Sports") true else false}}.map(x=>{(x._2,x._3)})
val res1=p1.reduceByKey(_+_).sortByKey(false)
val res2=p2.reduceByKey(_+_).sortByKey(false)
val res3=p3.reduceByKey(_+_).sortByKey(false)
val res4=p4.reduceByKey(_+_).sortByKey(false)
res1.coalesce(1).saveAsTextFile("qyyresult4a")
res2.coalesce(1).saveAsTextFile("qyyresult4b")
res3.coalesce(1).saveAsTextFile("qyyresult4c")
res4.coalesce(1).saveAsTextFile("qyyresult4d")

// figure7 video rank by popularity
val textFile = sc.textFile("4.txt")
val counts = textFile.filter{ x => {if(x.toString().split("\t").length >= 6) true else false} }.map(line=>{line.toString().split("\t")})
val newcounts = counts.map(line=>{(line(2).replace(" ", "").toInt,line(5).toInt)})
val res = newcounts.sortBy(-_._2)
val tes = newcounts.sortBy(-_._1)
val result = res.zipWithIndex.collect()
val result1 = result.map(x=>{(x._2,x._1._2)})
val distData1 = sc.parallelize(result1)
distData1.coalesce(1).saveAsTextFile("qyyresult7")

// figure8 video rank by popularity
val textFile = sc.textFile("4.txt")
val counts = textFile.filter{ x => {if(x.toString().split("\t").length >= 6) true else false} }.map(line=>{line.toString().split("\t")})
val newcounts = counts.map(line=>{(line(2).replace(" ", "").toInt,line(5).toInt)})
val res = newcounts.sortBy(-_._2)
val tes = newcounts.sortBy(-_._1)
val result = res.zipWithIndex.collect()
val result1 = result.filter{x=>{if(x._1._1 > 709) true else false}}.map(x=>{(x._2,x._1._2)})
val result2 = result.filter{x=>{if(x._1._1 > 709 && x._1._1 <= 730) true else false}}.map(x=>{(x._2,x._1._2)})
val result3 = result.filter{x=>{if(x._1._1 > 709 && x._1._1 <= 723) true else false}}.map(x=>{(x._2,x._1._2)})
val result4 = result.filter{x=>{if(x._1._1 > 709 && x._1._1 <= 716) true else false}}.map(x=>{(x._2,x._1._2)})
val distData1 = sc.parallelize(result1)
val distData2 = sc.parallelize(result2)
val distData3 = sc.parallelize(result3)
val distData4 = sc.parallelize(result4)
distData1.coalesce(1).saveAsTextFile("qyyresult8a")
distData2.coalesce(1).saveAsTextFile("qyyresult8b")
distData3.coalesce(1).saveAsTextFile("qyyresult8c")
distData4.coalesce(1).saveAsTextFile("qyyresult8d")

