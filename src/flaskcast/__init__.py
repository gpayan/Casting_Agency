from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://gpayan@localhost:5432/casting_agency'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

migrate = Migrate(app, db)

if __name__ == '__main__' :
    #context = ('local.crt', 'local.key')
    #app.run(debug=True, ssl_context=context)
    print('Flaskcast is run directly')
    print('name is:', __name__)
else:
    print('Flaskcast is run by another module')
    print('name is:', __name__)

from flaskcast import routes, models #workaround to circular imports