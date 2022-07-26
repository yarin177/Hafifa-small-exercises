from flask import Flask
import argparse
from random import randint

app = Flask(__name__)

def get_port_from_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--port", help = "Port number")
    args = parser.parse_args()

    if args.port is not None:
        return args.port
    return 8080

@app.route('/<str>', methods = ['GET'])
def get_random_string(string):
    rand_num = randint(1,3)
    if rand_num == 1:
        return string
    return ''


if __name__ == '__main__':
    port = get_port_from_parser() # default is 8080
    print(f'Running server with port: {port}')
    app.run(host='0.0.0.0', port=port)