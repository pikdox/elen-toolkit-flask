# Imports
from flask import Flask,request,render_template,redirect, make_response
import hashlib, os


# Modules
from MicroDB import MicroDB
import secure
from utils import calc_imc


app = Flask(__name__)

users_db = MicroDB('users','./db/')

def check_session():
    username = str(request.cookies.get('username'))
    auth_cookie = str(request.cookies.get('auth'))

    if username != 'None' and auth_cookie != 'None':
        password = str(users_db.get(f'{username}:password'))

        login_hash = secure.craft_login_hash(username,password,True)

        if auth_cookie == login_hash:
            return True
    return False

@app.route('/')
def index():
    return redirect('home')

@app.route('/tutorial')
def tutorial():
    return render_template('tutorial.html')

# Login Page
@app.route('/login',methods=['GET','POST'])
def login():

    # Response GET with a page, pass if is POST
    if request.method == 'GET':
        return render_template('login.html')
    
    # Get Form Values
    username = str(request.form.get('username'))
    password = str(request.form.get('password'))
    
    # Anti None Inputs (for more security, i don't like None users with None password)
    if username != 'None' and password != 'None':
        db_user_password = str(users_db.get(f'{username}:password'))

        if secure.hash_compare(password,db_user_password):
            login_hash = secure.craft_login_hash(username,password)
            resp = make_response(redirect('home'))
            resp.set_cookie('username',username,3*24*60*60,secure=True)
            resp.set_cookie('auth',login_hash,3*24*60*60,secure=True)
            return resp
        
        elif db_user_password == 'None':
            return redirect('signup')
    
    return render_template('login.html')

# Signup Page
@app.route('/signup',methods=['GET','POST'])
def signup():
    if request.method == 'GET':
        return render_template('signup.html')
    
    name = str(request.form.get('name'))
    username = str(request.form.get('username'))
    password = str(request.form.get('password'))
    
    if name != 'None' and username != 'None' and password != 'None':
        if not users_db.get(f'{username}:password'):
            
            password = secure.craft_hash(password)

            users_db.set(f'{username}:name',name)
            users_db.set(f'{username}:password',password)

            login_hash = secure.craft_login_hash(username,password,True)

            resp = make_response(redirect('home'))
            resp.set_cookie('username',username,3*24*60*60,secure=True)
            resp.set_cookie('auth',login_hash,3*24*60*60,secure=True)
            return resp
    
    return redirect('login')

@app.route('/logout')
def logout():
    resp = make_response(redirect('login'))
    resp.delete_cookie('auth')
    resp.delete_cookie('username')
    return resp


@app.route('/home')
def home():
    if not check_session():
        return redirect('login')
    username = request.cookies.get('username')
    return render_template('home.html',name=users_db.get(f'{username}:name'))


@app.route('/imc',methods=['GET','POST'])
def value():
    if not check_session():
        return redirect('login')

    if request.method == 'GET':
        return render_template('imc.html')
    
    username = request.cookies.get('username')

    weight = float(request.form.get('weight'))
    height = float(request.form.get('height'))

    users_db.set(f'{username}:weight',weight)
    users_db.set(f'{username}:height',height)

    imc_result = calc_imc(weight,height)
    
    users_db.set(f'{username}:imc',imc_result.get('value'))

    return render_template('imc.html',imc_result=imc_result, weight=weight, height=height)

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')