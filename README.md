# Data_Engineering_Project
 
 <img src='https://github.com/shvetsanton/Data_Engineering_Project/blob/master/Project%20Outline.png'>

## Step 1:

### API: https://darksky.net/

I streamed data from Dark Sky Api using my stream_dark_sky.py script. 

## Step 2:

I have my python script on an EC2 instance and I used Cron to stream weather data for four cities every twenty minutes.
The cities that I streamed data for are San Francisco, Walnut Creek, Santa Barbara, San Diego.

I used boto to store my unstructured data in an S3 bucket.

## Step 3: 

I spinned up an EMR cluster to read my data from my S3 bucket.
Then I used Spark to extracted the information I am interested in and stored it in 3rd Normal Form in Postgresql database.

I am able to keep my database up to date by having a .sh file on an EC2 instance that spins up a cluster, executes my python script to update my database, and finally shuts down my cluster.
I run the .sh script once a day to update my database.

## Step 4:

In order to get the statistics I am interested in I have a python script to do sql queries that return my desired output. 

## Step 5:

To display my statistics I made a static website using my S3 bucket. This website displays the average statistics and and a plot showing the daily average temperatures for each of the four cities over the entire period I've been streaming data.

The contents of my website get updated because I have my python script on an another EC2 instance that updates the statistics in my S3 bucket daily.

http://deprojectwebsite.s3-website-us-east-1.amazonaws.com

http://deprojectwebsite.s3-website-us-east-1.amazonaws.com/statsplot

http://deprojectwebsite.s3-website-us-east-1.amazonaws.com/statstable

## Comparing my system to the 8 Desired properties of a Big Data system:

### Robustness and fault tolerance: 

  The good: My system is not being run localy. If something happens with Spark my data is safe of Postgres. Even if my plots wont update one day the previous days results are still up on my website.
  
  The bad: I'm relying on AWS to run smoothly since my unstructured data is being dumped to S3 and my website is hosted there as well.

### Low latency reads and updates:

  The good: My statistics on my website are available instantaneously. Using Spark allows me to update my db fairly quickly if I decide to update it more than once a day.
  
  The bad: My data is not so big and hence I am able to get my query results quickly now. But if my data was much much larger I would also need to use Spark to get my statistics instead of just a regular python script. 

### Scalability:

  The good: Using AWS helps me scale up at any desired point. 
  
  The bad: Use Spark for step four would be the next goal. (Also to predict weather using a trained machine learning model when dealing with real time data)
  
### Generalization:
  
  The good: My steaming code actually allows me to stream all sorts of data (currently, hourly, daily, weekly, past, predict..)
  The bad:For now my system is built to only stream weather data and my data base has specific pre-set feature names and types.
 
### Extensibility:

  The good: It would be fairly easy to add more features to my database or to add another table if I decide to stream completely different data.

### Ad hoc queries:

  The good: Considering my data is stored in PostgreSQL running different queries to find new insights is really easy.

### Minimal maintenance:

  The good: Because of cron my entire system can technically run without me doing anything.
  
  The bad: Ideally I would want to lower the number of different cron jobs I have and use Airflow to schedule my automatic tasks to ensure my data is updated before I try to generate some new statistic. 

### Debuggability:
   
   The good: I am able to detect if my data is not streaming really easily, or if a cluster didn't start or terminated because of some reason. 
   
   The bad: Hard to say, any sort of Debugging in this field is difficult for me since I am new to this.


## Going Further:

For my Machine Learning component of the project I am using the SVM classifier to see if there is a noticable difference in the weather patterns between the four cities.

In order to visualize the results of this classifier I needed to use PCA to project data only on two features. 
I plan to update my static webpage with my SVM graph. 




