import numpy as np
import pandas as pd
from time import localtime, strftime
from sense_hat import SenseHat

FACTOR = 5.466
cpu_temp = int(open('/sys/class/thermal/thermal_zone0/temp').read()) / 1000

cols = ['date', 'time', 'humidity', 'temperature']
datetime_measured = strftime("%Y-%m-%d %I:%M:%S %p", localtime())
date_measured = strftime("%Y-%m-%d", localtime())
time_measured = strftime("%I:%M:%S %p", localtime())

sense = SenseHat()
temp = sense.get_temperature()
temp_calibrated = temp - ((cpu_temp - temp)/FACTOR)

hum = sense.get_humidity()

d = {'date':date_measured, 'time':time_measured, 'temperature':temp_calibrated, 'humidity': hum}
df = pd.DataFrame(data=d, index=[datetime_measured])
df = df[cols]
df.index.name = 'datetime'

with open('write.csv', 'a') as f:
    df.to_csv(f, header=False)

fixed_df = pd.read_csv('write.csv', sep=',', encoding='latin1', parse_dates=['datetime'], dayfirst=False, index_col='datetime')

#Plots the temp in the past 24 hours
plot_all = fixed_df[['temperature', 'humidity']].plot()
fig_all = plot_all.get_figure()
fig_all.savefig("Measurements_All.png")

#Plots the temp in the past 24 hours
plot_24 = fixed_df[['temperature', 'humidity']].tail(24).plot()
fig_24 = plot_24.get_figure()
fig_24.savefig("Measurements_24Hrs.png")
