from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('students.db')
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            roll TEXT UNIQUE,
            marks INTEGER
        )
    ''')
    conn.commit()
    conn.close()

init_db()


@app.route('/')
def dashboard():
    return render_template('dashboard.html')


@app.route('/add', methods=['GET', 'POST'])
def add():
    conn = sqlite3.connect('students.db')
    cur = conn.cursor()

    if request.method == 'POST':
        name = request.form['name']
        roll = request.form['roll']
        marks = request.form['marks']

        try:
            cur.execute("INSERT INTO students (name, roll, marks) VALUES (?, ?, ?)", 
                        (name, roll, marks))
            conn.commit()
        except:
            pass  

        return redirect(url_for('add'))

    students = cur.execute("SELECT * FROM students").fetchall()
    conn.close()

    return render_template('add.html', students=students)


@app.route('/update', methods=['GET', 'POST'])
def update():
    conn = sqlite3.connect('students.db')
    cur = conn.cursor()

    if request.method == 'POST':
        roll = request.form['roll']
        name = request.form['name']
        marks = request.form['marks']

        cur.execute("UPDATE students SET name=?, marks=? WHERE roll=?", 
                    (name, marks, roll))
        conn.commit()

        return redirect(url_for('update'))

    students = cur.execute("SELECT * FROM students").fetchall()
    conn.close()

    return render_template('update.html', students=students)


@app.route('/delete/<roll>')
def delete(roll):
    conn = sqlite3.connect('students.db')
    cur = conn.cursor()

    cur.execute("DELETE FROM students WHERE roll=?", (roll,))
    conn.commit()
    conn.close()

    return redirect(url_for('update'))


if __name__ == '__main__':
    app.run(debug=True)
