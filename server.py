# python libs
import os

# third party libs
from flask import Flask, render_template, request, session, redirect
    # for story files on server
from werkzeug import secure_filename
from werkzeug import SharedDataMiddleware

# my libs
from model import User, connect_to_db, db

# Set up storage for uploaded photos
APP_ROOT = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(APP_ROOT, 'static/uploads')
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

# create app instance
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get("FLASK_SECRET_KEY", "oribooboo")

# all routes go here
@app.route('/')
def index():
    """ Homepage for Lilypad """

    if "current_user" in session:
        return redirect("/all-profiles")
	
    return render_template("index.html")

@app.route('/login')
def login():
    """ Form for users to log in """

    return render_template("login.html")


@app.route('/process-login', methods=["POST"])
def process_login():
    """ Logs a registered user in """

    email = request.form["email"]
    password = request.form["password"]

    # test if user exists
    if User.query.filter_by(email=email).first() is None:
        flash("<p>User with that email doesn't exist. <a href=\"/register\">Sign Up</a>.</p>", "error")
        return redirect('/login')

    # TODO ADD AUTHENTICATION ON USER
    # 2. If user does exist, check the credentials. If password incorrect,
    # flash message that password and email doesn't match

    #3. User credentials are authenticated. Sign user in by creating a session,
    #   and route user to their front page.
    #   Decide if it is necessary to keep frontpage seperate from homepage.
    current_user = User.query.filter_by(email=email).one()
    session["current_user"] = {"user_id": current_user.user_id, "username": current_user.f_name}

    return redirect('/all-profiles')

@app.route('/logout')
def logout():
    """Logout signed in users"""

    session.pop('current_user', 0)
    return redirect('/')

    # get credential data user

@app.route('/register')
def register():
    """ Registration form """


    # takes a user to the registration form

    return render_template("blah.html")

@app.route('/process-new-user', methods=["POST"])
def process_new_user():
    """ Process users registration form """

    # Get information user entered in form
    f_name = request.form['f-name']
    l_name = request.form['l-name']
    email = request.form['email']
    password = request.form['password']
    file = request.form['videfile']

    subprocess.call(['upload.py', file])

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

    return redirect("all-profiles.html")


@app.route("/all-profiles")
def all_profiles():
    """ Displays all profiles of existing users """

    return render_template('all-profiles.html')
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
