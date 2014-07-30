import time
import locale

def convert_seconds_to_time(seconds):
	if not seconds:
		return "00:00:00"
	hours = int(seconds / 3600)
	seconds -= hours*3600
	minutes = int(seconds / 60)
	seconds -= minutes*60

	frmt = lambda x: ("0%d" if x < 10 else "%d") % x

	return "%s:%s:%s" % tuple(map(frmt, [hours, minutes, seconds]))

def convert_timestamp_to_time(timestamp):
	return time.strftime("%a %d %b %Y, %X", 
		time.localtime(timestamp)).decode(locale.getlocale()[1])