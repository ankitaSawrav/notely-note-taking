
from crypt import methods
import bcrypt
import psycopg2 
from flask import Flask ,render_template,request,redirect,session

import os
import emailvalidator,database

DB_URL = os.environ.get('DATABASE_URL', 'dbname=project2')
SECRET_KEY = os.environ.get('SECRET_KEY', 'pretend secret key for testing')

app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY

@app.route('/')
def index():
#   getting session data
    user_id = session.get('user_id')
    username = session.get('username')
    print(f'this is {user_id} & {username}')
    return render_template('index.html', username = session.get('username') )


@app.route('/search_action')
def search_action():
    user_search_text = request.args.get("user_search")
    print(user_search_text)
    
    
    parameter_db_search = "%"+user_search_text+"%"
    print(parameter_db_search)
    conn = psycopg2.connect('dbname=project2')
    cur = conn.cursor()
    cur.execute('SELECT * FROM notes WHERE title like %s  or notes_description like %s',[parameter_db_search,parameter_db_search]) # Query to check that the DB connected
    results = cur.fetchall()
    print(results)
    conn.close()
    if  results == None:
        return render_template('index.html',results ='there are no results based on your search',username = session.get('username'))
    else:   
        return render_template('index.html', results = results,username = session.get('username'))
@app.route('/signin')
def display_signin():
    return render_template('signin.html',username = session.get('username')) 

@app.route('/signin_action',methods=['POST'])
def signin():
    username = request.form.get("name")
    email = request.form.get('email')
    password = request.form.get('password')
    print(f'username: {username} email : {email} password: {password}')
    if emailvalidator.isValidEmail(email):
        print("in if loop if email is valid")
        print(emailvalidator.isValidEmail(email))
        password_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        print
        database.sql_write('INSERT INTO users(user_name, user_email , password_hash)values(%s,%s,%s)',[username,email,password_hash])
        return render_template('login.html',username = session.get('username'))
    else:
        print('in else loop')
        print(emailvalidator.isValidEmail(email))
        return render_template('signin.html',result = 'Please enter a valid email address example@hit.com',username = session.get('username'))
   
@app.route('/login')    
def login():
    
    return render_template('login.html',username = session.get('username'))

@app.route('/login_action' ,methods=['POST'])
def on_login_action():
    email = request.form.get('email')
    password = request.form.get("password")
    print(f'login: {email} password : {password}')
    # user_id | user_name |    user_email    | password_h
    results = database.sql_fetch('SELECT user_id,user_name,user_email,password_hash FROM users where user_email=%s',[email])
    print(results)
    if not results:
        return render_template("login.html",message = "Please enter a valid email address",username = session.get('username'))
    else:
        password_hash=results[0][3]# hashed password from database
        valid = bcrypt.checkpw(password.encode(), password_hash.encode())
        if valid:
            user_id = results[0][0]
            user_name = results[0][1]
            print('passwordvalid')
            print(f'userid={user_id} username = {user_name}')
            # setting session cookies
            session['user_id'] = user_id
            session['username'] = user_name

            return redirect('/')
        else:    
            return render_template('login.html',message = " Incorrect password !! ",username = session.get('username'))



#Add new note 

@app.route('/add_notes')
def add_note():
    return render_template('/addnote.html',username = session.get('username'))

@app.route('/add_notes_action' ,methods=['GET'])
def add_notes_action():
    user_id = 1
    new_note_title = request.args.get("title")
    new_note_content = request.args.get("notes-content")
    print(new_note_title) 
    print(new_note_content) 
    # insert into notes(user_id, title , notes_description ) VAlUES (1,'test data' , 'adding test data');

    database.sql_write('INSERT INTO notes(user_id, title , notes_description ) VALUES (%s,%s, %s)', [user_id,new_note_title, new_note_content])
    return render_template('index.html',username = session.get('username'))

@app.route('/note', methods=['GET'])
def get_note_details():
    note_id = request.args.get('id')
    print(note_id)
    note_details = database.sql_fetch('SELECT * FROM notes WHERE notes_id = %s', [note_id])
    print(note_details)
    return render_template('notes.html',notes = note_details,username = session.get('username'))





@app.route('/logout')
def logout():
  session.clear()
  return redirect('/')




if __name__ == "__main__":
    app.run(debug=True)