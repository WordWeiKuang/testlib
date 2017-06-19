import time, uuid, hashlib

def next_id():
    return '%015d%s000' % (int(time.time() * 1000), uuid.uuid4().hex)

def getuuid_32():
    return uuid.uuid4().hex

def registeger(name, passwd):
    sha1 = hashlib.sha1()
    sha1.update(name.encode('utf-8'))
    sha1.update(b':')
    sha1.update(passwd.encode('utf-8'))
    passwd = sha1.hexdigest()
    uid = next_id()
    sha1_passwd = '%s:%s' % (uid, passwd)
    passwd = hashlib.sha1(sha1_passwd.encode('utf-8')).hexdigest()
    s = '%s,%s,%s' %(uid, name, passwd)
    print(s)
    return s

if __name__=='__main__':
    registeger('admin', '123456')