from flask import Flask, render_template, request, redirect, url_for, flash
from flask import session as login_session
import pyrebase

app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SECRET_KEY'] = 'super-secret-key'
config = {
    "apiKey": "AIzaSyB_HC4Etpm0DykL5IbJ9rh-1u5TydYWsYE",
    "authDomain": "rec-books-89799.firebaseapp.com",
    "projectId": "rec-books-89799",
    "storageBucket": "rec-books-89799.appspot.com",
    "messagingSenderId": "398857765682",
    "appId": "1:398857765682:web:16c743230f6de6bca0cd2b",
    "databaseURL":"https://rec-books-89799-default-rtdb.europe-west1.firebasedatabase.app/"}
firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
db = firebase.database()
#Code goes below here

@app.route('/', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        category = request.form['category']
        try:
            login_session['user'] = auth.create_user_with_email_and_password(email, password)
            UID = login_session['user']['localId']
            user = {"email": email, "category": category}
            db.child("Users").child(UID).set(user)
            return redirect(url_for(category))
        except:
             error = "Authentication failed"
    return render_template("signup.html")
    
@app.route('/signin', methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        category = request.form['category']
        try:
            login_session['user'] = auth.sign_in_with_email_and_password(email, password)
            return redirect(url_for(category))
        except:
             error = "Authentication failed"
    return render_template("signin.html")

@app.route('/delete', methods=['GET', 'POST'])
def delete():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        try:
            UID = login_session['user']['localId']
            db.child("Users").child(UID).remove()
            return redirect(url_for('signup'))
        except:
             return "deleting failed"
    return render_template("delete.html")
    

@app.route('/add', methods=['GET', 'POST'])
def add():
    category = None
    catpics = {}
    if request.method == 'POST':
        picture = request.form['picture']
        link = request.form['link']
        category = request.form['category']
        try:
            pic = {"picture": picture, "link": link ,"category" : category}
            db.child("pics").child(category).set(pic)
            return redirect(url_for(category))
        except:
             return "adding failed"
    else:
        catpics_ordered = db.child("pics").child(category).get().val() if category else {}
        catpics = dict(catpics_ordered) 
    return render_template("add.html", catpics= catpics,category=category)

@app.route('/fantacy')
def fantacy():
    catpics = db.child("pics").child('fantacy').get().val() 

    return render_template('fan.html',catpics=catpics)

@app.route('/horror')
def horror():
    catpics = db.child("pics").child('horror').get().val() 
    print(catpics)
    return render_template('hor.html',catpics=catpics)

@app.route('/comedy')
def comedy():
    return render_template('com.html')

@app.route('/scifi')
def scifi():
    return render_template('scifi.html')

@app.route('/romance')
def romance():
    return render_template('rom.html')

#Code goes above here

if __name__ == '__main__':
    app.run(debug=True)