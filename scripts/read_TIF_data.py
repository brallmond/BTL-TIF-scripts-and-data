import csv
import matplotlib.pyplot as plt
import numpy as np

DEBUG = False

def trim_date(input_string, date):
  return input_string.replace(date,"").replace(".000","")

def store_data_from_csv(infile, sensor, time, data):
  with open(infile, newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=',', quotechar='"')
    store_data = False
    count = -1
    for row in reader:
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
          time[sensor].append(trim_date(row[0], "2024/03/26 "))
        except KeyError:
          time[sensor] = []
          time[sensor].append(trim_date(row[0], "2024/03/26 "))


read_range_start = "11:00:20.000"
#read_range_end   = "11:01:42.000"
read_range_end   = "14:20:00.000"

# filename, filelabel
infiles = {
        "p_1_3_7" : "/eos/user/b/ballmond/TIF_data/pressure_1_3_7_03272024.csv",
        "p_1_3_8" : "/eos/user/b/ballmond/TIF_data/pressure_1_3_8_03272024.csv",
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

for sensor in sensors:
  print(f"entries for {sensor}: time {len(time[sensor])}, data {len(data[sensor])}")

fig, ax = plt.subplots(2, sharex=True)
for sensor in sensors:
  ax[0].plot(time[sensor], data[sensor], label=sensor, marker=".", markersize=3, linestyle="none")
ax[1].plot(time["p_1_3_8"], data[sensors[0]]-data[sensors[1]], 
        label=f"{sensors[0]} - {sensors[1]}", marker=".", markersize=3, linestyle="none", color="green")

ax[0].set_title("Pressure Measurements : Powered Test at -35ºC")
ax[0].set_ylabel("Pressure [millibar?]")
#ax[0].xaxis.set_major_locator(plt.MaxNLocator(10)) # reduce number of time labels
#ax[0].tick_params(axis='x', labelrotation=45)      # set the axis labels so they do not overlap
ax[0].legend()
ax[1].set_ylabel("Input-Output [millibar?]")
ax[1].tick_params(axis='x', labelrotation=45)      # set the axis labels so they do not overlap
ax[1].xaxis.set_major_locator(plt.MaxNLocator(10)) # reduce number of time labels
ax[1].legend()
plt.show()


