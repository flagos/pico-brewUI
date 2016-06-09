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

    def test_empty_db(self):
        rv = self.app.get('/')
        #assert b'No entries here so far' in rv.data
        print(rv.data)


if __name__ == '__main__':
    unittest.main()
