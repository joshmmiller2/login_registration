from flask import render_template,redirect,session,request, flash
from flask_app import app
from flask_app.models.user import User
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/register', methods=['POST'])
def register():
    if not User.validate_register(request.form):
        # we redirect to the template with the form.
        return redirect('/')
    data ={ 
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form['email'],
        "password": bcrypt.generate_password_hash(request.form['password'])
        
    }
    user_id = User.save(data)
    # store user id into session
    session['User'] = user_id
    return redirect("/welcome")


@app.route('/')
def index():
    return render_template('index.html')

# @app.route('/register',methods=['POST'])
# def register():

#     data ={ 
#         "first_name": request.form['first_name'],
#         "last_name": request.form['last_name'],
#         "email": request.form['email'],
#         "password": bcrypt.generate_password_hash(request.form['password'])
#     }
#     id = User.save(data)
#     session['user_id'] = id

#     return redirect('/welcome')

@app.route('/login',methods=['POST'])
def login():
    emizzle = {'email': request.form['email']}
    user = User.get_by_email(emizzle)

    if not user:
        flash("Wrong Email Try Again", 'login')
        return redirect('/')
    if not bcrypt.check_password_hash(user.password, request.form['password']):
        flash("Wrong Password Try again", 'login')
        return redirect('/')
    session['user_id'] = user.id
    return redirect('/welcome')

@app.route('/welcome')
def dashboard():
    if 'user_id' not in session:
        return redirect('/logout')
    data ={
        'id': session['user_id']
    }
    return render_template("welcome.html",user=User.get_by_id(data))


@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')