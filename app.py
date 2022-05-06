
from crypt import methods
import json
from pydoc import describe
from unittest import result
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
    return render_template('index.html', username = session.get('username'),user_id = session.get('user_id') )

@app.route('/search_action')
def search_action():
    user_search_text = request.args.get("user_search")
    print(user_search_text)
    parameter_db_search = "%"+user_search_text+"%"
    print(parameter_db_search)
    # 
    search_word_list = emailvalidator.search_by_words(user_search_text)
    print (search_word_list)

    conn = psycopg2.connect(DB_URL)
    cur = conn.cursor()
    cur.execute('SELECT * FROM notes WHERE title like %s  or notes_description like %s ORDER BY likes DESC',[parameter_db_search,parameter_db_search]) # Query to check that the DB connected
    results = cur.fetchall()
    # print(results)
    conn.close()
    # converting results into a dictionary:
    notes_dic = convert_db_result_to_dic(results)
    
    if  results == None:
        return render_template('index.html',errorMsg ='There are no results based on your search',username = session.get('username'), notes_dic = None, user_id = session.get('user_id'))
    else:   
        return render_template('index.html',errorMsg='', username = session.get('username'), notes_dic = notes_dic, user_id = session.get('user_id'))


@app.route('/signup')
def display_signup():
    return render_template('signup.html',username = session.get('username')) 


@app.route('/signup_action',methods=['POST'])
def signup():
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
        return render_template('signup.html',result = 'Please enter a valid email address example@hit.com',username = session.get('username'))


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
    user_id = session.get('user_id')
    
    print (user_id)

    new_note_title = request.args.get("title")
    new_note_content = request.args.get("notes-content")
    print(new_note_title) 
    print(new_note_content)
    likes = 0
    dislikes = 0
    # insert into notes(user_id, title , notes_description ) VAlUES (1,'test data' , 'adding test data');

    database.sql_write('INSERT INTO notes(user_id, title , notes_description,likes,dislikes ) VALUES (%s,%s, %s,%s,%s)', [user_id,new_note_title, new_note_content,likes,dislikes])
    return render_template('index.html',username = session.get('username'))

# EDIT a note 

@app.route('/editnote',methods=['GET','POST'])
def edit_note():
    note_id=request.form.get("id")
    print(note_id)
    search_results = database.sql_fetch('select * from notes where notes_id=%s',[note_id])
    print(search_results)
    title = search_results[0][2]
    content = search_results[0][3]
    
    
    return render_template('editnote.html',username = session.get('username'),title= title, content = content, note_id=note_id)
    

@app.route('/edit_notes_action', methods=['POST'])
def edit_notes_action():
    note_id = request.form.get("note_id")
    username = session.get('username')
    title = request.form.get("title")
    description = request.form.get("notes-content")
    print(note_id)
    print(username)
    print(f'edit note page:{title}')
    print(description)
    
    database.sql_write('UPDATE notes SET  title = %s ,notes_description= %s WHERE notes_id=%s',[title,description,note_id])
    return redirect("/")

# delete functionality:

@app.route('/deletenote',methods=['GET','POST'])
def delete_note():
    note_id=request.form.get("id")
    print(note_id)
    search_results = database.sql_fetch('select * from notes where notes_id=%s',[note_id])
    print(f'delete note page: {search_results}')
    title = search_results[0][2]
 
    return render_template('deletenote.html',username = session.get('username'), note_id = note_id,title=title )
    

@app.route('/delete_notes_action', methods=['POST'])
def delete_notes_action():
    note_id = request.form.get("note_id")
    username = session.get('username')
    print(note_id)
    print(username)
    database.sql_write('DELETE FROM notes WHERE notes_id=%s',[note_id])
    return redirect("/")
    
   


@app.route('/note', methods=['GET'])
def get_note_details():
    note_id = request.args.get('id')
    session_user_id =session.get('user_id')
    print(session_user_id)
    results = database.sql_fetch('SELECT * FROM notes WHERE notes_id = %s', [note_id])
    
    note_details= convert_db_result_to_dic(results)
    print(note_details)
    for note in note_details:
        notes_user_id = note['user_id']
        if notes_user_id is None:
            notes_user_id='Guest'
   
        return render_template('notes.html',notes = note,username = session.get('username'),user_id=session_user_id,notes_user_id=notes_user_id)

@app.route('/like-dislike')
def like_dislike_action():
    id = request.args.get("id")
    value = request.args.get("value")
    print(id)
    print(value)
    # fetch note data by noteid
    conn = psycopg2.connect(DB_URL)
    cur = conn.cursor()
    if value == 'likes':
        print ('likes')
        cur.execute('Select likes from notes where notes_id=%s', [id])
        result = cur.fetchone()
        lcount=result[0] + 1
        print(lcount)
        
        database.sql_write('UPDATE notes SET likes=%s where notes_id=%s', [lcount,id])
        return redirect("/")
    else:
        cur.execute('Select dislikes from notes where notes_id=%s', [id])
        result = cur.fetchone()
        dcount=result[0] + 1
        print(dcount)
        database.sql_write('UPDATE notes SET dislikes=%s where notes_id=%s', [dcount,id])
        return redirect("/")
    


@app.route('/logout')
def logout():
  session.clear()
  return redirect('/')


def convert_db_result_to_dic(results):
    print(results)
    dic = []
    for row in results:
        note = {
            'notes_id': row[0],
            'user_id': row[1],
            'title': row[2],
            'notes_description': row[3],
            'likes': row[4],
            'dislikes': row[5]
        }
        dic.append(note)
    print(dic)
    print(json.dumps(dic, indent=4))
    return dic




if __name__ == "__main__":
    app.run(debug=True)