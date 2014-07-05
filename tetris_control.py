from flask import Flask, render_template, request
from flask.ext.socketio import SocketIO, emit
import redis

app = Flask(__name__, static_folder='static', static_url_path='/static')
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

r = redis.Redis()


@app.route('/')
def index():
    return render_template('tetris_controller.html')


@app.route('/post', methods=['POST'])
def post():
    print request.form
    r.lpush('tetris', request.form['action'])
    return '{"msg":"ok"}'


@socketio.on('action', namespace='/test')
def test_message(message):
    print  message['data']
    r.lpush('tetris', message['data'])
    emit('action', {'data': message['data']}, broadcast=True)


@socketio.on('connect', namespace='/test')
def test_connect():
    pass


@socketio.on('disconnect', namespace='/test')
def test_disconnect():
    pass


if __name__ == '__main__':
    socketio.run(app, host="0.0.0.0")
