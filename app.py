import datetime, re, json
import redis
from flask import Flask, render_template, jsonify, request, abort
from flask.views import MethodView

# flask config.
app = Flask(__name__)

# redis config.
r = redis.StrictRedis(host='localhost', port=6379, db=0)

# views.
class Index(MethodView):
    '''index.'''

    def get(self):
        return render_template('index.html')

class AlarmAPI(MethodView):
    '''alarm api.'''

    def get(self):
        '''get alarm current alarm.'''
        alarm = r.hgetall('alarm')
        if alarm:
            tobj = datetime.time(*map(int, re.split('[^\d]', alarm['time'])[:-1]))
            response = {'hour': tobj.hour, 'minute': tobj.minute, 
                        'active': alarm['active']}
        else:
            response = {}
        return jsonify(response)

    def post(self):
        '''post alarm.'''
        d = json.loads(request.data)
        try:
            d = {key: int(value) for (key, value) in d.items()}
        except ValueError:
            abort(403)
        try:
            alarm = datetime.time(hour=d['hour'], minute=d['minute'])
        except ValueError:
            abort(403)
        r.hmset('alarm', {'time': alarm.isoformat(), 'active': 0})    
        res = 'Alarm set for %r !\n' % alarm.isoformat()
        return res

    def delete(self):
        '''delete alarm.'''
        res = 'Alarm %r deleted\n' % r.hgetall('alarm')
        r.delete('alarm')
        return res

# register url rules.
app.add_url_rule('/', view_func=Index.as_view('index'))
app.add_url_rule('/alarm', view_func=AlarmAPI.as_view('alarm'))

if __name__ == '__main__':
    app.run(port=3000, debug=True)
