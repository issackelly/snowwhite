#!/usr/bin/env python


from flask import Flask, render_template, request
from flask.ext.socketio import SocketIO, emit
import redis
import random
import os

app = Flask(__name__, static_folder='static', static_url_path='/static')
app.config['SECRET_KEY'] = 'secret!'
app.debug = True
socketio = SocketIO(app)

r = redis.Redis()

images = []

for l in os.walk('/home/issackelly/images'):
    for i in l[2]:
        images.append('/home/issackelly/images/%s' % i)


gifs = []

STATIC = "/home/issackelly/Projects/art/snowwhite/static"

for l in os.walk('/home/issackelly/gifs'):
    for i in l[2]:
        gifs.append('/home/issackelly/gifs/%s' % i)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/tetris')
def tetris_controller():
    return render_template('tetris_controller.html')

@socketio.on('action', namespace='/mode')
def message(message):
    print  message['data']
    emit('action', {'data': message['data']}, broadcast=True)

    if message['data'] == 'image':
        r.set('stop_pattern', 'Yes')
        r.hset('patternargs', 'image', random.choice(images))
        r.set('pattern', message['data'])

    if message['data'] == 'gif':
        r.set('stop_pattern', 'Yes')
        r.hset('patternargs', 'gif', random.choice(gifs))
        r.set('pattern', message['data'])

    if message['data'] == 'white':
        r.set('stop_pattern', 'Yes')
        r.hset('patternargs', 'color', '255, 255, 255')
        r.set('pattern', 'color')

    else:
        r.set('stop_pattern', 'Yes')
        r.set('pattern', message['data'])



@socketio.on('connect', namespace='/controller')
def connect():
    pass


@socketio.on('disconnect', namespace='/controller')
def disconnect():
    pass


@socketio.on('action', namespace='/controller')
def message(message):
    print  message['data']
    r.lpush('tetris', message['data'])
    emit('action', {'data': message['data']}, broadcast=True)



@socketio.on('connect', namespace='/controller')
def connect():
    pass


@socketio.on('disconnect', namespace='/controller')
def disconnect():
    pass


### Slides and Presentation
@app.route('/remote')
def remote():
    return render_template('remote.html')


@socketio.on('slide', namespace='/presentation')
def message(message):
    print message, "slide"
    r.set('slide', message['data'])
    emit('slide', {'data': message['data']}, broadcast=True)


@socketio.on('action', namespace='/presentation')
def message(message):
    print message, "action"

    if message['action'] == 'image':
        r.set('stop_pattern', 'Yes')
        r.hset('patternargs', 'image', os.path.join(STATIC, 'slides', message['args']['image']))
        r.set('pattern', 'image')

    if message['action'] == 'gif':
        r.set('stop_pattern', 'Yes')
        r.hset('patternargs', 'gif', os.path.join(STATIC, 'slides', message['args']['gif']))
        r.set('pattern', 'gif')

    if message['action'] == 'color':
        r.set('stop_pattern', 'Yes')
        r.hset('patternargs', 'color', message['args']['color'])
        r.set('pattern', 'color')

    else:
        r.set('stop_pattern', 'Yes')
        r.set('pattern', message['action'])

@socketio.on('connect', namespace='/presentation')
def connect():
    print 'pres connect'
    pass


@socketio.on('disconnect', namespace='/presentation')
def disconnect():
    pass


@app.route('/slide/<foo>')
def slide(foo):
    r.set('stop_pattern', 'Yes')
    r.hset('patternargs', 'color', '0, 0, 0')
    r.set('pattern', 'color')
    return render_template('slide_%s.html' % foo)



# Purple 57, 20, 97

if __name__ == '__main__':
    socketio.run(app, host="0.0.0.0")
