from website import create_app
from waitress import serve

app = create_app()

if __name__ == '__main__':
    serve(app, port=5050, threads=4)
