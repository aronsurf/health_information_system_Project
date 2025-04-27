
from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
CORS(app)

# --- Initialize Database ---
def init_db():
    conn = sqlite3.connect('health.db')
    c = conn.cursor()
    # Clients Table
    c.execute('''
        CREATE TABLE IF NOT EXISTS clients (
            client_id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            age INTEGER NOT NULL,
            gender TEXT NOT NULL
        )
    ''')
    # Programs Table
    c.execute('''
        CREATE TABLE IF NOT EXISTS programs (
            program_id INTEGER PRIMARY KEY AUTOINCREMENT,
            program_name TEXT NOT NULL UNIQUE
        )
    ''')
    # Enrollments Table
    c.execute('''
        CREATE TABLE IF NOT EXISTS enrollments (
            enrollment_id INTEGER PRIMARY KEY AUTOINCREMENT,
            client_id TEXT,
            program_name TEXT,
            FOREIGN KEY (client_id) REFERENCES clients(client_id),
            FOREIGN KEY (program_name) REFERENCES programs(program_name)
        )
    ''')
    conn.commit()
    conn.close()

# Initialize DB if not already initialized
init_db()

# --- Routes ---

# 1. Register a new client
@app.route('/clients', methods=['POST'])
def register_client():
    data = request.get_json()
    client_id = data.get('client_id')
    name = data.get('name')
    age = data.get('age')
    gender = data.get('gender')

    conn = sqlite3.connect('health.db')
    c = conn.cursor()
    try:
        c.execute('INSERT INTO clients (client_id, name, age, gender) VALUES (?, ?, ?, ?)',
                  (client_id, name, age, gender))
        conn.commit()
    except sqlite3.IntegrityError:
        conn.close()
        return jsonify({"message": "Client ID already exists!"}), 400
    except Exception as e:
        conn.close()
        return jsonify({"message": f"Error: {str(e)}"}), 500
    finally:
        conn.close()

    return jsonify({"message": "Client registered successfully!"})

# 2. Create a new program
@app.route('/programs', methods=['POST'])
def create_program():
    data = request.get_json()
    program_name = data.get('program_name')

    conn = sqlite3.connect('health.db')
    c = conn.cursor()
    try:
        c.execute('INSERT INTO programs (program_name) VALUES (?)', (program_name,))
        conn.commit()
    except sqlite3.IntegrityError:
        conn.close()
        return jsonify({"message": "Program already exists!"}), 400
    except Exception as e:
        conn.close()
        return jsonify({"message": f"Error: {str(e)}"}), 500
    finally:
        conn.close()

    return jsonify({"message": "Program created successfully!"})

# 3. Enroll client into a program
@app.route('/enroll', methods=['POST'])
def enroll_client():
    data = request.get_json()
    client_id = data.get('client_id')
    program_name = data.get('program_name')

    conn = sqlite3.connect('health.db')
    c = conn.cursor()
    try:
        # Check if client exists
        c.execute('SELECT * FROM clients WHERE client_id = ?', (client_id,))
        client = c.fetchone()
        if not client:
            return jsonify({"message": "Client not found!"}), 404

        # Check if program exists
        c.execute('SELECT * FROM programs WHERE program_name = ?', (program_name,))
        program = c.fetchone()
        if not program:
            return jsonify({"message": "Program not found!"}), 404

        # Enroll client into the program
        c.execute('INSERT INTO enrollments (client_id, program_name) VALUES (?, ?)', (client_id, program_name))
        conn.commit()
    except Exception as e:
        conn.close()
        return jsonify({"message": f"Error: {str(e)}"}), 500
    finally:
        conn.close()

    return jsonify({"message": "Client enrolled successfully!"})

# 4. View a client profile
@app.route('/clients/<client_id>', methods=['GET'])
def get_client_profile(client_id):
    conn = sqlite3.connect('health.db')
    c = conn.cursor()
    try:
        c.execute('SELECT * FROM clients WHERE client_id = ?', (client_id,))
        client = c.fetchone()

        if not client:
            return jsonify({"message": "Client not found!"}), 404

        client_data = {
            "client_id": client[0],
            "name": client[1],
            "age": client[2],
            "gender": client[3]
        }

        c.execute('SELECT program_name FROM enrollments WHERE client_id = ?', (client_id,))
        programs = [row[0] for row in c.fetchall()]
        client_data['enrolled_programs'] = programs

    except Exception as e:
        return jsonify({"message": f"Error: {str(e)}"}), 500
    finally:
        conn.close()

    return jsonify(client_data)

# --- Start the App ---
if __name__ == '__main__':
    app.run(debug=True)
