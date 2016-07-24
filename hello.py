from flask import Flask

app = Flask(__name__)

@app.route("/")
#index page
def hello():
    return "Hello World!"

@app.route("/user/<username>")
def userProfile (username):

@app.route("/login"):
def loginPage ():

@app.route("/offering"):
def offering ():

@app.route("/roommate"):
def roommate ():


if __name__ == "__main__":
    app.run()