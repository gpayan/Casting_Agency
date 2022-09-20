from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
#from flaskcast.models import db
from .models import db
from flask_cors import CORS

app = Flask(__name__) #creates application object as an instance of class Flask

#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://gpayan@localhost:5432/casting_agency'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://govrefbkmbfdki:596dd04fe1871334a64acc660708e06912d9256deddaaa21631c8eedff37e47d@ec2-3-208-79-113.compute-1.amazonaws.com:5432/d64sbt9u36jf0o'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#db = SQLAlchemy(app)
db.init_app(app)

migrate = Migrate(app, db)

CORS(app)

if __name__ == '__main__' :
    #context = ('local.crt', 'local.key')
    #app.run(debug=True, ssl_context=context)
    print('Flaskcast is run directly')
    print('name is:', __name__)
else:
    print('Flaskcast is run by another module')
    print('name is:', __name__)

#from flaskcast import routes, models #workaround to circular imports
from . import routes, models #trying to fix local module import issue on heroku