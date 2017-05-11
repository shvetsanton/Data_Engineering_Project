import psycopg2
from functools import partial
from demjson import decode
from psycopg2 import IntegrityError, InternalError
from pyspark import SparkContext
from pyspark.sql import SparkSession



def current_data(city, raw_current):
    city = ''.join(city.split())
    time = raw_current['time']
    temperature = raw_current['temperature']
    precipProbability = raw_current['precipProbability']
    precipIntensity = raw_current['precipIntensity']
    pressure = raw_current['pressure']
    humidity = raw_current['humidity']
    visibility = raw_current['visibility']
    ozone = raw_current['ozone']
    cloudCover = raw_current['cloudCover']
    dewPoint = raw_current['dewPoint']

    return [city, time, temperature, precipProbability, precipIntensity, pressure, humidity,
            visibility, ozone, cloudCover, dewPoint]

def split_data(raw):
    test = []
    for key in raw.keys():
        test.append(current_data(key, raw[key]))
    return test


def insert(rows):
    total_count = 0
    if rows:
        conn = psycopg2.connect(**{'dbname': 'postgres',
                                   'host': 'postgresql-project.cj7ztqpujxwz.us-east-1.rds.amazonaws.com',
                                   'password': 'Kharkov62',
                                   'user': 'ashvets'})
        cur = conn.cursor()
        for datum in rows:
            datum = decode(datum)
            split_datum = split_data(datum)
            for row in split_datum:
                total_count += 1

                try:
                    cur.execute("INSERT INTO weather VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                                (row))
                    conn.commit()
                except (IntegrityError, InternalError) as e:  # prevents duplicates
                    cur.execute("rollback")
                    print('current # {}: {}'.format(total_count, row))


sc = SparkContext()
spark = SparkSession(sc)
raw_weather = sc.textFile("s3a://weatherstream2/*").cache()
raw_weather.foreachPartition(insert)
sc.stop()



