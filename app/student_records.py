# views.py

# imports
from flask import Flask, render_template, request, session, flash, redirect, url_for, g
import sqlite3
from functools import wraps

# config
DATABASE = 'students.db'
USERNAME = 'admin'
PASSWORD = 'admin'
SECRET_KEY = 'password'
app = Flask(__name__)

# pulls in configs by looking for UPPERCASE variables
app.config.from_object(__name__)

# method for connecting to db
def connect_db() :
    return sqlite3.connect(app.config['DATABASE'])

def login_required(test):
    @wraps(test)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return test(*args, **kwargs)
        else:
            flash('You need to login first.')
            return redirect(url_for('login'))
    return wrap

# login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME'] or request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid Credentials. Please try again.'
        else:
            session['logged_in'] = True
            return redirect(url_for('home'))
    return render_template('login.html', error=error)

# logout
@app.route('/logout')
def logout() :
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('home'))

# home page
@app.route('/', methods=["GET","POST"])
def home() :
    if request.method == "POST" :
        return redirect(url_for('view_all'))
    return render_template('home.html')

# view all records
@app.route('/view_all')
def view_all():
    g.db = connect_db()
    cur = g.db.execute('SELECT * FROM student')
    entries = [dict(stud_id=row[0],
                    f_name=row[1],
                    l_name=row[2],
                    mark=row[3]) for row in cur.fetchall()]
    g.db.close()
    return render_template('view_all.html', entries=entries)

# search page for submitting student id
@app.route('/search',methods=['GET','POST'])
def search() :
    error = None
    if request.method == 'POST' :
        if not request.form['studentid'] :
            error = "Please enter a student ID"
            return render_template('search.html')
        student_id = (int(request.form['studentid']),)
        g.db = connect_db()
        cur = g.db.execute('SELECT * FROM student WHERE id = ?', student_id)
        details = cur.fetchone()
        g.db.close()
        if not details :
            error = "Invalid student ID"
            return render_template('search.html', error = error)
        else :
            s_id = details[0]
            first_name = details[1]
            last_name = details[2]
            mark = details[3]
        
            return redirect(url_for('details', stud_id = s_id,
                                            first_name = first_name,
                                            last_name = last_name,
                                            mark = mark))
    return render_template('search.html', error = error)

# page for showing the details of student
@app.route('/details/<stud_id>/<first_name>/<last_name>/<mark>')
def details(stud_id, first_name, last_name, mark) :
    stud_id = stud_id
    f_name = first_name
    l_name = last_name
    mark = mark
    return render_template('details.html', student_id = stud_id,
                                            first_name = f_name,
                                            last_name = l_name,
                                            mark = mark)

# page for adding students
@app.route('/add', methods=['GET','POST'])
@login_required
def add():
    if request.method == 'GET' :
        return render_template('add.html')
    else :
        student_id = request.form['student_id']
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        mark = request.form['mark']
        if not student_id or not first_name or not last_name or not mark:
            flash("All fields are required. Please try again.")
            return redirect(url_for('add'))
        else:
            g.db = connect_db()
            g.db.execute('''INSERT INTO student (id,
                                                first_name,
                                                last_name,
                                                mark) VALUES(?, ?, ?, ?)''',
                                                [request.form['student_id'],
                                                 request.form['first_name'],
                                                 request.form['last_name'],
                                                 request.form['mark']])
            g.db.commit()
            g.db.close()
            flash('New entry was successfully posted')
            return redirect(url_for('search'))

# page for deleting students
@app.route('/delete', methods = ['GET','POST'])
@login_required
def delete():
    if request.method == 'GET' :
        return render_template('delete.html')
    else :
        if not request.form['studentid'] :
            flash("Please enter a student ID")
            return render_template('delete.html')
        student_id = (int(request.form['studentid']),)
        g.db = connect_db()
        cur = g.db.execute('DELETE FROM student WHERE id = ?', student_id)
        g.db.commit()
        g.db.close()
        flash('The entry was deleted.')
        return redirect(url_for('search'))

if __name__ == "__main__":
    app.run(debug = True)
