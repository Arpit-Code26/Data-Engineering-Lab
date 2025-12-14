# --- app.py ---

from flask import Flask, jsonify, request, render_template
from pymongo import MongoClient
from dotenv import load_dotenv
import os
from datetime import datetime
import random
# Ensure schemas.py is in the same directory
from schemas import attraction_schema, pass_schema, MOCK_ATTRACTIONS_DEFAULT, MOCK_PASSES 

# --- Configuration & Setup ---
load_dotenv()
app = Flask(__name__)

# IMPORTANT: MONGO_URI is HARDCODED here to bypass the persistent reading error.
# If your MongoDB is running on a different port/address, change this line only.
MONGO_URI = "mongodb://localhost:27017/PadharoDB"


# 1. Database Connection
try:
    # Use the hardcoded URI for connection
    client = MongoClient(MONGO_URI) 
    
    # Gets the database specified in the URI (PadharoDB)
    # & defines collections
    db = client.get_database() 
    attractions_col = db.attractions
    passes_col = db.passes
    print("✅ MongoDB connected successfully (NORMAL LOAD).")
except Exception as e:
    print(f"❌ Failed to connect to MongoDB: {e}")
    client = None

# Helper function: Database Initialization
def initialize_database(MOCK_DATA):
    """Wipes existing data and inserts mock data for a clean start."""
    if client:
        # Clear collections
        attractions_col.delete_many({})
        passes_col.delete_many({})
        
        # Insert mock attractions
        attractions_col.insert_many([attraction_schema(attr) for attr in MOCK_DATA])
        print(f"   > Inserted {len(MOCK_DATA)} attraction records.")
        
        # Insert mock passes
        passes_col.insert_many([pass_schema(p) for p in MOCK_PASSES])
        print(f"   > Inserted {len(MOCK_PASSES)} pass records.")

# --- API Endpoints ---

@app.route('/')
def home():
    """Serves the main frontend page (index.html)."""
    return render_template('index.html') 

@app.route('/api/attractions', methods=['GET'])
def get_attractions():
    """Returns current attraction capacity data from MongoDB."""
    if client:
        attractions_list = list(attractions_col.find({}, {"_id": 0}))
        
        # Simulate slight changes to visitor numbers
        for attraction in attractions_list:
             # Add a small random change (-5 to +5)
             attraction['current_visitors'] += random.randint(-5, 5) 
             # Keep visitors within 0 and max_capacity
             attraction['current_visitors'] = max(0, min(attraction['max_capacity'], attraction['current_visitors']))
             
        return jsonify(attractions_list)
    return jsonify({"error": "Database error"}), 500

@app.route('/api/passes/recent', methods=['GET'])
def get_recent_passes():
    """Returns the 10 most recent pass records."""
    if client:
        recent_passes = list(passes_col.find({}, {"_id": 0}).sort("pass_id", -1).limit(10))
        return jsonify(recent_passes)
    return jsonify({"error": "Database error"}), 500

@app.route('/api/passes/generate', methods=['POST'])
def generate_new_pass():
    """Generates and inserts a new pass record."""
    if client:
        data = request.json
        
        # Determine the next unique pass ID
        last_pass = passes_col.find_one(sort=[("pass_id", -1)])
        # Start at 1005 if no passes exist
        new_pass_id = last_pass['pass_id'] + 1 if last_pass else 1005 

        new_pass = {
            "pass_id": new_pass_id,
            "attraction": data.get('attraction_name', 'Default'),
            "visitor": data.get('visitor_name', 'New Visitor'),
            "status": "Active",
            "time": datetime.now().strftime("%I:%M %p")
        }
        
       # Insert the pass and capture the result
        result = passes_col.insert_one(new_pass)
        
        # CRITICAL FIX: Add the MongoDB generated _id to the dictionary 
        # and convert the ObjectId object to a simple string before returning it.
        new_pass['_id'] = str(result.inserted_id)
        
        return jsonify({"success": True, "message": "Pass successfully generated and stored.", "pass": new_pass}), 201

    return jsonify({"error": "Database connection failed."}), 500

# --- Run the App ---
if __name__ == '__main__':
    if client:
        # Initialize the database with default load data
        initialize_database(MOCK_ATTRACTIONS_DEFAULT)
        
    app.run(debug=True, port=5000)