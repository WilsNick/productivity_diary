from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from datetime import datetime


app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://nick:nick@localhost:5432/diary'
db = SQLAlchemy(app)

class Exercise(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), unique=True ,nullable=False)
    best_rep = db.Column(db.Integer, default=0)
    last_rep = db.Column(db.Integer, default=0)
    last_rest = db.Column(db.Integer, default=0)
    sets = db.relationship('Set', backref='exercise', lazy=True)

class TimeSubmissionWorkout(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    submission_date = db.Column(db.DateTime, default=datetime.utcnow)
    sets = db.relationship('Set', backref='workout', lazy=True)

class Set(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    reps = db.Column(db.Integer, nullable=False)
    rest = db.Column(db.Integer, nullable=False)
    exercise_id = db.Column(db.Integer, db.ForeignKey('exercise.id'), nullable=False)
    workout_id = db.Column(db.Integer, db.ForeignKey('time_submission_workout.id'), nullable=False)


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
        elif category == "Workouts":
            existing_project = Exercise.query.filter_by(title=project_title).first()

            if existing_project not in [None or "" or " "]:
                new_project = Exercise(title=project_title)
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
        elif category == "Workouts":
            exercises = Exercise.query.all()
            project_list = [{'id': exercise.id, 'title': exercise.title} for exercise in exercises]

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
        elif category == "Workouts":
            # Delete all books in the table
            Set.query.delete()
            TimeSubmissionWorkout.query.delete()
            Exercise.query.delete()

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


        if category == "Projects":
            description = data.get('description')
            project_name = data.get('project_name')
            time_spent = data.get('time_spent')

            # Create a new TimeSubmission object and add it to the database
            new_time_submission = TimeSubmissionProject(project_name=project_name, time_spent=time_spent, description=description)
        elif category == "Thesis":
            description = data.get('description')
            project_name = data.get('project_name')
            time_spent = data.get('time_spent')

            # Create a new TimeSubmission object and add it to the database
            new_time_submission = TimeSubmissionThesis(project_name=project_name, time_spent=time_spent,
                                                        description=description)

        elif category == "Books":

            current_page = data.get('current_page')
            project_name = data.get('project_name')
            time_spent = data.get('time_spent')
            new_time_submission = TimeSubmissionBook(book_name = project_name, time_spent=time_spent, current_page=current_page)
        elif category == "Workouts":
            exercises = data.get('exercises')
            with db.session.no_autoflush:

                new_time_submission = TimeSubmissionWorkout()
                db.session.add(new_time_submission)

                for exercise_data in exercises:
                    exercise_name = exercise_data.get('selectedExistingExercise')
                    exercise = Exercise.query.filter_by(title=exercise_name).first()

                    if exercise:
                        for set_data in exercise_data.get('sets', []):
                            new_set = Set(reps=set_data.get('reps'), rest=set_data.get('rest'), exercise=exercise,
                                          workout=new_time_submission)
                            db.session.add(new_set)

                            exercise.best_rep = max(exercise.best_rep, int(set_data.get('reps')))
                            exercise.last_rep = set_data.get('reps')
                            exercise.last_rest = set_data.get('rest')


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
        elif category == "Workouts":

            # Query all records from TimeSubmissionWorkout table
            workouts = TimeSubmissionWorkout.query.order_by(TimeSubmissionWorkout.submission_date.desc()).all()

            submission_list = []
            for workout in workouts:
                workout_data = {
                    'submission_date': workout.submission_date,
                    'exercises': [],
                }

                # Fetch only the sets associated with the current workout
                for set in workout.sets:
                    exercise_data = {
                        'exercise_name': set.exercise.title,
                        'sets': [
                            {'reps': s.reps, 'rest': s.rest}
                            for s in workout.sets  # Only include sets from the current workout
                        ],
                    }
                    workout_data['exercises'].append(exercise_data)

                submission_list.append(workout_data)



        return jsonify({'submissions': submission_list})

    except Exception as e:
        print("Error:", str(e))
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
