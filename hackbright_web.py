"""A web application for tracking projects, students, and student grades."""

from flask import Flask, request, render_template, make_response

import hackbright

app = Flask(__name__)

"""
Need to use python 3.6 or later.
"""
@app.route("/")
def index():
	"""List all students and projects"""

	students = hackbright.get_all_students()

	return render_template('index.html', students=students)

@app.route("/student", methods =["GET"])
def get_student():
	"""Show information about a student."""

	github = request.args.get('github')

	first, last, github = hackbright.get_student_by_github(github)

	grade_tuples = hackbright.get_grades_by_github(github)

	html = render_template('student_info.html',
							first=first,
							last=last,
							github=github,
							grade_tuples=grade_tuples)
	
	return html

@app.route("/student_search")
def get_student_form():
	"""Show form for searching for a student."""

	return render_template("student_search.html")


@app.route("/student_add")
def show_add_student_form():
	"""Show form to add a student"""

	return render_template("student_add.html")

@app.route("/show_student_added", methods=["POST"])
def add_student():
	"""Add student to the database and returns a confirmation 
	including a link to the student's profile. """

	first = request.form.get("first")
	last = request.form.get("last")
	github = request.form.get("github")

	hackbright.make_new_student(first, last, github)

	return render_template("student_added.html", first=first, last=last, github=github)

@app.route("/project", methods=["GET"])
def show_projects():
	""" Display list of all projects"""
	title = request.args.get('title')
	title, description, max_grade = hackbright.get_project_by_title(title)

	grade_tuples = hackbright.get_grades_by_title(title)

	return render_template("project.html", title=title, description=description, max_grade=max_grade, grade_tuples=grade_tuples)

if __name__ == "__main__":
	hackbright.connect_to_db(app)
	app.run(debug=True)
