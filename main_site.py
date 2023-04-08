from waitress import serve

from website import create_app

app = create_app()

if __name__ == '__main__':
    serve(app, port=5050, threads=4)
