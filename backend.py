from flask import Flask, request, render_template, redirect, url_for, session
import mysql.connector
import os
from werkzeug.utils import secure_filename

app = Flask(__name__, static_folder='static')

app.secret_key = 'your_secret_key'  

UPLOAD_FOLDER = 'static/images'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Database connection
db = mysql.connector.connect(
    host='localhost',
    user='root',
    password='vignesh493',
    database='employee_info'
)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    if 'username' not in session:
        return redirect(url_for('login'))
    cursor = db.cursor()
    cursor.execute("SELECT EID, NAME, ROLE, BRANCH, SALARY, profile_picture FROM et_1")
    employees = cursor.fetchall()
    return render_template('index.html', employees=employees, selected_employee=None)

@app.route('/edit_employee', methods=['POST'])
def edit_employee():
    eid = request.form.get('eid')
    cursor = db.cursor()
    cursor.execute("SELECT EID, NAME, ROLE, BRANCH, SALARY, profile_picture FROM et_1 WHERE EID = %s", (eid,))
    employee = cursor.fetchone()
    if employee:
        selected_employee = {
            'eid': employee[0],
            'name': employee[1],
            'role': employee[2],
            'branch': employee[3],
            'salary': employee[4],
            'profile_picture': employee[5] if employee[5] else 'default_profile.png'
        }
        cursor.execute("SELECT EID, NAME, ROLE, BRANCH, SALARY, profile_picture FROM et_1")
        employees = cursor.fetchall()
        return render_template('index.html', employees=employees, selected_employee=selected_employee)
    return redirect(url_for('index'))

@app.route('/update_employee', methods=['POST'])
def update_employee():
    eid = request.form.get('eid')
    name = request.form.get('name')
    role = request.form.get('role')
    branch = request.form.get('branch')
    salary = request.form.get('salary')

    # Handle profile picture upload
    profile_picture = request.files.get('profile_picture')
    if profile_picture and allowed_file(profile_picture.filename):
        filename = secure_filename(profile_picture.filename)
        profile_picture.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        picture_path = filename
    else:
        cursor = db.cursor()
        cursor.execute("SELECT profile_picture FROM et_1 WHERE EID = %s", (eid,))
        current_picture = cursor.fetchone()[0]
        picture_path = current_picture if current_picture else 'default_profile.png'

    cursor = db.cursor()
    cursor.execute("""UPDATE et_1
                      SET NAME = %s, ROLE = %s, BRANCH = %s, SALARY = %s, profile_picture = %s 
                      WHERE EID = %s""", (name, role, branch, salary, picture_path, eid))
    db.commit()
    return redirect(url_for('index'))

@app.route('/delete_employee', methods=['POST'])
def delete_employee():
    eid = request.form.get('eid')
    cursor = db.cursor()
    cursor.execute("DELETE FROM et_1 WHERE EID = %s", (eid,))
    db.commit()
    return redirect(url_for('index'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if username == 'vignesh4903' and password == 'arj74ruzmn7890':
            session['username'] = username
            return redirect(url_for('index'))
        else:
            return 'Invalid credentials'
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
