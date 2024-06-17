from core.server import create_app, socketio

app = create_app()

if __name__ == '__main__':
    print("Starting Server")
    socketio.run(app, port=app.config['socketio_port'])
