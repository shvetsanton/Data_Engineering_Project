import os
import yaml
import pandas as pd
from sqlalchemy import create_engine
import matplotlib
# Force matplotlib to not use any Xwindows backend.
matplotlib.use('Agg')

import matplotlib.pyplot as plt
import boto
from boto.s3.key import Key
import time

credentials = yaml.load(open(os.path.expanduser('~/.ssh/api_cred.yml')))

engine = create_engine('postgresql://{user}:{password}@{host}:5432/{dbname}'.format(**credentials['rds']))

stats = pd.read_sql('SELECT city, avg(temperature) as avg_temp from weather group by city order by city', engine)

stats.to_html('statstable.html')

conn = boto.connect_s3(host='s3.amazonaws.com')
mybucket = 'deprojectwebsite'
bucketobj = conn.get_bucket(mybucket)
k = Key(bucketobj)
k.key = 'statstable'
k.set_contents_from_filename('statstable.html', policy='public-read')


data = pd.read_sql('select city, avg(temperature) as avg_temp, extract(month from to_timestamp(time)) as month, extract(day from to_timestamp(time)) as day from weather group by city, month, day order by month, day', engine)
data = data.iloc[1:,:]

x = []
for i in range(len(set(data.day))):
    x.append(i)

y_sd = data[data['city'] == 'SanDiego'].avg_temp
y_sb = data[data['city'] == 'SantaBarbara'].avg_temp
y_sf = data[data['city'] == 'SanFrancisco'].avg_temp
y_wc = data[data['city'] == 'WalnutCreek'].avg_temp

plt.plot(x, y_sd, '-o', c='b', label='San Diego')
plt.plot(x, y_sb, '-o', c='m', label='Santa Barbara')
plt.plot(x, y_sf, '-o', c='g', label='San Francisco')
plt.plot(x, y_wc, '-o', c='r', label='Walnut Creek')

plt.xlabel('Days since data streaming started')
plt.ylabel('Average temperature')
plt.title('%s' % time.strftime('%x'))
plt.legend()
plt.savefig('statsplot.png')
k.key = 'statsplot'
k.set_contents_from_filename('statsplot.png', policy='public-read')