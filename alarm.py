import datetime, time, re
import redis

r = redis.StrictRedis(host='localhost', port=6379, db=0)

while True:
    alarm = r.get('alarm')
    if not alarm: continue
    tobj = datetime.datetime(*map(int, re.split('[^\d]', alarm)[:-1]))
    dt = (tobj - datetime.datetime.now()).total_seconds();
    if dt <= 0:
        r.delete('alarm')
        alarm()
    time.sleep(10)

def alarm():
    '''Do something.'''
    print 'RING!'
