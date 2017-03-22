from flask import Flask, request, render_template
from flask import request
from flask import render_template
from flask import jsonify
from flask import json

from knockserver import app
from knockserver.database import db_session
from knockserver.models import AccessPattern, PatternPiece

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/patterns/', methods=['POST'])
def patterns_post():
    """
    Handles the creation of new knock patterns for a user.
    """
    data = request.get_json(force=True)# converts request body json into python dict

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

    if 'maxUses' in data:
        pattern.maxUses = data['maxUses']
    else:
        pattern.maxUses = -1

    # Fields that always are initialized to the same value
    pattern.active = True
    pattern.usedCount = 0
    pattern.pending = True

    db_session.add(pattern)
    db_session.commit()

    return '{"success": true}' #TODO decide response


@app.route('/patterns/', methods = ['GET'])
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
    data = request.get_json(force=True)# converts request body json into python dict

    # Check for pending knock
    pending_pattern = AccessPattern.query.filter(AccessPattern.pending == True).first()

    if pending_pattern is not None:
        i = 0
        # Convert int values from json array and store them as PatternPieces
        for json_val in data['pattern']:
            piece = PatternPiece()
            piece.length = data['pattern'][i]
            piece.order = i
            # First int is pressed time so all even indexed values are pressed
            piece.pressed = i % 2 == 0 

            pending_pattern.patternPieces.append(piece)
            i += 1

        # Don't keep adding knocks to this pattern
        pending_pattern.pending = False

        db_session.add(pending_pattern)
        db_session.commit()

        print(pending_pattern.id)
        return '{"success": true}'

    else: # TODO Pattern matching
        new_pattern = AccessPattern()

        for i, piece_length in enumerate(data['pattern']):
            piece = PatternPiece()
            piece.length = piece_length
            piece.order = i
            # First int is pressed time so all even indexed values are pressed
            piece.pressed = i % 2 == 0  # Assigns pressed to true or false.
            new_pattern.patternPieces.append(piece)

        match_patterns = AccessPattern.query.all()
        for pattern in match_patterns:
            # Check to make sure number of pieces match
            if (len(new_pattern.patternPieces) != len(pattern.patternPieces)) or (len(pattern.patternPieces) <= 0):
                continue
            # We know that new_pattern is already ordered because we just created it.
            # but we don't know if pattern is so order it here before compairing.
            ordered_pattern_pieces = sorted(pattern.patternPieces, key=lambda p: p.order)

            piece_failed = False
            for new_pattern_piece, stored_pattern_piece in zip(new_pattern.patternPieces, ordered_pattern_pieces):
                # TODO: make sure that buffer is defined.
                buffer = 200
                if not abs(new_pattern_piece - stored_pattern_piece) <= buffer:
                    # TODO: properly jsonify things in this return.
                    piece_failed = True
                    break
            
            if piece_failed:
                # Move onto checking the next pattern.
                continue
            else:
                # Correct pattern detected!!! :D
                # Unlock the door

                # TODO: UPDATE USED COUNT
                return '{"success": true}'
            
        return '{"success": false}'
