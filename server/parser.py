'''
    Copyright: Dumitrescu Alexandra - Jan 2024
'''
import re
import json

# the topic of the received messages must be <location/station>
def check_topic_format(topic : str) -> bool:
    pattern = re.compile("[^/]+/[^/]+")
    return not pattern.match(topic) == None

# the received payload should be a JSON
def check_json_payload(msg : str) -> bool:
    try:
        json.loads(msg)
    except:
        return False
    return True

# we ignore the values that are not numbers
def check_entry_format(key, value) -> bool:
    if isinstance(value, int) or isinstance(value, float):
        return True
    return False  