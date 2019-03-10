import json
from datetime import datetime

def serialize(serializable_object):
    if isinstance(serializable_object, datetime):
        return serializable_object.__str__()
    return serializable_object.__dict__

def convert_to_dict(serializable_object):
	return json.loads(json.dumps(serializable_object, default=serialize))