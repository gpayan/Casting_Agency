from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

from src.casting_agency import app
from src.flaskcast import db

migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    manager.run()