from io import StringIO
import csv
import matplotlib.pyplot as plt
import pandas as pd
import datetime


scsv = """dt,sal
2003-01-31,400
2004-01-31,500
2004-06-30,550
2004-11-30,800
2005-03-31,1300
2005-09-30,1800
2007-04-30,2700
2008-04-30,3200
2009-04-30,3600
2010-04-30,3700
2011-02-30,5700
2012-04-30,6100
2013-04-30,6500
2013-10-31,9000
2014-10-31,9600
2015-08-31,12500
2016-07-31,13000
2018-07-31,13000
2020-06-30,13700"""

f = StringIO(scsv)
salaries = pd.read_csv(f)

r = pd.date_range(start='2003-01-01', end='2021-01-01', freq="M", closed="left")
#salaries.set_index('dt').reindex(r).fillna(0.0).rename_axis('dt').reset_index()

plt.plot(salaries.dt, salaries.sal)


plt.show()
