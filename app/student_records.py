# views.py

# imports
from flask import Flask, render_template, request, session, flash, redirect, url_for, g
import sqlite3

# config
DATABASE = 'students.db'

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
        student_id = request.form['studentid']
        return redirect(url_for('details', student_id = student_id))
    return render_template('index.html', error = error)

# page for showing the details of student
@app.route('/details/<student_id>')
def details(student_id) :
    sid = (int(student_id),)
    g.db = connect_db()
    cur = g.db.execute('SELECT * FROM student WHERE id = ?', sid)
    details = cur.fetchone()
    g.db.close()
    stud_id = details[0]
    f_name = details[1]
    l_name = details[2]
    mark = details[3]
    return render_template('details.html', student_id = stud_id,
                                            first_name = f_name,
                                            last_name = l_name,
                                            mark = mark)

if __name__ == "__main__":
    app.run(debug = True)
