from flask import Flask, request, Response, render_template, jsonify, json, flash

from knockserver import app
from knockserver.forms import UserProfileForm
from knockserver.notifications import *
from knockserver.database import db_session
from knockserver.models import *
from config import RECOGNITION_TOLERANCE
import time


@app.route('/')
def index():
    return render_template('index.html')


@app.route("/onboard/", methods=["GET", "POST"])
def on_board_user():
    """Onboard a user."""
    form = UserProfileForm()
    if form.validate_on_submit():
        user = User()
        user.username = form.username.data
        user.ifttt_secret = form.ifttt_secret.data

        device = Device()
        device.identifier = form.device_id.data
        device.failure_count = 0

        preferences = NotificationPreferences()
        preferences.expire_threshold = form.expire_threshold.data
        preferences.failed_attempts_threshold = form.failed_attempts_threshold.data
        preferences.remaining_use_threshold = form.remaining_use_threshold.data
        preferences.send_no_earlier = form.send_no_earlier.data
        preferences.send_no_later = form.send_no_later.data
        preferences.success_threshold = form.success_threshold.data
        preferences.name = form.name.data
        preferences.failure_endpoint = form.failure_endpoint.data

        db_session.add(user)
        db_session.add(device)
        db_session.add(preferences)
        db_session.commit()

        profile_join = ProfileJoin()
        profile_join.device_id = device.id
        profile_join.user_id = user.id
        profile_join.preference_id = preferences.id
        profile_join.door_name = "Door 1"

        db_session.add(profile_join)
        db_session.commit()
        flash(user.username + ' successfully onboarded!', 'success')

    return render_template('onboarding.html', form=form)


@app.route('/patterns/', methods=['POST'])
def patterns_post():
    """Handles the creation of new knock patterns for a user."""
    data = request.get_json(force=True)  # Converts request body json into python dict

    pattern = AccessPattern()

    # Fields from form
    try:
        pattern.name = data['name']
    except KeyError as e:
        return Response('Name is required', 400)

    if 'expiration' in data:
        pattern.expiration = data['expiration']
    else:
        pattern.expiration = 0

    if 'max_uses' in data:
        pattern.max_uses = data['max_uses']
    else:
        pattern.max_uses = -1
    if 'device_id' in data:
        device_id = data['device_id']
        user_id = User.query.first().id
        profile = ProfileJoin.query.filter(User.id == user_id).first()
        device = Device.query.filter(Device.id == profile.device_id).first()
        device.identifier = device_id

    # Fields that always are initialized to the same value
    pattern.active = True
    pattern.used_count = 0
    pattern.pending = True

    db_session.add(pattern)
    db_session.commit()

    return jsonify(success=True)


@app.route('/patterns/', methods=['GET'])
def patterns_get():
    """
    Return all patterns for debugging
    Patterns ordered newest first
    """
    return jsonify(
        [pattern.serialize for pattern in
            AccessPattern.query.order_by(AccessPattern.id.desc()).all()]
    )


@app.route('/knock/', methods=['POST'])
def knock():
    """
    Receives knock information from the Android app
    If a knock is pending, this will set the pattern for the knock
    If no knocks are pending, this will attempt to match the pattern
    """
    data = request.get_json(force=True)  # Converts request body json into python dict

    # Check for pending knock
    user = User.query.first()
    pending_pattern = AccessPattern.query.filter(AccessPattern.pending == True).first()

    if pending_pattern is not None:

        # Convert int values from json array and store them as pattern_pieces
        for i, json_val in enumerate(data['pattern']):
            piece = PatternPiece()
            piece.length = data['pattern'][i]
            piece.order = i
            # First int is pressed time so all even indexed values are pressed
            piece.pressed = i % 2 == 0

            pending_pattern.pattern_pieces.append(piece)

        # Don't keep adding knocks to this pattern
        pending_pattern.pending = False

        db_session.add(pending_pattern)
        db_session.commit()

        return jsonify(success=True)

    else:
        if 'pattern' not in data:
            return jsonify(success=False)

        # Grab the current pattern pieces
        received_pattern_pieces = data['pattern']

        # Filter out all expired knocks
        match_patterns = AccessPattern.query.filter(AccessPattern.expiration > time.time())
        for pattern in match_patterns:

            # Check to make sure number of pieces match
            if (len(received_pattern_pieces) != len(pattern.pattern_pieces)) or (len(pattern.pattern_pieces) <= 0):
                continue

            # We know that new_pattern is already ordered because we just created it.
            # but we don't know if pattern is so order it here before comparing.
            ordered_pattern_pieces = sorted(pattern.pattern_pieces, key=lambda p: p.order)

            piece_failed = False
            for received_pattern_piece, stored_pattern_piece in zip(received_pattern_pieces, ordered_pattern_pieces):
                if not abs(received_pattern_piece - stored_pattern_piece.length) <= RECOGNITION_TOLERANCE:
                    piece_failed = True
                    break

            if piece_failed:
                # Move onto checking the next pattern.
                continue
            else:

                # Correct pattern detected!!! :D
                # Unlock the door
                pattern.used_count += 1
                db_session.commit()
                pattern_success(pattern, "TestDevice1")  # temp device id until implemented
                return jsonify(success=True)

        send_failure_notification("TestDevice1")  # temp device id until implemented
        return jsonify(success=False)
