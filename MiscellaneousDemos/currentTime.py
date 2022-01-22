import datetime
	
# for timezone()
import pytz
	
# using now() to get current time
current = datetime.datetime.now(pytz.timezone('Asia/Kolkata'))
print(current)
current_time = current.strftime("%H:%M:%S")
print (current_time)
