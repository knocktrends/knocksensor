import os
from knockserver import database, app
import unittest
import tempfile
import json


class KnockServerTestCase(unittest.TestCase):

    def setUp(self):
        self.db_fd, app.config['DATABASE'] = tempfile.mkstemp()
        app.config['TESTING'] = True
        self.app = app.test_client()
        with app.app_context():
            database.init_db()

    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(app.config['DATABASE'])

    def test_empty_db_no_match(self):
        resp = self.app.post(
            '/knock/',
            data=json.dumps({"pattern": [123, 123, 123]}),
            content_type='application/json',
            follow_redirects=True
        )

        print(resp.data)
        data = json.loads(resp.data)
        self.assertEqual(data['success'], False)

    # - Can ignore an empty button press (THis should never happen but we should check for this)
    # - Can detect if the length of two button press patterns are different.
    # - Can detect if the length of two button press patterns are the same.

    # def test_



if __name__ == '__main__':
    unittest.main()
