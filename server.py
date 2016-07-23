# python libs
import os

# third party libs
from flask import Flask, render_template, request, session, redirect

# my libs
from model import connect_to_db, db

# create app instance
app = Flask(__name__)

# all routes go here
@app.route('/')
def index():
	""" Homepage for YouMate """

	return render_template("index.html")

@app.route('/process-new-user', methods=["POST"])
def process_new_user():
    """ Process users registration form """

    # Get information user entered in form
    f_name = request.form['firstname']
    l_name = request.form['lastname']
    email = request.form['email']
    
    # create new user object to create and store
    # new user in the database
    user = User(firstname=f_name, lastname=l_name, email=email)
    
    # add user to database
    db.session.add(user)
    db.session.commit()

    # after user account is created,
    # create session for user so user 
    # can stay logged in. 
    # Query on email, because this is what seperates
    # each user from the next .
    current_user = User.query.filter_by(email=email).one()
    session["curren_user"] = {"user_id": current.user_id,
                              "firstname": current_user.f_name
                              }

    # redirect user to homepage so that user can begin using site

    return redirect('/')

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
