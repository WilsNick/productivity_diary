from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from datetime import datetime


app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://nick:nick@localhost:5432/diary'
db = SQLAlchemy(app)

class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), unique=True, nullable=False)


class Thesis(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), unique=True, nullable=False)


class Books(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), unique=True, nullable=False)

class TimeSubmissionProject(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    project_name = db.Column(db.String(255), db.ForeignKey('project.title'), nullable=False)
    time_spent = db.Column(db.Float, nullable=False)
    description = db.Column(db.Text, nullable=False)
    submission_date = db.Column(db.DateTime, default=datetime.utcnow)

class TimeSubmissionBook(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    book_name = db.Column(db.String(255), db.ForeignKey('books.title'), nullable=False)
    time_spent = db.Column(db.Float, nullable=False)
    current_page = db.Column(db.Float, nullable=False)
    submission_date = db.Column(db.DateTime, default=datetime.utcnow)

class TimeSubmissionThesis(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    project_name = db.Column(db.String(255), db.ForeignKey('project.title'), nullable=False)
    time_spent = db.Column(db.Float, nullable=False)
    description = db.Column(db.Text, nullable=False)
    submission_date = db.Column(db.DateTime, default=datetime.utcnow)

with app.app_context():
    db.create_all()

@app.route('/add-project', methods=['POST'])
def add_project():
    try:
        data = request.get_json()
        project_title = data.get('title')
        category = data.get('category')
        if category == "Projects":
            existing_project = Project.query.filter_by(title=project_title).first()

            if existing_project not in [None or "" or " "]:
                new_project = Project(title=project_title)
                db.session.add(new_project)
                db.session.commit()
                return jsonify({'message': 'Project added successfully!'})
            else:
                return jsonify({'message': 'Project already exists!'})

        elif category == "Thesis":
            existing_project = Thesis.query.filter_by(title=project_title).first()

            if existing_project not in [None or "" or " "]:
                new_project = Thesis(title=project_title)
                db.session.add(new_project)
                db.session.commit()
                return jsonify({'message': 'Project added successfully!'})
            else:
                return jsonify({'message': 'Project already exists!'})
        elif category == "Books":

            existing_project = Books.query.filter_by(title=project_title).first()

            if existing_project not in  [None or "" or " "]:
                new_project = Books(title=project_title)
                db.session.add(new_project)
                db.session.commit()
                return jsonify({'message': 'Project added successfully!'})
            else:
                return jsonify({'message': 'Project already exists!'})

    except Exception as e:
        print("Error:", str(e))
        return jsonify({'error': str(e)}), 500

@app.route('/get-existing-projects', methods=['GET'])
def get_existing_projects():
    try:
        category = request.args.get('category')
        project_list =[]
        if category == "Projects":
            projects = Project.query.all()
            project_list = [{'id': project.id, 'title': project.title} for project in projects]
        elif category == "Thesis":
            projects = Thesis.query.all()
            project_list = [{'id': project.id, 'title': project.title} for project in projects]
        elif category == "Books":
            books = Books.query.all()
            project_list = [{'id': book.id, 'title': book.title} for book in books]
        return jsonify({'projects': project_list})

    except Exception as e:
        print("Error:", str(e))
        return jsonify({'error': str(e)}), 500

@app.route('/reset-table', methods=['GET'])
def reset_table():
    try:
        category = request.args.get('category')
        if category == "Projects":
            # Delete all projects in the table
            TimeSubmissionProject.query.delete()
            Project.query.delete()
        elif category == "Thesis":
            # Delete all projects in the table
            TimeSubmissionThesis.query.delete()
            Thesis.query.delete()
        elif category == "Books":
            # Delete all books in the table
            TimeSubmissionBook.query.delete()
            Books.query.delete()

        db.session.commit()

        return jsonify({'message': 'Table reset successful!'})

    except Exception as e:
        print("Error:", str(e))
        return jsonify({'error': str(e)}), 500

@app.route('/submit-time', methods=['POST'])
def submit_time():
    try:
        data = request.get_json()

        category = data.get('category')

        project_name = data.get('project_name')
        time_spent = data.get('time_spent')

        if category == "Projects":
            description = data.get('description')

            # Create a new TimeSubmission object and add it to the database
            new_time_submission = TimeSubmissionProject(project_name=project_name, time_spent=time_spent, description=description)
        elif category == "Thesis":
            description = data.get('description')

            # Create a new TimeSubmission object and add it to the database
            new_time_submission = TimeSubmissionThesis(project_name=project_name, time_spent=time_spent,
                                                        description=description)

        elif category == "Books":

            current_page = data.get('current_page')
            new_time_submission = TimeSubmissionBook(book_name = project_name, time_spent=time_spent, current_page=current_page)
        db.session.add(new_time_submission)
        db.session.commit()

        return jsonify({'message': 'Time submitted successfully!'})

    except Exception as e:
        print("Error:", str(e))
        return jsonify({'error': str(e)}), 500

# Add a new route to fetch all data from the TimeSubmission table
@app.route('/get-all-submissions', methods=['GET'])
def get_all_submissions():
    try:
        category = request.args.get('category')
        if category == "Projects":
            # Query all records from TimeSubmission table
            submissions = TimeSubmissionProject.query.all()

            # Create a list to store the data
            submission_list = []
            for submission in submissions:
                submission_data = {
                    'project_name': submission.project_name,
                    'time_spent': submission.time_spent,
                    'description': submission.description,
                    'submission_date': submission.submission_date,
                }
                submission_list.append(submission_data)
        elif category == "Thesis":
            # Query all records from TimeSubmission table
            submissions = TimeSubmissionThesis.query.all()

            # Create a list to store the data
            submission_list = []
            for submission in submissions:
                submission_data = {
                    'project_name': submission.project_name,
                    'time_spent': submission.time_spent,
                    'description': submission.description,
                    'submission_date': submission.submission_date,
                }
                submission_list.append(submission_data)
        elif category == "Books":
            # Query all records from TimeSubmission table
            submissions = TimeSubmissionBook.query.all()

            # Create a list to store the data
            submission_list = []
            for submission in submissions:
                submission_data = {
                    'project_name': submission.book_name,
                    'time_spent': submission.time_spent,
                    'submission_date': submission.submission_date,
                    'current_page': submission.current_page,
                }
                submission_list.append(submission_data)

        return jsonify({'submissions': submission_list})

    except Exception as e:
        print("Error:", str(e))
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
