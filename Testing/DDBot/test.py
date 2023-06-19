from time import ctime
from datetime import datetime

start_time = "10:00:00"
end_time = "10:07:00"

# convert time string to datetime
t1 = datetime.strptime(start_time, "%H:%M:%S")
print('Start time:', t1.time())

t2 = datetime.strptime(end_time, "%H:%M:%S")
print('End time:', t2.time())

# get difference
delta = t2 - t1

# time difference in seconds
print(f"Time difference is {delta.total_seconds()} seconds")

# time difference in milliseconds
ms = delta.total_seconds() * 1000
print(f"Time difference is {ms} milliseconds")