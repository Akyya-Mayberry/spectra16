# python libs
import os
import subprocess

# third party libs
from flask import Flask, render_template, request, session, redirect
import upload
import youtube

    # for story files on server
from werkzeug import secure_filename
from werkzeug import SharedDataMiddleware

# my libs
from model import User, connect_to_db, db

# Set up storage for uploaded photos
APP_ROOT = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(APP_ROOT, 'static/uploads')
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
CLIENT_SECRETS_FILE = "client_id.json"

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

    return render_template('andrea-abode.html')

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

@app.route('/offering')
def offering():
    """ Offering page"""


    # takes a user to the registration form

    return render_template("offering.html")


@app.route('/andrea')
def andrea_abode():
    """ Registration form """


    # takes a user to the registration form

    return render_template("andrea-abode.html")


@app.route('/youtube-login')
def youtube_logging_in():
    """Authenticate users through YouTube Account"""

    """A user will be requested to grant the Preach app access to
    data on their YouTube account. This route does that.
    It routes users to a authorization server, which is specified in the
    client_secrets.json file which is "auth_uri": "https://accounts.google.com/o/oauth2/auth".
    It attaches pretty much everything from the flow_from_secrets function.
    The the scope, redirect_uri, and client ids to the url.

    When the user approves or denies access, the authurization routes the user to the url
    callback listed in the flow_from_client secrets, which is http://localhost:5000/oauth2callback,
    and it attaches and error parameter for deny or a code for approve. My /oauth2callback route
    will handle what is returned from the authorization server.
    """

    # TO DO: MOVE TO YOUTUBE.PY 
 
    # Set up the process to route user to YouTube authorization servers
    flow = youtube.flow_from_clientsecrets(CLIENT_SECRETS_FILE,
                                   scope='https://www.googleapis.com/auth/youtube',
                                   redirect_uri='http://localhost:5000/oauth2callback')

    # Sends user to authorization server.
    # Once user allows app to act on their behalf, the Youtube server
    # sends a response with a code added as a parameter. This code will
    # be handled in the /oauth2callback route function. This is because
    # this route is set up above as the 'redirect_uri'

    auth_uri = flow.step1_get_authorize_url()

    return redirect(auth_uri)


@app.route('/oauth2callback')
def oauth2callback():
    """Handles reponse sent back from YouTube's authorization server"""

    """If the users granted access to the app, then YouTube attached a code
    parameter in the redirect_url (which is this route) otherwise
    it attaches a code. The code is use to exchange an access token,
    which allows my app to make API calls on the behalf of the user.
    """

    # If user denies app access...
    # Send them back to the login page, so they can create a new account or
    # or log in using their log in credentials from my app.
    error = request.args.get('error')
    if error:
        return redirect('/')

    # If user approves app to access...
    # Get the code as it will be used to request
    # from the authorization server, an access token.
    # The access token will allow the app to interact with and make calls to the
    # YouTube services (based on the scope listed above)
    code = request.args.get('code')

    if code:
        flow = youtube.flow_from_clientsecrets(CLIENT_SECRETS_FILE,
                                       "https://www.googleapis.com/auth/youtube",
                                       redirect_uri=request.base_url)

    # Try to exchange the authorization code for user credentials
    try:
        credentials = flow.step2_exchange(code)
    except Exception as e:
        print "Unable to get an access token because ", e.message

    # At this point, we have receive a credential from the authorization server
    # which includes many things, but most importantly, the access and refresh tokens.
    # Save the credentials in a session for now, but plan to use Storage.
    session['credentials'] = credentials

    return redirect('/all-profiles')



@app.route('/process-new-user', methods=["POST"])
def process_new_user():
    """ Process users registration form """

    # Get information user entered in form
    f_name = request.form['f-name']
    l_name = request.form['l-name']
    email = request.form['email']
    password = request.form['password']
    profile_vid = request.form['vidfile']

    # uploads video file to youtube
    # os.system("upload.py --file" + profile_vid)

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

    return redirect("/all-profiles")


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
