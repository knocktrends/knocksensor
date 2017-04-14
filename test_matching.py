import os
from knockserver import database, app, models
import unittest
import tempfile
import json
import time

from knockserver.database import db_session


class KnockServerTestCase(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        database.init_db()

    def tearDown(self):
        db_session.remove()
        database.silent_remove_test_db()


    def test_empty_db_no_match(self):
        resp = self.app.post(
            '/knock/',
            data=json.dumps({"pattern": [123, 123, 123]}),
            content_type='application/json',
            follow_redirects=True
        )

        data = json.loads(resp.data.decode())
        self.assertEqual(data['success'], False)

    def test_perfect_match(self):
        stored_pattern = models.AccessPattern()
        stored_pattern.active = True
        stored_pattern.name = "Test Pattern 1"
        stored_pattern.pending = False
        stored_pattern.used_count = 0

        # Make this access pattern expire in the future by a significant amount of seconds
        stored_pattern.expiration = time.time() + 10000

        for i in range(3):
            piece = models.PatternPiece()
            piece.length = 123
            piece.order = i
            # First int is pressed time so all even indexed values are pressed
            piece.pressed = i % 2 == 0

            stored_pattern.pattern_pieces.append(piece)

        db_session.add(stored_pattern)
        db_session.commit()

        resp = self.app.post(
            '/knock/',
            data=json.dumps({"pattern": [123, 123, 123]}),
            content_type='application/json',
            follow_redirects=True
        )

        data = json.loads(resp.data.decode())
        self.assertEqual(data['success'], True)

    # - Can ignore an empty button press (THis should never happen but we should check for this)
    # - Can detect if the length of two button press patterns are different.
    # - Can detect if the length of two button press patterns are the same.


if __name__ == '__main__':
    unittest.main()
