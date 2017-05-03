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

        KnockServerTestCase.env_setup()

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

    def test_pending_pattern(self):
        pending = True
        name = "test name"
        expiration = 6
        max_uses = 100
        device_id = "01:23:45:67:89"
        active = True
        used_count = 0

        KnockServerTestCase.env_setup()

        # First check to see if there are no pending patterns in the db
        pending_pattern = models.AccessPattern.query.filter(models.AccessPattern.pending == True).first()
        self.assertIsNone(pending_pattern, "Pending pattern found before test started")

        # Now try to create a pending pattern
        resp = self.app.post(
            '/patterns/',
            data=json.dumps({"name": name,
                             "expiration": expiration,
                             "max_uses": max_uses,
                             "device_id": device_id}),
            content_type='application/json',
            follow_redirects=True
        )
        pending_pattern = models.AccessPattern.query.filter(models.AccessPattern.pending == pending).first()
        self.assertIsNotNone(pending_pattern, "Pending pattern not found")

        user = models.User.query.first()
        profile = models.ProfileJoin.query.filter(models.ProfileJoin.user_id == user.id).first()
        device = models.Device.query.filter(models.Device.id == profile.device_id).first()

        # Check the new pattern object
        self.assertEqual(pending_pattern.name, name, "Name is incorrect")
        self.assertEqual(pending_pattern.expiration, expiration, "Expiration is incorrect")
        self.assertEqual(pending_pattern.max_uses, max_uses, "Max uses is incorrect")
        self.assertEqual(pending_pattern.active, active, "Active is incorrect")
        self.assertEqual(pending_pattern.used_count, used_count, "Used count is incorrect")

        # Check the device object
        self.assertEqual(device.identifier, device_id, "Device ID is incorrect")

        # Check that we got success
        data = json.loads(resp.data.decode())
        self.assertEqual(data['success'], True)

    # - Can ignore an empty button press (This should never happen but we should check for this)
    # - Can detect if the length of two button press patterns are different.
    # - Can detect if the length of two button press patterns are the same.

    @staticmethod
    def env_setup():
        """
        Utilize this helper function to initialize all the user profile stuff for testing
        :return:
        """
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

        db_session.add(stored_device)
        db_session.add(stored_user)
        db_session.add(stored_profile)
        db_session.add(stored_preferences)
        db_session.commit()

if __name__ == '__main__':
    unittest.main()
