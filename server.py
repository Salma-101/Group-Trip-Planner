# server.py
import socketio
from flask import Flask

app = Flask(__name__)
sio = socketio.Server(cors_allowed_origins="*")
app = socketio.WSGIApp(sio, app)

# Dictionary to store trips (you can connect this to a DB later)
trips = {}

@sio.event
def connect(sid, environ):
    print(f"{sid} connected")

@sio.event
def disconnect(sid):
    print(f"{sid} disconnected")

@sio.event
def join_trip(sid, trip_id):
    sio.enter_room(sid, trip_id)
    if trip_id not in trips:
        trips[trip_id] = []
    sio.emit('trip_update', trips[trip_id], room=trip_id)

@sio.event
def add_place(sid, data):
    trip_id = data['trip_id']
    place = data['place']
    trips[trip_id].append(place)
    sio.emit('trip_update', trips[trip_id], room=trip_id)

if __name__ == '__main__':
    import eventlet
    eventlet.wsgi.server(eventlet.listen(('localhost', 5000)), app)
