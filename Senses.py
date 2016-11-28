import numpy as np
import pandas as pd
from time import localtime, strftime
from sense_hat import SenseHat

cols = ['date', 'time', 'humidity', 'temperature']
datetime_measured = strftime("%Y-%m-%d %I:%M:%S %p", localtime())
date_measured = strftime("%Y-%m-%d", localtime())
time_measured = strftime("%I:%M:%S %p", localtime())

sense = SenseHat()
temp = sense.get_temperature()
hum = sense.get_temperature_from_humidity()

d = {'date':date_measured, 'time':time_measured, 'temperature':temp, 'humidity': hum}
df = pd.DataFrame(data=d, index=[datetime_measured])
df = df[cols]
df.index.name = 'datetime'

with open('write.csv', 'a') as f:
    df.to_csv(f, header=False)


fixed_df = pd.read_csv('write.csv', sep=',', encoding='latin1', parse_dates=['datetime'], dayfirst=False, index_col='datetime')
fixed_df = fixed_df.tail(24)

#Plots the temp
plot_temp = fixed_df[['temperature', 'humidity']].plot()
fig_temp = plot_temp.get_figure()
fig_temp.savefig("Measurements.png")
