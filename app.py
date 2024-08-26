import datetime
from flask import Flask, flash, redirect, render_template, request, url_for
from dotenv import load_dotenv, find_dotenv
import os
import pprint
from pymongo import MongoClient
import certifi


load_dotenv(find_dotenv())

print (datetime.date.today())
password = os.environ.get("SECRET_KEY")
connection_string = f"mongodb+srv://jen:{password}@studentdb.thkbj.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(connection_string, tlsCAFile=certifi.where())

""" print all database names """
dbs = client.list_database_names()
db_student = client['student']
db_teacher = client['teachers']
db_parent = client['parents']

today = datetime.datetime.today()

""" print specific collection """
""" student_db = client.student
collections = student_db.list_collection_names()
print(collections)

def insert_student_doc():
    collection = student_db.profile
    profile_document = {
        "First Name": "Namjoo0n",
        "Last Name": "Kim",
        "Date of Birth (MM-DD-YYYY)": {
    "$date": (1995,12,4)
  }
    }
    inserted_id = collection.insert_one(profile_document).inserted_id
    print(inserted_id)

insert_student_doc()
 """
""" db_teacher = client.teachers
collections = db_teacher.list_collection_names()
print(collections)

def insert_teacher_doc():
    collection = db_teacher.profile
    profile_document = {
        "First Name": "Namjoo0n",
        "Last Name": "Kim",
        "email": "test@gmail.com",
        "password": "test"
  }
    inserted_id = collection.insert_one(profile_document).inserted_id
    print(inserted_id)

insert_teacher_doc() """

app = Flask(__name__)

@app.route("/")
def home():
    return render_template('home.template.html')


# TEACHER PROFILE

@app.route('/teachers')
def show_teachers():
    all_teachers = db_teacher.teachers.find()
    print(all_teachers)
    return render_template('teachers/teacher_profile.template.html',
                           all_teachers=all_teachers)


# TEACHER SIGN UP
@app.route('/teachers/signup')
def show_create_teacher():
    return render_template('teachers/create_teacher.template.html')


@app.route('/teachers/signup', methods=["POST"])
def process_create_teacher():
    first_name = request.form.get("first_name")
    last_name = request.form.get("last_name")
    email = request.form.get("email")
    password = request.form.get("password")

    new_record = {
        "first_name": first_name,
        "last_name": last_name,
        "email": email,
        'password': password
    }

    db_teacher.teachers.insert_one(new_record)
    flash("Sign up successful")
    return redirect(url_for('show_teachers'))


# TEACHER LOGIN

@app.route('/teachers/login')
def teacher_login():
    return render_template('teachers/login_teacher.template.html')


@app.route('/teachers/login', methods=["POST", "GET"])
def process_teacher_login():
    email = request.form.get('email')
    password = request.form.get('password')

    db_teacher.teachers.find_one({
        'email': email,
        'password': password
    })

    return redirect(url_for("show_teachers"))


# PARENTS MAIN PAGE

@app.route('/parents')
def show_parents():
    all_parents = db.parents.find()
    return render_template('parents/all_parents.template.html',
                           all_parents=all_parents)


# PARENT SIGN UP

@app.route('/parents/signup')
def show_create_parent():
    return render_template('parents/create_parent.template.html')


@app.route('/parents/signup', methods=["POST"])
def process_create_parent():
    first_name = request.form.get("first_name")
    last_name = request.form.get("last_name")
    email = request.form.get("email")
    password = request.form.get("password")

    if len(first_name) == 0:
        flash("Name cannot be empty", "error")
        return redirect(url_for('show_create_parent'))

    new_record = {
        "first_name": first_name,
        "last_name": last_name,
        "email": email,
        'password': password
    }

    db.parents.insert_one(new_record)
    flash("Sign up successful")
    return redirect(url_for('show_parents'))


# PARENT LOGIN

@app.route('/parents/login')
def parent_login():
    return render_template('parents/login_parent.template.html')


@app.route('/parents/login', methods=["POST", "GET"])
def process_parents_login():
    email = request.form.get('email')
    password = request.form.get('password')

    db.parent.find_one({
        'email': email,
        'password': password
    })

    return redirect(url_for("show_parents"))


# STUDENT LIST

@app.route('/students')
def show_students():
    all_students = db.students.find()
    return render_template('students/all_students.template.html',
                           all_students=all_students)


# CREATE STUDENT MAIN DATABASE

@app.route('/students/create')
def show_create_student():
    return render_template('students/create_student.template.html')


@app.route('/students/create', methods=["POST"])
def process_create_student():
    first_name = request.form.get("first_name")
    last_name = request.form.get("last_name")
    date_of_birth = request.form.get("date_of_birth")
    clock_in = request.form.get("clock_in")
    clock_out = request.form.get("clock_out")
    temparature = request.form.get("temparature")
    class_groupId = request.form.get("class_groupId")
    teacher = request.form.get("teacher")
    remarks = request.form.get("remarks")

    new_record = {
        "first_name": first_name,
        "last_name": last_name,
        "date_of_birth": date_of_birth,
        "clock_in": clock_in,
        "clock_out": clock_out,
        "temparature": temparature,
        "class_groupId": class_groupId,
        "teacher": teacher,
        "remarks": remarks
    }

    db.students.insert_one(new_record)
    return redirect(url_for('show_students'))


