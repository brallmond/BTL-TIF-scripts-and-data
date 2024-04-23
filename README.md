# BTL-TIF-scripts-and-data

This is a repo to keep scripts (and important related data) for BTL-TIF-operations together and somewhat organized.

Scripts, or any file ending with .py, .sh, .C, or .not-csv, should be placed in the scripts directory.
Please add your name and script-execution instructions at the top.

Data, basically any file ending in .csv that you'd like to be kept with your scripts, should be placed in the data directory.
Please title your data file similarly to the existing data files.
For example, a file containing temperature data for sensor 98-8-5 from data collect on April 12th of 2024 should be titled
`temperature_98_8_5_041220214.csv`

If your file contains data from multiple sensors, write a descriptive name, and add a comment at the top of the csv file with the exact sensors used and your best description of their corresponding physical component (i.e. LYSO, heater, Cu housing, etc.)


# How to “Export as CSV” with TIF data

<img width="1030" alt="TIF MTRS Panel" src="https://github.com/brallmond/BTL-TIF-scripts-and-data/assets/32043198/7549dc81-a295-4220-9006-617f78f46e12">

### For pressure data

open a plot (click on a sensor, click “Plot”, click “Converted Value”)

select your viewing range

from the dropdown “Plot menu…”

select “Export as CSV”

check the box "Fill empty cells with previous values"

in the prompt, type the location on your eos space, should be something like this

\\cernbox-smb\eos\user\b\ballmond\filename.csv

### For temperature data

open a plot --> click on a sensor, click “Plot”, click “Plot Only This Channel” or "Plot Multiple Channels", second option should result in multi-column csv.

<img width="632" alt="help image 1" src="https://github.com/brallmond/BTL-TIF-scripts-and-data/assets/32043198/3692ff06-4a4e-42ee-8f8f-380617e3bab9">

select your viewing range --> Right click the graph display, click "Time Range," click "User Specified."

<img width="921" alt="help image 2" src="https://github.com/brallmond/BTL-TIF-scripts-and-data/assets/32043198/58777f9a-3ffb-4d58-8b4a-7454d2c2323c">

<img width="386" alt="help image 3" src="https://github.com/brallmond/BTL-TIF-scripts-and-data/assets/32043198/2a0f39f5-1c43-451c-b094-6a4878a4163d">

when the data you are viewing corresponds to the period of time you expect, right click the graph display, click "Other," and click "Export plot to CSV"

<img width="1030" alt="help image 4" src="https://github.com/brallmond/BTL-TIF-scripts-and-data/assets/32043198/2aef108f-055c-426e-804f-331ad62c4234">

check the box "Fill empty cells with previous values"

in the prompt, type the location on your eos space, should be something like this

`\\cernbox-smb\eos\user\b\ballmond\filename.csv`

<img width="632" alt="help image 5" src="https://github.com/brallmond/BTL-TIF-scripts-and-data/assets/32043198/40442028-a561-461d-982f-c0863c645155">


