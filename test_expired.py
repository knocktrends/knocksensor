import os
from knockserver import database, app, models
import unittest
import tempfile
import json

from knockserver.database import db_session


class KnockServerTestCase(unittest.TestCase):

    def setUp(self):
        self.db_fd, app.config['DATABASE'] = tempfile.mkstemp()
        app.config['TESTING'] = True
        self.app = app.test_client()
        with app.app_context():
            database.init_db()

    def tearDown(self):
        db_session.remove()
        # os.remove('knock.db')  # TODO: This makes the tests pass.  Workaround, remove when real solution available
        os.close(self.db_fd)
        os.unlink(app.config['DATABASE'])

    def test_no_knocks_in_db(self):
        # This test will sometimes fail until we get a proper way to set up the testing framework
        # Need to properly setup and teardown db
        self.assertEqual(len(models.AccessPattern.query.all()), 0)

    def test_expired_knock_not_matched(self):
        stored_pattern = models.AccessPattern()
        stored_pattern.active = True
        stored_pattern.name = "Test Pattern 1"
        stored_pattern.pending = False
        stored_pattern.used_count = 0

        # Set the pattern in the past
        stored_pattern.expiration = 1491230220

        for i in range(3):
            piece = models.PatternPiece()
            piece.length = 123
            piece.order = i
            # First int is pressed time so all even indexed values are pressed
            piece.pressed = i % 2 == 0

            stored_pattern.pattern_pieces.append(piece)

        db_session.add(stored_pattern)
        db_session.commit()

        # Add a pattern that should match, and try to match it
        resp = self.app.post(
            '/knock/',
            data=json.dumps({"pattern": [123, 123, 123]}),
            content_type='application/json',
            follow_redirects=True
        )

        data = json.loads(resp.data.decode())

        # The pattern should not be in the database
        self.assertEqual(data['success'], False)


if __name__ == '__main__':
    unittest.main()
