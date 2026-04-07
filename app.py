from flask import Flask, jsonify, request
from pymongo import MongoClient
from pymongo.read_preferences import ReadPreference
from pymongo.write_concern import WriteConcern

app = Flask(__name__)

MONGO_URI = "mongodb+srv://kaavyamaha12_db_user:SAcUacx8NCKKYCTi@cluster0.xnscszq.mongodb.net/?appName=Cluster0&retryWrites=true&w=majority"

client = MongoClient(MONGO_URI)
db = client["ev_db"]
base_collection = db["vehicles"]

def _collection(read_pref=None, write_concern=None):
    opts = {}
    if read_pref is not None:
        opts["read_preference"] = read_pref
    if write_concern is not None:
        opts["write_concern"] = write_concern
    if opts:
        return base_collection.with_options(**opts)
    return base_collection

@app.route("/insert-fast", methods=["POST"])
def insert_fast():
    data = request.get_json(force=True)
    col = _collection(write_concern=WriteConcern(w=1))
    result = col.insert_one(data)
    return jsonify({"inserted_id": str(result.inserted_id)}), 201

@app.route("/insert-safe", methods=["POST"])
def insert_safe():
	data = request.get_json(force=True)
	col = _collection(write_concern=WriteConcern(w="majority"))
	result = col.insert_one(data)
	return jsonify({"inserted_id": str(result.inserted_id)}), 201

@app.route("/count-tesla-primary", methods=["GET"])
def count_tesla_primary():
	col = _collection(read_pref=ReadPreference.PRIMARY)
	count = col.count_documents({"Make": "TESLA"})
	return jsonify({"count": count}), 200

@app.route("/count-bmw-secondary", methods=["GET"])
def count_bmw_secondary():
    col = _collection(read_pref=ReadPreference.SECONDARY_PREFERRED)
    count = col.count_documents({"Make": "BMW"})
    return jsonify({"count": count}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)