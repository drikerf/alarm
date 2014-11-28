import datetime, time, re
import redis

SLEEP = 1

r = redis.StrictRedis(host='localhost', port=6379, db=0)

def sound_alarm():
    '''Do something.'''
    while r.get('alarm'):
        print 'RING'
        # Ring until alarm is deleted.
    # Continue listening.
    listen()

def listen():
    ''' Listen for alarm.'''
    while True:
        alarm = r.get('alarm')
        if not alarm: continue
        tobj = datetime.time(*map(int, re.split('[^\d]', alarm)[:-1]))
        now = datetime.datetime.now().time()
        print tobj, now
        if now.hour == tobj.hour and now.minute == tobj.minute:    
            sound_alarm()
        time.sleep(SLEEP)

if __name__ == '__main__':
    listen()
