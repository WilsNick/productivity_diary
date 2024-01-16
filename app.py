from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://nick:nick@localhost:5432/diary'
db = SQLAlchemy(app)

class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), unique=True, nullable=False)

with app.app_context():
    db.create_all()

@app.route('/add-project', methods=['POST'])
def add_project():
    try:
        data = request.get_json()
        project_title = data.get('title')

        existing_project = Project.query.filter_by(title=project_title).first()

        if existing_project not in  [None or "" or " "]:
            new_project = Project(title=project_title)
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
        projects = Project.query.all()
        project_list = [{'id': project.id, 'title': project.title} for project in projects]
        return jsonify({'projects': project_list})

    except Exception as e:
        print("Error:", str(e))
        return jsonify({'error': str(e)}), 500

@app.route('/reset-table', methods=['POST'])
def reset_table():
    try:
        # Delete all projects in the table
        Project.query.delete()
        db.session.commit()

        return jsonify({'message': 'Table reset successful!'})

    except Exception as e:
        print("Error:", str(e))
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
