import socketio

sio = socketio.Client()

@sio.event
def connect():
    print("connection established")
    sio.emit('on_message',
             'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE2NzYzNTA1ODIsImlhdCI6MTY3NjI2NDE4MiwiYnJhbmNoX2lkIjoibWFpbl9tYXN0ZXIifQ.k7mDUjNiChQWXgqPO3YWPKcATtCO4pRxQitEd4G9Qd0')

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
def potwData(message):
    print("data 3333 33333 3333333333333333333333333333333333333333333 received data: ", message)

sio.connect('http://192.168.113.60:8000')


sio.wait()