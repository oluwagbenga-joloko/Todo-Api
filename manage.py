import os

from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

from api import create_flask_app
from api.models import db


app = create_flask_app(os.getenv("ENVIRONMENT"))
print(os.getenv("ENVIRONMENT"))
migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)

if __name__ == "__main__":
    manager.run()
