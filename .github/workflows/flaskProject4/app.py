from flask import Flask, jsonify, request
from flask_mysqldb import MySQL

app = Flask(__name__)

app.config['MYSQL_USER'] = 'DELL'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_HOST'] = '127.0.0.1'
app.config['MYSQL_DB'] = 'mysql'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)

@app.route('/')
def hello():
    return 'welcome page'

	
@app.route('/student/create', methods=['POST'])
def student():
    cur = mysql.connection.cursor()
    cur.execute('''CREATE TABLE student (id INTEGER PRIMARY KEY, name VARCHAR(20), subjects VARCHAR(200), Marks INTEGER, Exam_Result VARCHAR(20), Class_categorty varchar(80))''')
    return 'Student table created successfully. Please verify in mysql database', 200
	
@app.route('/student/add', methods=['PUT'])
def add_student():
    cur = mysql.connection.cursor()
    cur.execute('''INSERT INTO student VALUES (1, 'valli', 'Maths', 200, 'PASS', 'Distinction')''')
    cur.execute('''INSERT INTO student VALUES (2, 'laxmi', 'Physics', 150, 'PASS', 'First Class')''')
	cur.execute('''INSERT INTO student VALUES (3, 'Keerti', 'Science', 45, 'Fail', 'None')''')
	cur.execute('''INSERT INTO student VALUES (4, 'Keerti', 'Social', 112, 'PASS', 'Second Class')''')
    mysql.connection.commit()
    return 'Student details added successfully. Please verify in mysql database', 200
	
@app.route('/student/view', methods=['GET'])
def view_details():
    cur = mysql.connection.cursor()
    cur.execute('''select * from student''')
	results = cur.fetchall()
    print(results)
    if results is ():
		print('Data is not available in database')
        results = 'Data is not available in database'
    return jsonify(results)
	
@app.route('/student/display/<string:param>', methods=['GET'])
def view_details(param):
    cur = mysql.connection.cursor()
    cur.execute("select * from student where name = %s", [param])
    results = cur.fetchall()
    print(results)
    if results is ():
        print('student details for %s is not available in database', [param])
        results = 'student details for '+ str(param) + ' is not available in database'
    return jsonify(results)
	
@app.route('/student/view/<string:name>/<int:index>', methods=['GET'])
def view_details(index, name):
    cur = mysql.connection.cursor()
    cur.execute("select * from student where name = %s and id = %s", [name, index])
    results = cur.fetchall()
    print(results)
    if results is ():
        print('student details for %s is not available in database', [name])
    results = 'student details for ' + str(index) + ' is not available in database'
    return jsonify(results)
	
@app.route('/student/change/<int:index>', methods=['PUT'])
def update_details(index):
	try:
		cur = mysql.connection.cursor()
		cur.execute('''update student set marks= marks+20 where id = %d''')
		mysql.connection.commit()
	except MySQLdb.ProgrammingError as err:
		output = str(err) + ' Id entered does not available in table. Please provide valid index'
		print('Id entered does not available in table. Please provide valid index')
	else:
		output = 'Details updated for index [index]'
	return output
	
@app.route('/student/exam/<string:Exam_Result>', methods=['GET'])
def exam_details(Exam_Result):
	cur = mysql.connection.cursor()
	cur.execute('''select * from student where Exam_Result = %s''')
	results = cur.fetchall()
	print(results)
	if results is ():
		print('Data is not available in database')
		results = 'Data is not available in database'
	return str(results)
	
@app.route('/student/delete/<int:index>', methods=['DELETE'])
def del_details(index):
	cur = mysql.connection.cursor()
	cur.execute('''delete from student where id = %d''')
	mysql.connection.commit()
	return 'Deleted [index] successfully', 200
	
@app.route('/student/exam/<string:Exam_Result>-percentage', methods=['GET'])
def exam_details(Exam_Result):
	cur = mysql.connection.cursor()
	cur.execute('''select Exam_Result,(Count(Marks)* 100 / (Select Count(*) From student)) as percentage from student where Exam_Result = %s''')
	results = cur.fetchall()
	print(results)
	if results is ():
		print('Data is not available in database')
		results = 'Data is not available in database'
	return str(results)
	


	

	

	

	

	
	
