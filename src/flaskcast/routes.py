from flaskcast import app

@app.route('/index')
def index():
    return 'Hello World!'