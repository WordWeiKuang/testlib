import time, uuid

def next_id():
    return '%015d%s000' % (int(time.time() * 1000), uuid.uuid4().hex)

def getuuid_32():
    return uuid.uuid4().hex
