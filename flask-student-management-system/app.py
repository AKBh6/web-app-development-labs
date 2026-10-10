from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.sqlite3'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


class Student(db.Model):
    __tablename__ = "student"

    student_id = db.Column(db.Integer, primary_key=True)
    roll_number = db.Column(db.String, unique=True, nullable=False)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String)


class Course(db.Model):
    __tablename__ = "course"

    course_id = db.Column(db.Integer, primary_key=True)
    course_code = db.Column(db.String, unique=True, nullable=False)
    course_name = db.Column(db.String, nullable=False)
    course_description = db.Column(db.String)


class Enrollment(db.Model):
    __tablename__ = "enrollments"

    enrollment_id = db.Column(db.Integer, primary_key=True)

    estudent_id = db.Column(
        db.Integer,
        db.ForeignKey("student.student_id"),
        nullable=False
    )

    ecourse_id = db.Column(
        db.Integer,
        db.ForeignKey("course.course_id"),
        nullable=False
    )


COURSE_MAP = {
    "course_1": 1,
    "course_2": 2,
    "course_3": 3,
    "course_4": 4,
}


@app.route("/")
def index():
    students = Student.query.order_by(Student.student_id).all()
    return render_template("index.html", students=students)


@app.route("/student/create", methods=["GET"])
def create_student():
    return render_template("create.html")


@app.route("/student/create", methods=["POST"])
def create_student_post():

    roll = request.form.get("roll")
    fname = request.form.get("f_name")
    lname = request.form.get("l_name")
    courses = request.form.getlist("courses")

    existing = Student.query.filter_by(roll_number=roll).first()

    if existing:
        return render_template(
            "error.html",
            message="Student already exists. Please use different Roll Number!"
        )

    student = Student(
        roll_number=roll,
        first_name=fname,
        last_name=lname
    )

    db.session.add(student)
    db.session.commit()

    for course in courses:
        cid = COURSE_MAP[course]
        db.session.add(
            Enrollment(
                estudent_id=student.student_id,
                ecourse_id=(cid)
            )
        )

    db.session.commit()

    return redirect("/")


@app.route("/student/<int:student_id>")
def student_details(student_id):

    student = Student.query.get_or_404(student_id)

    enrollments = Enrollment.query.filter_by(
        estudent_id=student_id
    ).all()

    courses = []

    for enrollment in enrollments:
        course = Course.query.get(enrollment.ecourse_id)
        courses.append(course)

    return render_template(
        "student.html",
        student=student,
        courses=courses
    )


@app.route("/student/<int:student_id>/update", methods=["GET"])
def update_student(student_id):

    student = Student.query.get_or_404(student_id)

    enrollments = Enrollment.query.filter_by(
        estudent_id=student_id
    ).all()

    selected = []

    for enrollment in enrollments:
        selected.append(enrollment.ecourse_id)

    return render_template(
        "update.html",
        student=student,
        selected=selected
    )


@app.route("/student/<int:student_id>/update", methods=["POST"])
def update_student_post(student_id):

    student = Student.query.get_or_404(student_id)

    student.first_name = request.form.get("f_name")
    student.last_name = request.form.get("l_name")

    Enrollment.query.filter_by(
        estudent_id=student_id
    ).delete()

    for course in request.form.getlist("courses"):
        db.session.add(
        Enrollment(
            estudent_id=student_id,
            ecourse_id=COURSE_MAP[course]
            )
        )

    db.session.commit()

    return redirect("/")


@app.route("/student/<int:student_id>/delete")
def delete_student(student_id):

    Enrollment.query.filter_by(
        estudent_id=student_id
    ).delete()

    db.session.commit()

    student = Student.query.get_or_404(student_id)
    db.session.delete(student)
    db.session.commit()

    return redirect("/")


if __name__ == "__main__":
    app.run()


