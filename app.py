import email
from flask import Flask,render_template,url_for,flash,redirect,session,g,request
from matplotlib.pyplot import title
from forms import RegistrationForm,LoginForm,OrderForm,AdminLogin
from pymongo import MongoClient

client = MongoClient()
client = MongoClient("mongodb://localhost:27017/")
mydatabase = client.vehicle
loginDB = mydatabase.loginInfo
orderDB = mydatabase.orderInfo
adminDB = mydatabase.adminInfo

app = Flask(__name__)

app.config['SECRET_KEY']='5791628bb0b13ce0c676dfde280ba245'

@app.route("/")#home page route
@app.route("/home")

def home():
    session.pop('user',None)
    return render_template('home.html')

@app.route("/about")
def about():
    return render_template('about.html',title="ABOUT")

@app.route("/register",methods=['GET','POST'])
def register():
    form=RegistrationForm()
    if form.validate_on_submit():
        email=form.email.data
        password=form.password.data
        user_data = loginDB.find_one({'email': email})
        if user_data:
            message="{} this email already exists".format(form.email.data)
            flash(message,"warning")
        else:
            user_data=loginDB.insert_one({"email":email,"password":password})
            message="Account is created with email {}".format(form.email.data)
            if user_data:flash(message,'success')
            return redirect(url_for('home'))#name of the function not file
    return render_template('register.html',title='Register',form=form)

@app.route("/login",methods=['GET','POST'])
def login():
    form=LoginForm()
    if form.validate_on_submit():
        session.pop('user',None)
        email=form.email.data
        user_password=form.password.data
        user_data = loginDB.find_one({'email': email})
        if user_data and user_data["password"] == user_password:
            session['user']=email
            message="You hava been logged as {}".format(email)
            flash(message,'success')
            return redirect(url_for('orderform'))
        else:
            flash('Login unsuccessful. Please check username and password','danger')
    return render_template('login.html',title='Login',form=form)

@app.before_request
def before_request():
    g.user=None
    if 'user' in session:
        g.user=session['user']

@app.route("/orderform",methods=['GET','POST'])
def orderform():
    form=OrderForm()
    if g.user:
        if request.method == "POST":
            name=request.form.get("name")
            phoneNumber=request.form.get("phoneNumber")
            email=session['user']
            address=request.form.get("address")
            number=request.form.get("number")
            print(name)
            print(email)
            print(phoneNumber)
            print(address)
            print(number)
            order=orderDB.insert_one({"name":name,"phonenumber":phoneNumber,"email":email,"address":address,"pieces":number,})
            if order:
                message="order is placed as {}".format(email)
                flash(message,"success")
                return redirect(url_for('home'))
            else:
                message="There is some issue in placing this order. Try again"
                flash(message,"warning")
                return redirect(url_for('home'))
        return render_template('orderForm.html',title="ORDER FORM",form=form,user=session['user'])

# @app.route("/orderForm",methods=['GET','POST'])
# def orderForm():
#     form=OrderForm()
#     if form.validate_on_submit():
#         name=form.name.data
#         phoneNumber=form.phoneNumber.data
#         email=form.email.data
#         address=form.address.data
#         number=form.number.data
#         message="order is placed as {}".format(email)
#         flash(message,"success")
#         # user_data = orderDB.insert_one({"email":email,"password":password})
#         # message="Your order is successfully placed"
#         # if user_data:
#         #     flash(message,'success')
#         #     return redirect(url_for('home'))
#         return render_template('home.html',title="Home")

@app.route("/adminlogin",methods=["GET","POST"])
def adminlogin():
    form=AdminLogin()
    if form.validate_on_submit():
        session.pop('user',None)
        email=form.email.data
        user_password=form.password.data
        user_data = adminDB.find_one({'email': email})
        if user_data and user_data["password"] == user_password:
            session['user']=email
            message="You hava been logged as {}".format(email)
            flash(message,'success')
            return redirect(url_for('orders'))    
        else:
            flash('Login unsuccessful. Please check username and password','danger')
    return render_template('admin.html',title="Orders Placed",form=form)

@app.route("/ordersplaced")
def orders():
    order=orderDB.find()
    return render_template('orders.html',title="Orders Placed",order=order)