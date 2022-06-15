from distutils.log import debug
from pip import main
from flask import Flask, request, jsonify


# Init App
app = Flask(__name__)



if __name__ == '__main__':
    app.run(debug=True)
