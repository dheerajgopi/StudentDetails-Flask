# views.py

# imports
from flask import Flask, render_template, request, session, flash, redirect, url_for, g
import sqlite3

# config
DATABASE = 'students.db'
SECRET_KEY = 'password'
app = Flask(__name__)

# pulls in configs by looking for UPPERCASE variables
app.config.from_object(__name__)

# method for connecting to db
def connect_db() :
    return sqlite3.connect(app.config['DATABASE'])

# home page for submitting student id
@app.route('/',methods=['GET','POST'])
def index() :
    error = None
    if request.method == 'POST' :
        if not request.form['studentid'] :
            error = "Please enter a student ID"
            return render_template('index.html')
        student_id = (int(request.form['studentid']),)
        g.db = connect_db()
        cur = g.db.execute('SELECT * FROM student WHERE id = ?', student_id)
        details = cur.fetchone()
        g.db.close()
        if not details :
            error = "Invalid student ID"
            return render_template('index.html', error = error)
        else :
            s_id = details[0]
            first_name = details[1]
            last_name = details[2]
            mark = details[3]
        
            return redirect(url_for('details', stud_id = s_id,
                                            first_name = first_name,
                                            last_name = last_name,
                                            mark = mark))
    return render_template('index.html', error = error)

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

if __name__ == "__main__":
    app.run(debug = True)
