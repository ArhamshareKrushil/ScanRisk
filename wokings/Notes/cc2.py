import socketio

sio = socketio.Client()

@sio.event
def connect():
    print("connection established")

@sio.event
def disconnect():
    print("disconnected from server")

@sio.event
def data(message):
    print("received data: ", message)

@sio.event
def data1(message):
    print("data 1 111111 1 111111 received data: ", message)

@sio.event
def data2(message):
    print("data 2 222 22222222222222222222222 222 received data: ", message)

@sio.event
def data3(message):
    print("data 3333 33333 3333333333333333333333333333333333333333333 received data: ", message)

sio.connect('http://192.168.102.155:5555')
sio.wait()