# python libs
import os

# third party libs
from flask import Flask, render_template, request, session, redirect

# my libs
from model import User, connect_to_db, db

# create app instance
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get("FLASK_SECRET_KEY", "oribooboo")

# all routes go here
@app.route('/')
def index():
	""" Homepage for YouMate """

	return render_template("index.html")

@app.route('/login')
def login():
    """ Logs a registered user in """

    # get credential data user 

@app.route('/register')
def register():
    """ Registration form """

    # takes a user to the registration form

    return render_template("register.html")

@app.route('/process-new-user', methods=["POST"])
def process_new_user():
    """ Process users registration form """

    # Get information user entered in form
    f_name = request.form['f-name']
    l_name = request.form['l-name']
    email = request.form['email']
    password = request.form['password']

    print("#######User firstname", f_name)
    
    # create new user object to create and store
    # new user in the database
    user = User(f_name=f_name, l_name=l_name, email=email, password=password)
    
    # add user to database
    db.session.add(user)
    db.session.commit()

    # after user account is created,
    # create session for user so user 
    # can stay logged in. 
    # Query on email, because this is what seperates
    # each user from the next .
    current_user = User.query.filter_by(email=email).one()
    session["current_user"] = {"user_id": current_user.user_id,
                              "firstname": current_user.f_name
                              }

    # redirect user to homepage so that user can begin using site

    return "new user %s %s created" % (current_user.f_name, current_user.l_name)

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
