
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError

BASE_DIR = Path(__file__).resolve().parent

app = Flask(
    __name__,
    template_folder=str(BASE_DIR.parent / "templates"),
    static_folder=str(BASE_DIR.parent / "static")
)

app.config["SECRET_KEY"] = "prototype-secret-key"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.sqlite3"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


# -------------------- DATABASE MODELS --------------------

class Student(db.Model):
    __tablename__ = "student"

    student_id = db.Column(db.Integer, primary_key=True)
    roll_number = db.Column(db.String(30), unique=True, nullable=False)
    first_name = db.Column(db.String(80), nullable=False)
    last_name = db.Column(db.String(80))

    enrollments = db.relationship(
        "Enrollment",
        back_populates="student",
        cascade="all, delete-orphan"
    )

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name or ''}".strip()


class Course(db.Model):
    __tablename__ = "course"

    course_id = db.Column(db.Integer, primary_key=True)
    course_code = db.Column(db.String(20), unique=True, nullable=False)
    course_name = db.Column(db.String(100), nullable=False)
    course_description = db.Column(db.String(255))

    enrollments = db.relationship(
        "Enrollment",
        back_populates="course",
        cascade="all, delete-orphan"
    )


class Enrollment(db.Model):
    __tablename__ = "enrollments"

    enrollment_id = db.Column(db.Integer, primary_key=True)

    student_id = db.Column(
        db.Integer,
        db.ForeignKey("student.student_id"),
        nullable=False
    )

    course_id = db.Column(
        db.Integer,
        db.ForeignKey("course.course_id"),
        nullable=False
    )

    student = db.relationship("Student", back_populates="enrollments")
    course = db.relationship("Course", back_populates="enrollments")

    __table_args__ = (
        db.UniqueConstraint(
            "student_id",
            "course_id",
            name="unique_student_course"
        ),
    )


# -------------------- INITIALIZATION --------------------

def initialize_database():
    db.create_all()

    if Course.query.count() == 0:
        courses = [
            Course(
                course_code="CS101",
                course_name="Introduction to Programming",
                course_description="Programming fundamentals"
            ),
            Course(
                course_code="CS102",
                course_name="Data Structures",
                course_description="Lists, trees and algorithms"
            ),
            Course(
                course_code="MA101",
                course_name="Mathematics",
                course_description="Core mathematical concepts"
            ),
            Course(
                course_code="ST101",
                course_name="Statistics",
                course_description="Probability and statistical methods"
            )
        ]

        db.session.add_all(courses)
        db.session.commit()


# -------------------- HELPERS --------------------

def get_selected_courses():
    course_ids = request.form.getlist("courses")
    courses = []

    for course_id in course_ids:
        try:
            course_id = int(course_id)
        except ValueError:
            continue

        course = db.session.get(Course, course_id)

        if course and course not in courses:
            courses.append(course)

    return courses


def validate_student_form():
    roll = request.form.get("roll", "").strip()
    first_name = request.form.get("first_name", "").strip()
    last_name = request.form.get("last_name", "").strip()

    if not roll or not first_name:
        flash("Roll number and first name are required.", "error")
        return None

    return {
        "roll": roll,
        "first_name": first_name,
        "last_name": last_name
    }


# -------------------- DASHBOARD --------------------

@app.route("/")
def index():
    students = Student.query.order_by(Student.student_id).all()

    return render_template(
        "index.html",
        students=students,
        student_count=len(students),
        course_count=Course.query.count()
    )


# -------------------- CREATE STUDENT --------------------

@app.route("/student/create", methods=["GET", "POST"])
def create_student():
    courses = Course.query.order_by(Course.course_code).all()

    if request.method == "POST":
        data = validate_student_form()

        if data is None:
            return render_template("create.html", courses=courses)

        existing = Student.query.filter_by(
            roll_number=data["roll"]
        ).first()

        if existing:
            flash("That roll number already exists.", "error")
            return render_template("create.html", courses=courses)

        student = Student(
            roll_number=data["roll"],
            first_name=data["first_name"],
            last_name=data["last_name"]
        )

        student.enrollments = [
            Enrollment(course=course)
            for course in get_selected_courses()
        ]

        db.session.add(student)

        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            flash("Could not create student. Check the submitted data.", "error")
            return render_template("create.html", courses=courses)

        flash("Student added successfully.", "success")
        return redirect(url_for("index"))

    return render_template("create.html", courses=courses)


# -------------------- STUDENT DETAILS --------------------

@app.route("/student/<int:student_id>")
def student_details(student_id):
    student = db.get_or_404(Student, student_id)

    return render_template("student.html", student=student)


# -------------------- UPDATE STUDENT --------------------

@app.route("/student/<int:student_id>/update", methods=["GET", "POST"])
def update_student(student_id):
    student = db.get_or_404(Student, student_id)
    courses = Course.query.order_by(Course.course_code).all()

    if request.method == "POST":
        data = validate_student_form()

        if data is None:
            return render_template(
                "update.html",
                student=student,
                courses=courses
            )

        duplicate = Student.query.filter(
            Student.roll_number == data["roll"],
            Student.student_id != student_id
        ).first()

        if duplicate:
            flash("That roll number belongs to another student.", "error")
            return render_template(
                "update.html",
                student=student,
                courses=courses
            )

        student.roll_number = data["roll"]
        student.first_name = data["first_name"]
        student.last_name = data["last_name"]

        student.enrollments = [
            Enrollment(course=course)
            for course in get_selected_courses()
        ]

        db.session.commit()

        flash("Student details updated.", "success")
        return redirect(url_for("student_details", student_id=student_id))

    return render_template(
        "update.html",
        student=student,
        courses=courses
    )


# -------------------- DELETE STUDENT --------------------

@app.route("/student/<int:student_id>/delete", methods=["POST"])
def delete_student(student_id):
    student = db.get_or_404(Student, student_id)

    db.session.delete(student)
    db.session.commit()

    flash("Student deleted.", "success")
    return redirect(url_for("index"))


# -------------------- RUN APPLICATION --------------------

if __name__ == "__main__":
    with app.app_context():
        initialize_database()

    app.run(debug=True)
