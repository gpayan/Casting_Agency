import unittest
from flask_sqlalchemy import SQLAlchemy
from flaskcast import app
from flaskcast.models import Actor


DB_PATH = "postgresql://gpayan@localhost:5432/casting_agency_test"

class CastingAgencyTestCase(unittest.TestCase):

    def setUp(self):
        self.app = app
        self.client = self.app.test_client

        self.app.config['SQLALCHEMY_DATABASE_URI'] = DB_PATH
        self.app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            self.db.create_all()

        actor = Actor(
            name = 'Buffy',
            age = '42',
            gender = 'female'
        )
        actor.insert()

    def tearDown(self):
        pass

    def test_get_actor(self):
        #res = self.client().get('/actors')
        #data = json.loads(res.data)
        #print(data)
        pass

if __name__ == '__main__':
    unittest.main()