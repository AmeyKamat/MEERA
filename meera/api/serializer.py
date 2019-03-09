from datetime import datetime

def serializer(o):
    if isinstance(o, datetime):
        return o.__str__()
    return o.__dict__