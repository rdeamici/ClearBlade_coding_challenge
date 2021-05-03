# ClearBlade_coding_challenge
coding challenge for clearblade summer internship 2021

# Summary
The challenge was to send system information from a raspberry pi to the ClearBlade platform at regular intervals,
store the information in a Collection(s) and run some analytics on the data at regular intervals, publishing the results to the 'analytics' topic

The code is broken up into 2 categories: code running on the raspberry pi, and code running on the ClearBlade platform, known as Code Services

## Raspberry pi code:
The code that runs on the raspberry pi is the python files. The driver code is `collect_data_and_send_to_clearblade.py`.

This code imports the file `sysinfo.py` which does the work of collecting the data. The data collected includes:

  1. device temperature
  2. total RAM usage
  3. number of currently running processes
  4. list of bluetooth devices in range of device

The data is broken up into 2 groups: system information, and bluetooth device information.
The system information includes all above information, except it only reports the total number of ble devices currently in range.
The bluetooth device information reports the address and name(if applicable) of all devices currently in range.

System information is published to the `sysinfo` topic.

Bluetooth deivce information is published to the `ble/_platform` topic.

**NOTE:** `collect_data_and_send_to_clearblade.py` is set to execute every 10 minutes locally on the r-pi as a cron job.


## ClearBlade Code Services
The Code Services are all the javascript files. These scripts are all triggered by various events as they are detected on the platform.
The events include:
  1. message published to topic `ble/_platform`
  2. message published to topic `sysinfo`
  3. a new hour of the day (this event is a timer, not a trigger)

### 1. message published to `ble/_platform`
When a message is published to this topic, the script `bleDevices.js` is triggered and executes. 
This script retrieves the information sent from the rapsberry pi and stores it in the `ble_devices` Collection.
This Collection only contains rows with unique bluetooth addresses. 
If a message comes in with a bluetooth address that has already been stored in the Collection, no new row is created.

### 2. messages published to `sysinfo`
When a message is published to this topic, the `sysinfo.js` script is triggered and executes.
The script retrieves the system information reported by the raspberry pi, and stores it in the `rPISystemInformation` Collection.
This collection can be thought of as a log of the raspberry pi system over time. 
Every message published to this topic results in a new row being added to this Collection.

### 3. analytics run every hour on the hour
The script `rpi_analytics.js` is set on a timer to be executed every hour on the hour. 
This script publishes summaries of the raspberry pi's system information from the past hour to the `analytics` topic.

The summaries reported include:
  1. RAM usage info as a percentage of total RAM. This is useful to monitor when a r-pi might need to flush it's memory or get a memory upgrade
  2. average number of processes running. This is useful to monitor when the number of processes changes drastically.
  3. temperature information. The highest temp and the average temp is calculated, and the difference between the two is also reported. 
  This is useful for detecting when a machine might be running too hot, so pre-emptive measures can be taken to keep the device from being destroyed.
  4. new bluetooth device information. This message is indicates which new devices come in range of the r-pi.
  This information could prove useful for systems where the raspberry pi is regularly communicating with various bluetooth devices as they come in range.

## areas for improvement

1. reporting bluetooth devices in range of rpi: 

    Within the script that stores information in the ble_devices Collection, 
    it would be better first query this Collection with the address of the most recently reported ble device. If the current device is already stored
    in the Collection, we should update the timestamp. This way we can keep track of the last time each device was in range of the raspberry-pi.
    The current setup stores the time when the ble device was first in range of the r-pi. 
    
    We should keep track of both timestamps, original time, and most recent time.
    
    another issue I noticed is that it appears some bluetooth device addresses are being created dynamically. This leads to hundreds of "new devices"
    being reported every hour, which is not accurate. No immediate solution jumps out to me for this issue.

2. extrapolate raspberry pi static information from `rPISystemInformation` Collection: 
    Currently the `rPISystemInformation` Collection includes columns for the raspberry pi model and serial number, as well as the max RAM capacity.
    This information is not likely to change much, so it should be stored in a separate collection. 
    This collection would include a single row for each raspberry pi device. 
    Then each raspberry pi could have it's own `SystemInformation` Collection,
    or each row in the `rPISystemInformation` Collection could include a single column containing the device_id of each raspberry pi device that 
    created the information in that row.

3. analytics could be more interesting:
    Right now the analytics beingrun are fairly basic. It would be better to compute more interesting metrics.
    For example, it would be good to compute increases compared to the past hour/day/week for data like temperature and RAM usage.
    If this information was computed it would be easier to predict potential issues ahead of time. For example, if the RAM usage is currently at 50%,
    but it increased to that point drastically (in the past hour or day) that would indicate we should get ahead of the issue and detect what caused the jump.
    If the RAM usage has hovered around 50% for weeks or months, that would indicate the device is in a stable configuration and no actions are needed.

## FINAL COMMENTS
I had an absolute blast working with this technology. It took me a longer than expected time to wrap my mind around how the system works.
I had to read the documentation over and over and search for other resources like the ClearBlade academy, which proved helpful.
I estimate I spent about 7-10 hours researching and reading documentation.

Onced I figured out how everything worked, programming the system was a real joy. I spent more time than I probably should have,
but I was enjoying myself so I spent probably another 5 hours developing.

I then spent another hour or two writing this documentation. I estimate the total time I spent on this challenge at 12-15 hours.

Thank you for giving me this opportunity! I enjoyed working with your technology and can already see so many applications in my own projects.




