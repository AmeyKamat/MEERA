from datetime import datetime

def jsonDefault(o):
	if isinstance(o, datetime):
		return o.__str__()
	else:
		return o.__dict__