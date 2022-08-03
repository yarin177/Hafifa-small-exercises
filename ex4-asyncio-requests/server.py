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
    """
    This function gets a word(string) parameter via a URL,
        and returns the same word 1/3 of the times.
    Args:
        word: (str) A word from a GET HTTP request.
    Returns:
        The same word 1/3 of the times, empty string otherwise.
    """
    rand_num = randint(1,3)

    if rand_num == 1:
        return string
    return ''


if __name__ == '__main__':
    #default port is 8080
    
    port = get_port_from_parser()
    print(f'Running server with port: {port}')
    app.run(host='0.0.0.0', port=port)