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

@app.route('/patterns/', methods=['GET', 'POST'])
def patterns():
    """
    Handles the creation of new knock patterns for a user.
    """
    if request.method == 'POST':
        data = request.get_json(force=True)# converts request body json into python dict

        pattern = AccessPattern()
        
        # Fields from form
        pattern.name = data['name']

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

        return '{"Ok": true}' #TODO decide response
        
    elif request.method == 'GET':
        pass

    return ''

@app.route('/knock/', methods=['POST'])
def knock():
    """
    Receives knock information from the Android app
    If a knock is pending, this will set the pattern for the knock
    If no knocks are pending, this will attempt to match the pattern
    """
    data = request.get_json(force=True)# converts request body json into python dict

    # Check for pending knock
    pending_pattern = AccessPatten.query.filter(AccessPattern.pending == True).first()

    if pending_pattern is not None:
        i = 0
        for json_val in data['pattern']:
            piece = PatternPiece()
            piece.length = data['pattern'][i]
            piece.order = i
            #TODO Don't remember if first is pressed
            piece.pressed = True if (i % 2 == 0) else False 

            pending_pattern.patternPieces.add(piece)
            i += 1

        db_session.add(pending_pattern)
        db_session.commit()

    else: # TODO Pattern matching
        pass

