import datetime
import redis
from flask import Flask
from flask.views import MethodView

# flask config.
app = Flask(__name__)

# redis config.
r = redis.StrictRedis(host='localhost', port=6379, db=0)

# views.
class Index(MethodView):
    '''index.'''

    def get(self):
        return 'index!'

class AlarmAPI(MethodView):
    '''alarm api.'''

    def get(self):
        '''get alarm current alarm.''' 
        return 'alarm!'

    def post(self):
        '''post alarm.'''
        d = {'hour': 13, 'minute': 28}
        now  = datetime.datetime.now()
        hours = d['hour'] - now.hour
        minutes = d['minute'] - now.minute
        if hours < 0: hours += 24
        if minutes < 0: minutes += 60
        seconds = hours*3600 + minutes*60 - now.second
        alarm = now + datetime.timedelta(seconds=seconds)
        r.set('alarm', alarm.isoformat())
        return 'Alarm set!\n'

    def delete(self):
        '''delete alarm.'''
        return 'NYI\n'

# register url rules.
app.add_url_rule('/', view_func=Index.as_view('index'))
app.add_url_rule('/alarm', view_func=AlarmAPI.as_view('alarm'))

if __name__ == '__main__':
    app.run(port=3000, debug=True)
