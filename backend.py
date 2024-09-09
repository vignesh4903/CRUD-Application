from flask import Flask, request, render_template, redirect, url_for
import mysql.connector

app = Flask(__name__)

db = mysql.connector.connect(
    host='localhost',
    user='root',
    password='vignesh493',
    database='employee_info'
)

@app.route('/')
def index():
    cursor = db.cursor()
    cursor.execute("SELECT EID, NAME, ROLE, BRANCH, SALARY FROM et_1")
    employees = cursor.fetchall()
    return render_template('index.html', employees=employees)

@app.route('/edit', methods=['POST'])
def edit_employee():
    eid = request.form.get('eid')
    cursor = db.cursor()
    cursor.execute("SELECT EID, NAME, ROLE, BRANCH, SALARY FROM et_1 WHERE EID = %s", (eid,))
    employee = cursor.fetchone()
    if employee:
        selected_employee = {
            'eid': employee[0],
            'name': employee[1],
            'role': employee[2],
            'branch': employee[3],
            'salary': employee[4]
        }
        return render_template('index.html', employees=[employee], selected_employee=selected_employee)
    return redirect(url_for('index'))

@app.route('/update_employee', methods=['POST'])
def update_employee():
    eid = request.form.get('eid')
    name = request.form.get('name')
    role = request.form.get('role')
    branch = request.form.get('branch')
    salary = request.form.get('salary')

    # Check if all required fields are present
    if not all([eid, name, role, branch, salary]):
        return redirect(url_for('index'))  # Redirect if any field is missing

    cursor = db.cursor()
    cursor.execute("""
        UPDATE et_1
        SET NAME = %s, ROLE = %s, BRANCH = %s, SALARY = %s 
        WHERE EID = %s
        """, (name, role, branch, salary, eid))
    db.commit()

    return redirect(url_for('index'))

@app.route('/delete', methods=['POST'])
def delete_employee():
    eid = request.form.get('eid')
    if not eid:
        return redirect(url_for('index'))  # Redirect if ID is missing

    cursor = db.cursor()
    query = "DELETE FROM et_1 WHERE EID = %s"
    cursor.execute(query, (eid,))
    db.commit()

    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
