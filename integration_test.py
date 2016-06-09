from future import standard_library
standard_library.install_aliases()
import unittest
import app
import os
import tempfile


import time

class IntegrationTest(unittest.TestCase):

    def setUp(self):
        self.db_fd, app.app.config['DATABASE'] = tempfile.mkstemp()
        self.app = app.app.test_client()
        #app.init_db()

    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(app.app.config['DATABASE'])

    def test_flask_is_alive(self):
        rv = self.app.get('/')
        assert(rv.data)

    def test_adding_a_recipe(self):
        self.app.get('/add/recipe', data=dict(
            url='https://www.brewtoad.com/recipes/black-walnut-brown-1968'
        ))
        self.app.get('/update/task', data=dict(
            task_id='0',
            task_status='true'
        ))
        #time.sleep(120)

        

        
if __name__ == '__main__':
    unittest.main()
