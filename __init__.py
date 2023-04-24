from flask import Blueprint,request,render_template,redirect, make_response
from micro_db import MicroDB
import hashlib,os

from config import elentoolkit

_current_url = '/etk'

bp = Blueprint("etk", __name__, url_prefix=_current_url,template_folder='./templates')

db = MicroDB('etk_db')

security_salt = str(os.getenv('elentoolkit_secretkey'))

print(bp.template_folder)

def check_session():
    username = str(request.cookies.get('username'))
    auth_cookie = str(request.cookies.get('auth'))
    if username != 'None' and auth_cookie != 'None':
        password = str(db.get(f'users:{username}:password'))
        sha512hash = hashlib.sha512(str(username+password+security_salt).encode('utf-8')).hexdigest()
        if auth_cookie == sha512hash:
            return True
    return False



@bp.route('/')
def index():
    return redirect('home')

@bp.route('/tutorial')
def tutorial():
    return render_template('etk_tutorial.html')


# Login Page
@bp.route('/login',methods=['GET','POST'])
def login():

    # Response GET with a page, pass if is POST
    if request.method == 'GET':
        return render_template('etk_login.html')
    
    # Get Form Values
    username = str(request.form.get('username'))
    password = str(request.form.get('password'))

    # DEBUG
    print('Attempt to login with: ',username,password)
    
    # Anti None Inputs (for more security, i don't like None users with None password)
    if username != 'None' and password != 'None':
        user_password = str(db.get(f'users:{username}:password'))

        if user_password == password:
            print('login-success')
            sha512hash = hashlib.sha512(str(username+password+security_salt).encode('utf-8')).hexdigest()

            resp = make_response(redirect('home'))
            resp.set_cookie('username',username,3*24*60*60,secure=True,path=_current_url)
            resp.set_cookie('auth',sha512hash,3*24*60*60,secure=True,path=_current_url)
            print(resp)
            return resp
        elif user_password == 'None':
            print('login-notexist')
            return redirect('signup')
    
    print('login-failed')
    return render_template('etk_login.html')

# Signup Page
@bp.route('/signup',methods=['GET','POST'])
def signup():
    if request.method == 'GET':
        return render_template('etk_signup.html')
    
    name = str(request.form.get('name'))
    username = str(request.form.get('username'))
    password = str(request.form.get('password'))

    print('Attempt to signup with: ',name,username,password)
    
    if name != 'None' and username != 'None' and password != 'None':
        if not db.get(f'users:{username}:password'):
            print('signup-success')
            db.set(f'users:{username}:name',name)
            db.set(f'users:{username}:password',password)

            sha512hash = hashlib.sha512(str(username+password+security_salt).encode('utf-8')).hexdigest()

            resp = make_response(redirect('home'))
            resp.set_cookie('username',username,3*24*60*60,secure=True,path=_current_url)
            resp.set_cookie('auth',sha512hash,3*24*60*60,secure=True,path=_current_url)
            return resp
    
    print('signup-failed')
    return redirect('login')

@bp.route('/logout')
def logout():
    resp = make_response(redirect('login'))
    resp.delete_cookie('auth')
    resp.delete_cookie('username')
    return resp


@bp.route('/home')
def home():
    if not check_session():
        return redirect('login')
    username = request.cookies.get('username')
    return render_template('etk_home.html',name=db.get(f'users:{username}:name'))


@bp.route('/imc',methods=['GET','POST'])
def imc():
    if not check_session():
        return redirect('login')

    if request.method == 'GET':
        return render_template('etk_imc.html')
    age = int(request.form.get('age'))
    weight = float(request.form.get('weight'))
    height = float(request.form.get('height'))

    imc = round(weight/(height*height),2)

    if imc < 16.9:
        imc_type = 'Muito abaixo do peso'
        imc_response = 'Entre o vento e você, não há diferenças.'
    elif imc >= 17 and imc <= 18.4:
        imc_type = 'Abaixo do peso'
        imc_response = 'Não entre em brigas.'
    elif imc >= 18.5 and imc <= 24.9:
        imc_type = 'Peso ideal/normal'
        imc_response = 'Saudável, não há muito o que dizer.'
    elif imc >= 25 and imc <= 29.9:
        imc_type = 'Acima do peso'
        imc_response = 'Bom para lutas, desde que respeite a regra número 1.'
    elif imc >= 30 and imc <= 34.9:
        imc_type = 'Obesidade grau 1'
        imc_response = 'Corrar um pouco, coma menos.'
    elif imc >= 35 and imc <= 40:
        imc_type = 'Obesidade grau 2'
        imc_response = 'Arremesse seus apetrechos gamer pela janela e vá correr!'
    elif imc >= 40:
        imc_type = 'Obesidade grau 3'
        imc_response = '...'

    return render_template('etk_imc.html',imc_result = [imc,imc_type,imc_response],age=age,weight=weight,height=height)