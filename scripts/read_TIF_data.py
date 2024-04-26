# clumsily cobbled together by Braden Allmond
# to use, set your filenames in the variable "infiles" then
# python3 read_TIF_data.py
# a nice plot with three lines should be made

import csv
import matplotlib.pyplot as plt
import numpy as np

DEBUG = False
date = "2024/04/11 " #Introduce the date of the test

def trim_date(input_string, date):
  return input_string.replace(date,"").replace(".000","")

def store_data_from_csv(infile, sensor, time, data):
  with open(infile, newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=',', quotechar='"')
    store_data = False
    count = -1
    for row in reader:
      #print(row)
      # row format: ['2024/03/26 16:24:20.000', '12.4446152549', '']
      if (DEBUG):
        count += 1
        if count > 50: break

      # only store data in specified time range
      if (read_range_start in row[0]): 
        store_data = True
        if DEBUG:  print(f"start time found: {read_range_start} | store_data = {store_data}")
      if (read_range_end in row[0]):
        store_data = False
        if DEBUG:  print(f"end time found: {read_range_end}     | store_data = {store_data}")

      if (store_data == True):
        #print(', '.join(row))
        try:
          data[sensor].append(float(row[1]))
        except KeyError:
          data[sensor] = []
          data[sensor].append(float(row[1]))

        try:
          time[sensor].append(trim_date(row[0], date))
        except KeyError:
          time[sensor] = []
          time[sensor].append(trim_date(row[0], date))


#Introduce the beginning and end of the test (time). 
#Note that for both csv's files have to be present those time values
read_range_start = "11:30:01.000"
#read_range_end   = "11:01:42.000"
read_range_end   = "13:20:01.000"

# filename, filelabel
infiles = {
        "p_1_3_7" : "/eos/user/c/cmunozdi/TIF_data/pressure_1_3_7_04112024.csv",
        "p_1_3_8" : "/eos/user/c/cmunozdi/TIF_data/pressure_1_3_8_04112024.csv",
          }

time = {}
data = {}

sensors = ["p_1_3_8", "p_1_3_7"]
for sensor in sensors:
  store_data_from_csv(infiles[sensor], sensor, time, data)
  time[sensor] = np.array(time[sensor])
  data[sensor] = np.array(data[sensor])
  print(f"entries for {sensor}: time {len(time[sensor])}, data {len(data[sensor])}")

# cleaning
print("Cleaning...")
remove_values_from_0 = []
for i, value in enumerate(time[sensors[0]]):
  if value not in time[sensors[1]]:
    remove_values_from_0.append(i)

remove_values_from_1 = []
for j, value in enumerate(time[sensors[1]]):
  if value not in time[sensors[0]]:
    remove_values_from_1.append(j)

print(f"n entries to remove from {sensors[0]} : {len(remove_values_from_0)}")
print(f"n entries to remove from {sensors[1]} : {len(remove_values_from_1)}")

time[sensors[0]] = np.delete(time[sensors[0]], remove_values_from_0)
data[sensors[0]] = np.delete(data[sensors[0]], remove_values_from_0)
time[sensors[1]] = np.delete(time[sensors[1]], remove_values_from_1)
data[sensors[1]] = np.delete(data[sensors[1]], remove_values_from_1)

#Adding another element in time and data dictionaries, for the difference p_1_3_7-p_1_3_8
time['diff'] = time['p_1_3_8']#time is the same
data['diff'] = data['p_1_3_7']-data['p_1_3_8']

for sensor in sensors:
  print(f"entries for {sensor}: time {len(time[sensor])}, data {len(data[sensor])}")

fig, ax = plt.subplots(2, sharex=True)
for sensor in sensors:
  ax[0].plot(time[sensor], data[sensor], label=sensor, marker=".", markersize=3, linestyle="none")
ax[1].plot(time["p_1_3_8"], data[sensors[1]]-data[sensors[0]], 
        label=f"{sensors[1]} - {sensors[0]}", marker=".", markersize=3, linestyle="none", color="green")

#Introduce times at rest (before the test)
rest_region_start = "11:30:01"
rest_region_end = "12:22:01"


#Introduce times of beginning and ending of the stabilized region
#when the heaters are 600W and temperature is stabilized also
stable_region_start = "12:34:01"
stable_region_end = "12:55:01"

#Making masks and arrays for the different regions
mask_rest = (time[sensors[0]] >= rest_region_start) & (time[sensors[0]] <= rest_region_end)
rest_data_diff = data['diff'][mask_rest]
mask_stable = (time[sensors[0]] >= stable_region_start) & (time[sensors[0]] <= stable_region_end)
stable_data_diff = data['diff'][mask_stable]

    

# Compute the Mean for the regions
mean_rest = np.mean(rest_data_diff)
mean_stable = np.mean(stable_data_diff)
print(f"Constant (mean) at rest region: {mean_rest}")
print(f"Constant (mean) at stable region: {mean_stable}")
print(f"Difference stable-rest:{mean_rest-mean_stable}")




#Adding vertical lines for rest and stabilized regions and fit lines
ax[0].axvline(x=rest_region_start, color='y', linestyle='--', linewidth=1)
ax[1].axvline(x=rest_region_start, color='y', linestyle='--', linewidth=1)
ax[0].axvline(x=rest_region_end, color='y', linestyle='--', linewidth=1)
ax[1].axvline(x=rest_region_end, color='y', linestyle='--', linewidth=1)
ax[0].axvline(x=stable_region_start, color='r', linestyle='--', linewidth=1)
ax[1].axvline(x=stable_region_start, color='r', linestyle='--', linewidth=1)
ax[0].axvline(x=stable_region_end, color='r', linestyle='--', linewidth=1)
ax[1].axvline(x=stable_region_end, color='r', linestyle='--', linewidth=1)
ax[1].axhline(mean_rest, color='y', linewidth=1)
ax[1].axhline(mean_stable, color='r', linewidth=1)

ax[0].set_title("Pressure Measurements : Powered Test at -35ºC")
ax[0].set_ylabel("Pressure [bar]")
#ax[0].xaxis.set_major_locator(plt.MaxNLocator(10)) # reduce number of time labels
#ax[0].tick_params(axis='x', labelrotation=45)      # set the axis labels so they do not overlap
ax[0].legend()
ax[1].set_ylabel("Input-Output [bar]")
ax[1].tick_params(axis='x', labelrotation=45)      # set the axis labels so they do not overlap
ax[1].xaxis.set_major_locator(plt.MaxNLocator(10)) # reduce number of time labels
ax[1].legend()
plt.show()


