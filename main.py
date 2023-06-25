from bson import ObjectId
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError
from flask import Flask, request, jsonify, redirect, Response
import json
import uuid
import time

# Connect to our local MongoDB
client = MongoClient('mongodb://localhost:27017/')
# Choose database
db = client['InfoSys']
# Choose collections
users = db['Users']
products = db['Flights']

# Initiate Flask App
app = Flask(__name__)

def has_required_fields(field_names, data):
    # Σε αυτήν την συνάρτηση βάζουμε σε list τα ονόματα των fields που πρέπει να περιέχει το json που θα δώσει ο χρήστης.
    # Αν δεν υπάρχει κάποιο από αυτά, επιστρέφεται False
    for field in field_names:
        if not field in data:
            return False
    return True

users_sessions = list()
def create_session(email, category):
    # Η συνάρτηση αυτή δημιουργεί και επιστρέφει ένα μοναδικό κωδικό uuid
    user_uuid = str(uuid.uuid1())
    users_sessions.append((user_uuid, email, time.time(), category))
    return user_uuid

def is_session_valid(user_uuid, category):
    # Η συνάρτηση αυτή ελέγχει αν το uuid είναι έγκυρο και αν ο χρήστης που του ανήκει, έχει πρόσβαση στο category
    # Είναι έτσι σχεδιασμένο που αν ο χρήστης είναι admin μπορεί να έχει προσβάση στα endpoint που είναι Simple ενώ το αντίθετο δεν ισχύει
    for session in users_sessions:
        if (session[0] == user_uuid) and (session[3]==category or session[3]=="Admin"):
            return True
    return False

@app.route('/login', methods=['POST'])
def login():
    # Το endpoint αυτό χρησιμοποιείται για να συνδεθεί ο χρήστης
    try:
        data = json.loads(request.data)
    except Exception:
        return Response("This request needs JSON data", status=500, mimetype='application/json')
    if not has_required_fields(("email", "password"), data):
        return Response("There is missing at least one field in your request", status=500, mimetype="application/json")

    # Έλεγχος αν υπάρχει κάποιος χρήστης με αυτό το email και τον κωδικό
    user = users.find_one({ "$and": [{"email":data['email']},{"password":data['password']}]})
    if user is None:
        # Η αυθεντικοποίηση είναι ανεπιτυχής. Μήνυμα λάθους (Λάθος email ή password)
        return Response("Wrong email or password.", mimetype='application/json', status=400)
    else:
        # Επιτυχής ταυτοποίηση. Επιστροφή uuid
        res = {"uuid": create_session(user['email'],user['category']), "username":user['name']}
        return Response(json.dumps(res), mimetype='application/json', status=200)

@app.route('/api/v1/users', methods=['GET'])
def get_users():
    # Εδώ θα πρέπει να πάρουμε όλους τους χρήστες
    # Αν δεν υπάρχουν, επιστρέφουμε κατάλληλο μήνυμα
    # Αν υπάρχουν, τους επιστρέφουμε σε μορφή json
    users = list(users.find({}, {'_id': False}))
    if len(users) > 0:
        return Response(json.dumps(users),  mimetype='application/json')
    else:
        return Response(json.dumps({'error': 'No users found'}),  mimetype='application/json')
    
@app.route('/api/v1/users/<user_id>', methods=['GET'])
def get_user(user_id):
    # Εδώ θα πρέπει να πάρουμε το χρήστη με id user_id
    # Αν δεν υπάρχει, επιστρέφουμε κατάλληλο μήνυμα
    # Αν υπάρχει, τον επιστρέφουμε σε μορφή json
    user = users.find_one({'user_id': user_id}, {'_id': False})
    if user:
        return Response(json.dumps(user),  mimetype='application/json')
    else:
        return Response(json.dumps({'error': 'User not found'}),  mimetype='application/json')
    
