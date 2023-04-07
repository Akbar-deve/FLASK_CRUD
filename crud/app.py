from flask import Flask, render_template, make_response, request, url_for, flash, jsonify
from werkzeug.utils import redirect
from flask_mysqldb import MySQL
import jwt
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
import datetime
from functools import wraps



app = Flask(__name__)
app.secret_key = 'many random bytes'

app.config['SECRET_KEY'] = 'key' 
# jwt = JWTManager(app)

# here i have mentioned my database cridentials 

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'crud'


mysql = MySQL(app)

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):

        token = request.args.get('token')
        if not token:
            return jsonify({'message':'token is missing'}), 403
        try:
            data = jwt.decode(token, app.config['SECRET_KEY]'])
        except:
            return jsonify({'message':'token is invalid'}), 403
        return f(*args, **kwargs)
    return decorated

@app.route('/unprotected')

def unprotected():
    return jsonify({'message':'any one can view this'})

@app.route('/protected')
@token_required
def protected():
    return jsonify({'message':'this is only avaliable for people with valid tokens.'})


#when you enter the url in browser then 1st it ask you to login
# then to see the data you need to write http://127.0.0.1:5000/index
@app.route('/')
def login():
    auth = request.authorization
    if auth and auth.password == 'amd': #this is my password

        token = jwt.encode({'user': auth.username, 'exp' : datetime.datetime.utcnow() + datetime.timedelta(seconds= 15) }, app.config['SECRET_KEY'])
        return jsonify({'token': token.encode().decode('UTF-8')})   #jsonify({'message': 'successfully'})
    
    return make_response('Could not verify!', 401, {'www-Authenticate':'Basic realm="Login required"'})
    




# it will fetch all the data from mysql databade 
@app.route('/index')
def Index():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM ta")
    data = cur.fetchall()
    cur.close()
    return render_template('index.html', ta=data)


@app.route('/insert', methods = ['POST'])
def insert():
    if request.method == "POST":
        # flash("Data Inserted Successfully")
        # id_data = request.form['id']
        native_english_speaker = request.form['native_english_speaker'] 
        course_instructor = request.form['course_instructor']
        course = request.form['course']
        semester = request.form['semester']
        class_size = request.form['class_size']
        performance_score = request.form['performance_score']

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO ta (native_english_speaker, course_instructor, course, semester,  class_size, performance_score  ) VALUES (%s, %s, %s, %s, %s, %s)", ( native_english_speaker, course_instructor, course, semester,  class_size, performance_score ))
        mysql.connection.commit()
        # this will redirect to the index page 
        # return redirect(url_for('Index'))

        # this will give the json response as data inserted , im using json 
        return jsonify({'message': 'Data Inserted successfully'})

@app.route('/delete/<string:id_data>', methods = ['GET'])
def delete(id_data):
    # flash("Record Has Been Deleted Successfully")
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM ta WHERE id=%s", (id_data,))
    mysql.connection.commit()
    return redirect(url_for('Index'))
    # return jsonify({'message': 'Data Deleted successfully'})


@app.route('/update', methods= ['POST', 'GET'])
def update():
    if request.method == 'POST':
        id_data = request.form['id']
        native_english_speaker = request.form['native_english_speaker']
        course_instructor = request.form['course_instructor']
        course = request.form['course']
        semester = request.form['semester']
        class_size = request.form['class_size']
        performance_score = request.form['performance_score']




        cur = mysql.connection.cursor()
        cur.execute("""
        UPDATE ta SET native_english_speaker=%s, course_instructor=%s, course=%s, semester=%s, class_size=%s, performance_score=%s
        WHERE id=%s
        """, (native_english_speaker, course_instructor, course, semester, class_size, performance_score, id_data))
        # flash("Data Updated Successfully")
        
        mysql.connection.commit()
        # return redirect(url_for('Index'))
        return jsonify({'message': 'Data Updated successfully'})




if __name__ == "__main__":
    app.run(debug=True)