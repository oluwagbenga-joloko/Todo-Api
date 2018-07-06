from flask_testing import TestCase
import os 
# import pdb; pdb.set_trace()
from api.main import create_flask_app
from api.models import db


class BaseTestCase(TestCase):

    def create_app(self):
        self.app = create_flask_app('test')
        return self.app

    def setUp(self):
        db.create_all()
    
    def tearDown(self):
        db.session.remove()
        db.drop_all()

    
        
        
