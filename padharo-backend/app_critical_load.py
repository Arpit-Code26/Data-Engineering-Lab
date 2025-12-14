# --- app_critical_load.py ---
# This file is for running the Critical Load Scenario.

from flask import Flask, jsonify, request, render_template
from pymongo import MongoClient
from dotenv import load_dotenv
import os
from datetime import datetime
import random
# Import schemas to maintain data integrity
from schemas import attraction_schema, pass_schema, MOCK_PASSES

# --- Mock Data for Critical Load Scenario ---
CRITICAL_ATTRACTIONS = [
    {'id': 1, 'name': 'City Palace (Jaipur)', 'current': 2950, 'max': 3000, 'district': 'Jaipur'}, # 98%
    {'id': 2, 'name': 'Hawa Mahal', 'current': 3400, 'max': 3500, 'district': 'Jaipur'},        # 97% - CRITICAL
    {'id': 3, 'name': 'Jantar Mantar', 'current': 2500, 'max': 2900, 'district': 'Jaipur'},      # 86% - BUSY
    {'id': 4, 'name': 'Lake Palace (Udaipur)', 'current': 3100, 'max': 3200, 'district': 'Udaipur'}, # 97% - CRITICAL
    {'id': 5, 'name': 'Mehrangarh Fort', 'current': 2000, 'max': 2500, 'district': 'Jodhpur'},    # 80% - BUSY
]

# --- Configuration & Setup ---
load_dotenv()
app = Flask(__name__)

# CORRECT FIX: Define the full URI including the database name
MONGO_URI = "mongodb://localhost:27017/PadharoDB" 

# 1. Database Connection (Single, Correct Block)
try:
    # Connect to the MongoDB server using the full URI
    client = MongoClient(MONGO_URI)

    # Explicitly attempt to access the database to force connection check
    # We use the key notation here which is often cleaner for direct access
    db = client['PadharoDB'] 

    attractions_col = db.attractions
    passes_col = db.passes

    # ONLY print success if all previous lines executed without error
    print("✅ MongoDB connected successfully (CRITICAL LOAD).") 
except Exception as e:
    print(f"❌ Failed to connect to MongoDB: {e}")
    client = None # Set client to None on failure

# --- Helper Function: Database Initialization ---
def initialize_database():
    """Initializes with high-load mock data."""
    if client:
        attractions_col.delete_many({})
        passes_col.delete_many({})
        
        # Insert Critical Load attractions
        attractions_col.insert_many([attraction_schema(attr) for attr in CRITICAL_ATTRACTIONS])
        print(f"   > Inserted {len(CRITICAL_ATTRACTIONS)} high-load attraction records.")
        
        # Insert mock passes
        passes_col.insert_many([pass_schema(p) for p in MOCK_PASSES])
        print(f"   > Inserted {len(MOCK_PASSES)} pass records.")

# --- API Endpoints ---

@app.route('/')
def home():
    return render_template('index.html') 

@app.route('/api/attractions', methods=['GET'])
def get_attractions():
    if client:
        attractions_list = []
        for doc in attractions_col.find({}, {"_id": 0}):
            attractions_list.append(doc)
            
        # Simulate slight random fluctuation
        for attraction in attractions_list:
             # Keep this simple and within bounds
             attraction['current_visitors'] += random.randint(-10, 10) 
             attraction['current_visitors'] = max(0, min(attraction['max_capacity'], attraction['current_visitors']))
        
        return jsonify(attractions_list)
    return jsonify({"error": "Database error"}), 500

@app.route('/api/passes/recent', methods=['GET'])
def get_recent_passes():
    if client:
        recent_passes = list(passes_col.find({}, {"_id": 0}).sort("pass_id", -1).limit(10))
        return jsonify(recent_passes)
    return jsonify({"error": "Database error"}), 500

@app.route('/api/passes/generate', methods=['POST'])
def generate_new_pass():
    if client:
        data = request.json
        last_pass = passes_col.find_one(sort=[("pass_id", -1)])
        # Use 1005 as the starting ID, matching your previous successful attempt
        new_pass_id = last_pass['pass_id'] + 1 if last_pass else 1005 

        new_pass = {
            "pass_id": new_pass_id,
            "attraction": data.get('attraction_name', 'Default'),
            "visitor": data.get('visitor_name', 'New Visitor'),
            "status": "Active",
            "time": datetime.now().strftime("%I:%M %p")
        }
        
        result = passes_col.insert_one(new_pass)
        # CRITICAL FIX: Add the MongoDB generated _id to the dictionary 
        new_pass['_id'] = str(result.inserted_id)

        return jsonify({
            "success": True,
            "message": "Pass successfully generated and stored.",
            "pass": new_pass
        }), 201

    return jsonify({"error": "Database connection failed."}), 500

# --- Run the App ---
if __name__ == '__main__':
    if client:
        initialize_database()
        
    app.run(debug=True, port=5000)