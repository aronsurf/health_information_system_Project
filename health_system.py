# from flask import Flask, request, jsonify

# app = Flask(__name__)

# # In-memory "databases"
# clients = {}
# programs = set()

# # Model classes
# class Client:
#     def __init__(self, client_id, name, age, gender):
#         self.client_id = client_id
#         self.name = name
#         self.age = age
#         self.gender = gender
#         self.enrolled_programs = []

#     def to_dict(self):
#         return {
#             "client_id": self.client_id,
#             "name": self.name,
#             "age": self.age,
#             "gender": self.gender,
#             "programs": self.enrolled_programs
#         }

# # Route to create a health program
# @app.route('/programs', methods=['POST'])
# def create_program():
#     data = request.get_json()
#     program_name = data.get('program_name')
#     if not program_name:
#         return {"error": "Program name is required."}, 400
#     programs.add(program_name)
#     return {"message": f"Program '{program_name}' created successfully."}, 201

# # Route to register a new client
# @app.route('/clients', methods=['POST'])
# def register_client():
#     data = request.get_json()
#     client_id = data.get('client_id')
#     name = data.get('name')
#     age = data.get('age')
#     gender = data.get('gender')
    
#     if client_id in clients:
#         return {"error": "Client already exists."}, 400

#     client = Client(client_id, name, age, gender)
#     clients[client_id] = client
#     return {"message": f"Client '{name}' registered successfully."}, 201

# # Route to enroll client in health programs
# @app.route('/clients/<client_id>/enroll', methods=['POST'])
# def enroll_client(client_id):
#     data = request.get_json()
#     program_list = data.get('programs', [])

#     if client_id not in clients:
#         return {"error": "Client not found."}, 404

#     for program in program_list:
#         if program in programs:
#             if program not in clients[client_id].enrolled_programs:
#                 clients[client_id].enrolled_programs.append(program)

#     return {"message": f"Client '{client_id}' enrolled in programs."}, 200

# # Route to search for a client
# @app.route('/clients/search', methods=['GET'])
# def search_client():
#     query = request.args.get('q', '').lower()
#     results = [
#         client.to_dict() for client in clients.values()
#         if query in client.name.lower() or query in client.client_id.lower()
#     ]
#     return jsonify(results)

# # Route to view a client's profile
# @app.route('/clients/<client_id>', methods=['GET'])
# def view_profile(client_id):
#     client = clients.get(client_id)
#     if not client:
#         return {"error": "Client not found."}, 404
#     return jsonify(client.to_dict())

# # API endpoint to expose client profile
# @app.route('/api/clients/<client_id>', methods=['GET'])
# def api_get_client(client_id):
#     client = clients.get(client_id)
#     if not client:
#         return {"error": "Client not found."}, 404
#     return jsonify(client.to_dict())

# # Run the Flask app
# if __name__ == '__main__':
#     app.run(debug=True)
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Health Information System</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            padding: 20px;
        }
        h1 {
            color: #2c3e50;
        }
        form {
            margin: 10px 0;
        }
        input, button {
            padding: 10px;
            margin: 5px;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 10px;
        }
        th, td {
            padding: 8px;
            border: 1px solid #ccc;
            text-align: left;
        }
        th {
            background-color: #f2f2f2;
        }
    </style>
