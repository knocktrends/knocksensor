from flask import Flask
from knockserver.database import db_session

app = Flask(__name__)
app.secret_key = "super secret key whoa"

import knockserver.views

@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()
