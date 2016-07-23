# python libs
import os

# third party libs
from flask import Flask, render_template

# my libs
from model import connect_to_db, db

# create app instance
app = Flask(__name__)

# all routes go here
@app.route('/')
def index():
	""" Homepage for YouMate """

	return render_template("index.html")

# run server file here
if __name__ == "__main__":
    connect_to_db(app, os.environ.get("DATABASE_URL"))
    db.create_all(app=app)
    DEBUG = "NO_DEBUG" not in os.environ
    DEBUG_TB_INTERCEPT_REDIRECTS = False
    # DebugToolbarExtension(app)
    # set_val_user_id()
    PORT = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=PORT, debug=DEBUG)
