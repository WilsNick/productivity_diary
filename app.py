from flask import Flask, request, jsonify, g
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

DATABASE = 'data.db'
categories = ["programming", "workout", "reading", "passion_project"]

# Function to get a database connection
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

# Create tables if not exists
with app.app_context():
    conn = get_db()
    cursor = conn.cursor()
    # Create tables for each category
    for category in categories:
        cursor.execute(f'''
            CREATE TABLE IF NOT EXISTS {category}_data (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name_field TEXT,
                text_field_value TEXT,
                time_spent INTEGER  -- New column for time spent
            )
        ''')
    conn.commit()
    #conn.close()



@app.route('/submit-form', methods=['POST'])
def submit_form():
    try:
        data = request.get_json()
        name_field = data.get('text')
        category = data.get('category')
        time_spent = data.get('timeSpent')

        # Use the get_db function to get a connection
        conn = get_db()
        cursor = conn.cursor()

        # Store data in the category-specific table
        cursor.execute(f'INSERT INTO {category}_data (name_field, time_spent) VALUES (?, ?)', (name_field, time_spent))
        conn.commit()

        return jsonify({'message': 'Form submitted successfully!'})

    except Exception as e:
        print("Error:", str(e))
        return jsonify({'error': str(e)}), 500



@app.route('/get-data', methods=['GET'])
def get_data():
    try:
        category = request.args.get('category')

        # Use the get_db function to get a connection
        conn = get_db()
        cursor = conn.cursor()

        if not category:
            data = []
            for current_category in categories:
                cursor.execute(f'SELECT id, name_field, time_spent FROM {current_category}_data')
                data_table = [{'id': row[0], 'name_field': row[1], 'time_spent': row[2], 'category': current_category} for row in cursor.fetchall()]
                data.extend(data_table)
        else:
            cursor.execute(f'SELECT id, name_field, time_spent FROM {category}_data')
            data = [{'id': row[0], 'name_field': row[1], 'time_spent': row[2], 'category': category} for row in cursor.fetchall()]

        conn.close()  # Close the connection after use

        return jsonify({'data': data})

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/get-existing-projects', methods=['GET'])
def get_existing_projects():
    try:
        conn = get_db()
        cursor = conn.cursor()

        # Fetch existing projects from the passion_project_names table
        cursor.execute('SELECT id, name_field FROM passion_project_data')
        existing_projects = [{'id': row[0], 'name': row[1]} for row in cursor.fetchall()]

        conn.close()
        return jsonify({'data': existing_projects})

    except Exception as e:
        return jsonify({'error': str(e)}), 500



@app.route('/remove-all-data', methods=['POST'])
def remove_all_data():
    try:
        # Use the get_db function to get a connection
        conn = get_db()
        cursor = conn.cursor()

        # Remove all data from each category-specific table
        # Drop existing tables and recreate them with the new schema
        for category in categories:
            cursor.execute(f'DROP TABLE IF EXISTS {category}_data')
            cursor.execute(f'''
                CREATE TABLE IF NOT EXISTS {category}_data (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name_field TEXT,
                    text_field_value TEXT,
                    time_spent INTEGER
                )
            ''')
            conn.commit()
        conn.close()

        return jsonify({'message': 'All data removed successfully!'})

    except Exception as e:
        print("Error:", str(e))
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
