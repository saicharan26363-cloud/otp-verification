from flask import Flask, request, jsonify

app = Flask(__name__)

# Dummy data for cabs and rides
cabs = [
    {"id": 1, "driver": "Ram", "location": "Jubilee Hills", "available": True},
    {"id": 2, "driver": "Ravi", "location": "Banjara Hills", "available": True},
    {"id": 3, "driver": "Sai", "location": "Madhapur", "available": True}
]

rides = []

@app.route('/cabs', methods=['GET'])
def get_cabs():
    available_cabs = [cab for cab in cabs if cab["available"]]
    return jsonify(available_cabs)

@app.route('/book', methods=['POST'])
def book_cab():
    data = request.get_json()
    cab_id = data.get("cab_id")
    user_name = data.get("user_name")
    destination = data.get("destination")

    for cab in cabs:
        if cab["id"] == cab_id and cab["available"]:
            cab["available"] = False
            ride = {
                "ride_id": len(rides) + 1,
                "cab_id": cab_id,
                "user_name": user_name,
                "driver": cab["driver"],
                "pickup": cab["location"],
                "destination": destination,
                "status": "ongoing"
            }
            rides.append(ride)
            return jsonify(ride)
    return jsonify({"error": "Cab not available"}), 400

@app.route('/rides/<user_name>', methods=['GET'])
def get_user_rides(user_name):
    user_rides = [ride for ride in rides if ride["user_name"] == user_name]
    return jsonify(user_rides)

@app.route('/complete/<int:ride_id>', methods=['POST'])
def complete_ride(ride_id):
    for ride in rides:
        if ride["ride_id"] == ride_id:
            ride["status"] = "completed"
            # Mark cab as available again
            for cab in cabs:
                if cab["id"] == ride["cab_id"]:
                    cab["available"] = True
            return jsonify({"message": "Ride completed!"})
    return jsonify({"error": "Ride not found"}), 404

if __name__ == '__main__':
    app.run(debug=True)
