from knockserver import database, app, models
import unittest
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

        stored_device = models.Device()
        stored_device.failure_count = 1
        stored_device.name = "TestDevice1"
        stored_device.identifier = "TestDevice1"

        stored_user = models.User()
        stored_user.hashed_pass = "doesn't matter"
        stored_user.ifttt_secret = "cMq6JSJtMAzXa9BFq_EjX6"
        stored_user.salt = "fake the salt"
        stored_user.username = "TestUser1"

        stored_profile = models.ProfileJoin()
        stored_profile.device_id = 1
        stored_profile.pattern_id = 1
        stored_profile.preference_id = 1
        stored_profile.user_id = 1
        stored_profile.door_name = "TestDoor1"

        stored_preferences = models.NotificationPreferences()
        stored_preferences.expire_threshold = 10000
        stored_preferences.failed_attempts_threshold = 1
        stored_preferences.name = "knock_knock"
        stored_preferences.remaining_use_threshold = 10
        stored_preferences.send_no_earlier = None
        stored_preferences.send_no_later = None
        stored_preferences.success_threshold = 1
        stored_preferences.failure_endpoint = "knock_failed"



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

        db_session.add(stored_device)
        db_session.add(stored_user)
        db_session.add(stored_profile)
        db_session.add(stored_preferences)
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
