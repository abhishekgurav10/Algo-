from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import redis
import threading

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app) 

redis_client = redis.Redis(host='localhost', port=6379, db=0)
pubsub = redis_client.pubsub()

def redis_listener():
    pubsub.subscribe('total_pnl_channel')
    for message in pubsub.listen():
        if message['type'] == 'message':
            data = message['data'].decode('utf-8')
            socketio.emit('update_pnl', {'pnl': data})

# Start Redis listener in a separate thread
thread = threading.Thread(target=redis_listener)
thread.daemon = True
thread.start()

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    socketio.run(app, debug=True)        