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

http://deprojectwebsite.s3-website-us-east-1.amazonaws.com/
http://deprojectwebsite.s3-website-us-east-1.amazonaws.com/statsplot.png




