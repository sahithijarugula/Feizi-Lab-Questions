from flask import Flask, render_template, request, redirect
import os
import pandas as pd
from oauthlib.oauth2 import WebApplicationClient
import json
import requests

#Google credentials for login via gmail option
GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID", None)
GOOGLE_CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET", None)
GOOGLE_DISCOVERY_URL = (
    "https://accounts.google.com/.well-known/openid-configuration"
)



app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY") or os.urandom(24)
client = WebApplicationClient(GOOGLE_CLIENT_ID)

#builds path for csv (account_info.csv) that login info will be saved in
basedir = os.path.abspath(os.path.dirname(__file__))
app.config["question1"]= "/Users/sahithijarugula/question1"
path = os.path.join(basedir, app.config["question1"], "account_info.csv")

#reads existing info in account_csv to see if potential login is valid
df = pd.read_csv(path)
df2 = pd.DataFrame(columns=["First Name","Last Name","Email", "Username", "Password"])

#code for login page
@app.route("/login", methods=["POST","GET"])
def user_login():
  if request.method == "POST":
    user_id = request.form["username"]
    password = request.form["password"]
    
    #checks if login info is valid if it is goes to the next page, if not gives error
    if(user_id not in df["Email"].unique() and user_id not in df["Username"].unique()):
      return render_template("login.html", error=True)
    elif(password not in df["Password"].unique()):
      return render_template("login.html", error=True)
    elif(user_id in df["Email"].unique()):
      if(df[df["Email"] == user_id].index != df[df["Password"] == password].index):
        return render_template("login.html", error=True)
      else:
        return render_template("next.html")
    elif(user_id in df["Username"].unique()):
      if(df[df["Username"] == user_id].index != df[df["Password"] == password].index):
        return render_template("login.html", error=True)
      else:
        return render_template("next.html")
    else:
      df2.to_csv('account_info.csv', mode="a", index=False, header=False)
      return render_template("next.html")

  return render_template("login.html")


#code for login via gmail
@app.route("/google-login")
def login():    
    google_provider_cfg = get_google_provider_cfg()
    authorization_endpoint = google_provider_cfg["authorization_endpoint"]
    
    #requests for google login and gets user info
    request_uri = client.prepare_request_uri(
        authorization_endpoint,
        redirect_uri=request.base_url + "/callback",
        scope=["openid", "email", "profile"],
    ) 

    return redirect(request_uri)

def get_google_provider_cfg():
    return requests.get(GOOGLE_DISCOVERY_URL).json()

#directs to next page if google login was successful
@app.route("/google-login/callback")
def callback():
    return render_template("next.html")


#code for create account page
@app.route("/create-account", methods=["POST","GET"])
def new_account():
  global df2
  if request.method == "POST":
    #gets info user types in
    user_info = [request.form["first_name"], request.form["last_name"], request.form["email"], request.form["username"], request.form["password"]]    
    
    #checks if an account with the email already exists or if username has been taken and gives error that's the case 
    #if not successfully adds account info to account_info
    if(user_info[2] in df["Email"].unique()):
      return render_template("create.html", error1=True)
    elif(user_info[3] in df["Username"].unique()):
      return render_template("create.html", error2=True)
    else: 
      df2 = pd.concat([df2, pd.DataFrame([user_info], columns=["First Name","Last Name","Email", "Username", "Password"])])
      df2.to_csv(path, mode="a", index=False, header=False)
      return render_template("next.html")
 
  return render_template("create.html")

app.run(port=4500)