@app.route('/api/v1/users', methods=['POST'])
def add_user():
    # Εδώ θα πρέπει να προσθέσουμε ένα νέο χρήστη
    # Αν υπάρχει ήδη, επιστρέφουμε κατάλληλο μήνυμα
    # Αν δεν υπάρχει, τον προσθέτουμε και επιστρέφουμε το νέο χρήστη σε μορφή json
    if not has_required_fields(['user_id', 'name', 'surname', 'email', 'password', 'birthdate', 'homecountry', 'passport_id'], request.json):
        return Response(json.dumps({'error': 'Missing required fields'}),  mimetype='application/json')
    user_id = request.json['user_id']
    user = users.find_one({'user_id': user_id}, {'_id': False})
    if user:
        return Response(json.dumps({'error': 'User already exists'}),  mimetype='application/json')
    else:
        users.insert_one(request.json)
        return Response(json.dumps(request.json),  mimetype='application/json')
    
@app.route('/api/v1/users/<user_id>', methods=['PUT'])
def update_user(user_id):
    # Εδώ θα πρέπει να ενημερώσουμε το χρήστη με id user_id
    # Αν δεν υπάρχει, επιστρέφουμε κατάλληλο μήνυμα
    # Αν υπάρχει, τον ενημερώνουμε και επιστρέφουμε τον ενημερωμένο χρήστη σε μορφή json
    user = users.find_one({'user_id': user_id}, {'_id': False})
    if user:
        users.update_one({'user_id': user_id}, {'$set': request.json})
        return Response(json.dumps(request.json),  mimetype='application/json')
    else:
        return Response(json.dumps({'error': 'User not found'}),  mimetype='application/json')
    
