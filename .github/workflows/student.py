from flask import Flask, request, jsonify
from flaskext.mysql import MySQL
 
app = Flask(__name__)
mysql = MySQL()
 
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'root'
app.config['MYSQL_DATABASE_DB'] = 'jcg_schema'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)
connection = mysql.connect()
 
@app.route('/hello')
def hello():
    return 'Welcome!'
 
@app.route('/student', methods=['POST'])
def insert_student():
    new_student = request.get_json()
    insert_sql_query = "INSERT INTO Student ('name', 'roll_no') VALUES (%s, %s)"
    data = (new_student['name'], new_student['roll_no'])
    cursor = connection.cursor()
    cursor.execute(insert_sql_query, data)
    connection.commit()
    return 'Student inserted with name: %s' % new_student['name']
 
@app.route('/student/<student_id>', methods=['GET'])
def get_student(student_id):
    cursor = connection.cursor()
    cursor.execute("SELECT * from Student WHERE id='" + student_id + "'")
    student_data = cursor.fetchone()
    if student_data is None:
     return "Wrong ID passed."
    else:
     return jsonify(student_data)
 
@app.route('/student', methods=['PUT'])
def update_student():
    updated_student = request.get_json()
    update_sql_query = "Update Student SET name=%s, roll_no=%s WHERE id=%s"
    data = (updated_student['name'], updated_student['roll_no'], updated_student['id'])
    cursor = connection.cursor()
    cursor.execute(update_sql_query, data)
    connection.commit()
    return 'Student updated with ID: %s' % updated_student['id']
 
@app.route('/student/<int:student_id>', methods=['DELETE'])
def delete_student(student_id):
    cursor = connection.cursor()
    cursor.execute("DELETE FROM Student WHERE id=%s", (student_id,))
    connection.commit()
    return 'Deleted Student data with ID: %s' % student_id