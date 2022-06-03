import email
from flask import Flask,render_template,url_for,flash,redirect
# from forms import RegistrationForm,LoginForm
from pymongo import MongoClient

client = MongoClient()
client = MongoClient("mongodb://localhost:27017/")
mydatabase = client.flaskData
mycollection = mydatabase.login

app = Flask(__name__)

app.config['SECRET_KEY']='5791628bb0b13ce0c676dfde280ba245'

@app.route("/")#home page route
@app.route("/home")

def home():
    return render_template('home.html')

@app.route("/about")
def about():
    return render_template('about.html',title="ABOUT")

@app.route("/register",methods=['GET','POST'])
def register():
    form=RegistrationForm()
    if form.validate_on_submit():
        message="Account created for {}".format(form.username.data)
        flash(message,'success')
        return redirect(url_for('home'))#name of the function not file
    return render_template('register.html',title='Register',form=form)

@app.route("/login",methods=['GET','POST'])
def login():
    form=LoginForm()
    if form.validate_on_submit():
        email=form.email.data
        user_password=form.password.data
        print(email,user_password)
        user_data = mycollection.find_one({'email': email})
        print(user_data)
        print(type(user_data))
        if user_data and user_data["password"] == user_password:
            message="You hava been logged as {}".format(email)
            flash(message,'success')
            return redirect(url_for('home'))
        else:
            flash('Login unsuccessful. Please check username and password','danger')
    return render_template('login.html',title='Login',form=form)