@app.route('/api/v1/users/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    # Εδώ θα πρέπει να διαγράψουμε το χρήστη με id user_id
    # Αν δεν υπάρχει, επιστρέφουμε κατάλληλο μήνυμα
    # Αν υπάρχει, τον διαγράφουμε και επιστρέφουμε τον διαγραμμένο χρήστη σε μορφή json
    user = users.find_one({'user_id': user_id}, {'_id': False})
    if user:
        users.delete_one({'user_id': user_id})
        return Response(json.dumps(user),  mimetype='application/json')
    else:
        return Response(json.dumps({'error': 'User not found'}),  mimetype='application/json')
    

@app.route('/api/v1/flights', methods=['GET'])
def get_flights():
    # Εδώ θα πρέπει να πάρουμε όλα τα διαθέσιμα δρομολόγια
    # Αν δεν υπάρχουν, επιστρέφουμε κατάλληλο μήνυμα
    # Αν υπάρχουν, τα επιστρέφουμε σε μορφή json
    flights = list(products.find({}, {'_id': False}))
    if len(flights) > 0:
        return Response(json.dumps(flights),  mimetype='application/json')
    else:
        return Response(json.dumps({'error': 'No flights found'}),  mimetype='application/json')
    
@app.route('/api/v1/flights/<flight_id>', methods=['GET'])
def get_flight(flight_id):
    # Εδώ θα πρέπει να πάρουμε το δρομολόγιο με flight_id flight_id
    # Αν δεν υπάρχει, επιστρέφουμε κατάλληλο μήνυμα
    # Αν υπάρχει, το επιστρέφουμε σε μορφή json
    flight = products.find_one({'flight_id': flight_id}, {'_id': False})
    if flight:
        return Response(json.dumps(flight),  mimetype='application/json')
    else:
        return Response(json.dumps({'error': 'Flight not found'}),  mimetype='application/json')
    
@app.route('/api/v1/flights', methods=['POST'])
def add_flight():
    # Εδώ θα πρέπει να προσθέσουμε ένα νέο δρομολόγιο
    # Αν υπάρχει ήδη, επιστρέφουμε κατάλληλο μήνυμα
    # Αν δεν υπάρχει, το προσθέτουμε και επιστρέφουμε το νέο δρομολόγιο σε μορφή json
    if not has_required_fields(['flight_id', 'from', 'to', 'date', 'time', 'price', 'seats'], request.json):
        return Response(json.dumps({'error': 'Missing required fields'}),  mimetype='application/json')
    flight_id = request.json['flight_id']
    flight = products.find_one({'flight_id': flight_id}, {'_id': False})
    if flight:
        return Response(json.dumps({'error': 'Flight already exists'}),  mimetype='application/json')
    else:
        products.insert_one(request.json)
        return Response(json.dumps(request.json),  mimetype='application/json')
    
@app.route('/api/v1/flights/<flight_id>', methods=['PUT'])
def update_flight(flight_id):
    # Εδώ θα πρέπει να ενημερώνουμε τα στοιχεία μιας πτήσης
    # Αν δεν υπάρχει, επιστρέφουμε κατάλληλο μήνυμα
    # Αν υπάρχει, το ενημερώνουμε και επιστρέφουμε το ενημερωμένο δρομολόγιο σε μορφή json
    if not has_required_fields(['flight_id', 'from', 'to', 'date', 'time', 'price', 'seats'], request.json):
        return Response(json.dumps({'error': 'Missing required fields'}),  mimetype='application/json')
    else:
        products.update(request.json)
        return Response(json.dumps(request.json),  mimetype='application/json')
    
@app.route('/api/v1/flights/<flight_id>', methods=['DELETE'])
def delete_flight(flight_id):
    # Εδώ θα πρέπει να διαγράφουμε ένα δρομολόγιο
    # Αν δεν υπάρχει, επιστρέφουμε κατάλληλο μήνυμα
    # Αν υπάρχει, το διαγράφουμε και επιστρέφουμε το δρομολόγιο σε μορφή json
    flight = products.find_one({'flight_id': flight_id}, {'_id': False})
    if flight:
        products.delete_one({'flight_id': flight_id})
        return Response(json.dumps(flight),  mimetype='application/json')
    else:
        return Response(json.dumps({'error': 'Flight not found'}),  mimetype='application/json')
    
@app.route('/api/v1/flights/<flight_id>/seats', methods=['GET'])
def get_seats(flight_id):
    # Εδώ θα πρέπει να πάρουμε τις κρατήσεις για το δρομολόγιο με flight_id flight_id
    # Αν δεν υπάρχει, επιστρέφουμε κατάλληλο μήνυμα
    # Αν υπάρχει, τις επιστρέφουμε σε μορφή json
    seats = reservations.find({'flight_id': flight_id}, {'_id': False})
    if seats:
        return Response(json.dumps(seats),  mimetype='application/json')
    else:
        return Response(json.dumps({'error': 'Flight not found'}),  mimetype='application/json')
    
@app.route('/api/v1/flights/<flight_id>/seats', methods=['POST'])
def add_seat(flight_id):
    # Εδώ θα πρέπει να προσθέσουμε μια νέα κράτηση για το δρομολόγιο με flight_id flight_id
    # Αν δεν υπάρχει το δρομολόγιο, επιστρέφουμε κατάλληλο μήνυμα
    # Αν υπάρχει, προσθέτουμε την κράτηση και επιστρέφουμε την κράτηση σε μορφή json
    if not has_required_fields(['flight_id', 'seat'], request.json):
        return Response(json.dumps({'error': 'Missing required fields'}),  mimetype='application/json')
    flight = products.find_one({'flight_id': flight_id}, {'_id': False})
    if flight:
        reservations.insert_one(request.json)
        return Response(json.dumps(request.json),  mimetype='application/json')
    else:
        return Response(json.dumps({'error': 'Flight not found'}),  mimetype='application/json')
    
@app.route('/api/v1/flights/<flight_id>/seats/<seat>', methods=['DELETE'])
def delete_seat(flight_id, seat):
    # Εδώ θα πρέπει να διαγράψουμε μια κράτηση για το δρομολόγιο με flight_id flight_id
    # Αν δεν υπάρχει το δρομολόγιο, επιστρέφουμε κατάλληλο μήνυμα
    # Αν υπάρχει, διαγράφουμε την κράτηση και επιστρέφουμε την κράτηση σε μορφή json
    flight = products.find_one({'flight_id': flight_id}, {'_id': False})
    if flight:
        reservations.delete_one({'flight_id': flight_id, 'seat': seat})
        return Response(json.dumps({'flight_id': flight_id, 'seat': seat}),  mimetype='application/json')
    else:
        return Response(json.dumps({'error': 'Flight not found'}),  mimetype='application/json')
    
if __name__ == '__main__':
    app.run(debug=True, host='5000')