</head>
<body>
    <h1>Health Information System</h1>

    <h2>Register a New Client</h2>
    <form id="clientForm">
        <input type="text" id="client_id" placeholder="Client ID" required>
        <input type="text" id="name" placeholder="Name" required>
        <input type="number" id="age" placeholder="Age" required>
        <input type="text" id="gender" placeholder="Gender" required>
        <button type="submit">Register Client</button>
    </form>

    <h2>Create a Health Program</h2>
    <form id="programForm">
        <input type="text" id="program_name" placeholder="Program Name" required>
        <button type="submit">Create Program</button>
    </form>

    <h2>Enroll Client in a Program</h2>
    <form id="enrollForm">
        <input type="text" id="enroll_client_id" placeholder="Client ID" required>
        <input type="text" id="enroll_program_name" placeholder="Program Name" required>
        <button type="submit">Enroll</button>
    </form>

    <h2>View Client Profile</h2>
    <form id="viewProfileForm">
        <input type="text" id="view_client_id" placeholder="Client ID" required>
        <button type="submit">View Profile</button>
    </form>

    <h2>Client Profile Data</h2>
    <pre id="clientData"></pre>

    <h2>Search for a Client</h2>
    <form id="searchForm">
        <input type="text" id="search_query" placeholder="Enter name or client ID" required>
        <button type="submit">Search</button>
    </form>

    <h2>Search Results</h2>
    <div id="searchResults"></div>

    <script>
        const baseURL = 'http://127.0.0.1:5000'; // Base URL for backend

        // Reusable function to POST data
        async function postData(endpoint, data) {
            try {
                const response = await fetch(`${baseURL}${endpoint}`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(data)
                });
                const result = await response.json();
                alert(result.message);
            } catch (error) {
                alert('Error: ' + error.message);
            }
        }

        // Register Client
        document.getElementById('clientForm').addEventListener('submit', function(e) {
            e.preventDefault();
            const clientData = {
                client_id: document.getElementById('client_id').value,
                name: document.getElementById('name').value,
                age: document.getElementById('age').value,
                gender: document.getElementById('gender').value
            };
            postData('/clients', clientData);
            this.reset();
        });

        // Create Program
        document.getElementById('programForm').addEventListener('submit', function(e) {
            e.preventDefault();
            const programData = {
                program_name: document.getElementById('program_name').value
            };
            postData('/programs', programData);
            this.reset();
        });

        // Enroll Client (corrected)
        document.getElementById('enrollForm').addEventListener('submit', function(e) {
            e.preventDefault();
            const clientId = document.getElementById('enroll_client_id').value;
            const programName = document.getElementById('enroll_program_name').value;

            postData(`/clients/${clientId}/enroll`, { programs: [programName] });
            this.reset();
        });

        // View Client Profile
        document.getElementById('viewProfileForm').addEventListener('submit', function(e) {
            e.preventDefault();
            const clientId = document.getElementById('view_client_id').value;
            fetch(`${baseURL}/clients/${clientId}`)
                .then(response => response.json())
                .then(data => {
                    document.getElementById('clientData').textContent = JSON.stringify(data, null, 2);
                    document.getElementById('viewProfileForm').reset();
                })
                .catch(error => {
                    alert('Error fetching client profile: ' + error.message);
                });
        });

        // Search for Client
        document.getElementById('searchForm').addEventListener('submit', function(e) {
            e.preventDefault();
            const query = document.getElementById('search_query').value;
            fetch(`${baseURL}/clients/search?q=${encodeURIComponent(query)}`)
                .then(response => response.json())
                .then(data => {
                    displaySearchResults(data);
                    document.getElementById('searchForm').reset();
                })
                .catch(error => {
                    alert('Error searching client: ' + error.message);
                });
        });

        // Display Search Results
        function displaySearchResults(clients) {
            const searchResultsDiv = document.getElementById('searchResults');

            if (!Array.isArray(clients)) {
                clients = [clients];
            }

            if (clients.length === 0) {
                searchResultsDiv.innerHTML = "<p>No clients found.</p>";
                return;
            }

            let table = `<table>
                <thead>
                    <tr>
                        <th>Client ID</th>
                        <th>Name</th>
                        <th>Age</th>
                        <th>Gender</th>
                        <th>Programs</th>
                    </tr>
                </thead>
                <tbody>`;

            clients.forEach(client => {
                const programs = Array.isArray(client.programs) ? client.programs : [];
                const programsText = programs.length > 0 ? programs.join(", ") : "No programs enrolled";

                table += `
                    <tr>
                        <td>${client.client_id}</td>
                        <td>${client.name}</td>
                        <td>${client.age}</td>
                        <td>${client.gender}</td>
                        <td>${programsText}</td>
                    </tr>
                `;
            });

            table += `</tbody></table>`;
            searchResultsDiv.innerHTML = table;
        }
    </script>
</body>
</html>
