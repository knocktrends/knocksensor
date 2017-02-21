from flask import Flask, request, render_template
from flask import request
from flask import render_template
from flask import jsonify
from flask import json

from knockserver import app
from knockserver.database import db_session
from knockserver.models import ExampleObject

@app.route('/')
def index():
    return render_template('index.html')