# EDIT STUDENT MAIN DATABASE

@app.route('/students/edit/<student_id>')
def show_edit_student(student_id):
    student = db.students.find_one({
        '_id': ObjectId(student_id)
    })
    return render_template('students/edit_student.template.html',
                           student=student, today=today)


@app.route('/students/edit/<student_id>', methods=["POST"])
def process_edit_student(student_id):
    first_name = request.form.get("first_name")
    last_name = request.form.get("last_name")
    date_of_birth = request.form.get("date_of_birth")
    clock_in = request.form.get("clock_in")
    clock_out = request.form.get("clock_out")
    class_groupId = request.form.get("class_groupId")
    teacher = request.form.get("teacher")

    db.students.update_one({
        "_id": ObjectId(student_id)
    }, {
        "$set": {
            "first_name": first_name,
            "last_name": last_name,
            "date_of_birth": date_of_birth,
            "clock_in": clock_in,
            "clock_out": clock_out,
            "class_groupId": class_groupId,
            "teacher": teacher
        }
    })
    return redirect(url_for('show_students'))


# STUDENT PROFILE

@app.route('/students/profile')
def show_student_profile():
    all_student_profile = db.students.find()
    return render_template('students/student_profile.template.html',
                           all_student_profile=all_student_profile)


# EDIT STUDENT PROFILE

@app.route('/students/profile/edit/<student_id>')
def show_edit_student_profile(student_id):
    all_student_profile = db.students.find_one({
        '_id': ObjectId(student_id)
    })
    return render_template('students/edit_student_profile.template.html',
                           all_student_profile=all_student_profile)


@app.route('/students/profile/edit/<student_id>', methods=["POST"])
def process_edit_student_profile(student_id):
    first_name = request.form.get("first_name")
    last_name = request.form.get("last_name")
    date_of_birth = request.form.get("date_of_birth")
    class_groupId = request.form.get("class_groupId")
    teacher = request.form.get("teacher")

    db.students.update_one({
        "_id": ObjectId(student_id)
    }, {
        "$set": {
            "first_name": first_name,
            "last_name": last_name,
            "date_of_birth": date_of_birth,
            "class_groupId": class_groupId,
            "teacher": teacher
        }
    })
    return redirect(url_for('show_student_profile'))


# STUDENT ATTENDANCE

@app.route('/students/attendance')
def show_student_attendance():
    all_student_attendance = db.students.find()
    return render_template('students/student_attendance.template.html',
                           all_student_attendance=all_student_attendance)


# EDIT STUDENT PROFILE

@app.route('/students/attendance/edit/<student_id>')
def show_edit_student_attendance(student_id):
    all_student_attendance = db.students.find_one({
        '_id': ObjectId(student_id)
    })
    return render_template('students/edit_student_attendance.template.html',
                           all_student_attendance=all_student_attendance,
                           today=today)


@app.route('/students/attendance/edit/<student_id>', methods=["POST"])
def process_edit_student_attendance(student_id):
    first_name = request.form.get("first_name")
    last_name = request.form.get("last_name")
    temparature = request.form.get("temparature")
    clock_in = request.form.get("clock_in")
    clock_out = request.form.get("clock_out")
    teacher = request.form.get("teacher")

    remarks = request.form.get("remarks")

    db.students.update_one({
        "_id": ObjectId(student_id)
    }, {
        "$set": {
            "first_name": first_name,
            "last_name": last_name,
            "temparature": temparature,
            "clock_in": clock_in,
            "clock_out": clock_out,
            "teacher": teacher,
            "remarks": remarks
        }
    })
    return redirect(url_for('show_student_attendance'))


# DELETE STUDENT FROM MAIN DATABASE

@app.route('/students/delete/<student_id>')
def show_confirm_delete(student_id):
    students_to_be_deleted = db.students.find_one({
        "_id": ObjectId(student_id)
    })
    return render_template('students/show_confirm_delete.template.html',
                           student=students_to_be_deleted)


@app.route('/students/delete/<student_id>', methods=["POST"])
def confirm_delete(student_id):
    db.students.remove({
        "_id": ObjectId(student_id)
    })
    return redirect(url_for("show_students"))


# SEARCH

@app.route('/teachers/search')
def show_search_form():
    return render_template('search.template.html')


@app.route('/teachers/search', methods=['POST'])
def process_search_form():
    first_name = request.form.get('first_name')
    class_groupId = request.form.get('class_groupId')
    teacher = request.form.get('teacher')

    critera = {}

    if first_name:
        critera['first_name'] = {
            '$regex': first_name,
            '$options': 'i'  # i means 'case-insensitive'
        }

    if class_groupId:
        critera['class_groupId'] = {
            '$regex': class_groupId,
            '$options': 'i'  # i means 'case-insensitive'
        }

    if teacher:
        critera['teacher'] = {
            '$regex': teacher,
            '$options': 'i'  # i means 'case-insensitive'
        }

    searched_by = [first_name, class_groupId, teacher]

    results = db.students.find(critera)
    
    return render_template('students/display_student.template.html',
                           all_students=results,
                           searched_by=searched_by)


@app.route('/logout')
def logout():
    flash("You have been logged out!")
    return redirect(url_for("home"))

if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)
    
