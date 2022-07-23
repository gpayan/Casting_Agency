from flask import Flask

app = Flask(__name__)

from flaskcast import routes #workaround to circular imports