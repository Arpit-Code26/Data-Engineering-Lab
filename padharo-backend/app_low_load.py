# --- app_critical_load.py ---
# This file is for running the Critical Load Scenario.

from flask import Flask, jsonify, request, render_template
from pymongo import MongoClient
from dotenv import load_dotenv
import os
from datetime import datetime
import random
# IMPORTANT: This imports the CRITICAL LOAD data
from schemas import attraction_schema, pass_schema, MOCK_ATTRACTIONS_CRITICAL, MOCK_PASSES

# --- Configuration & Setup ---
load_dotenv()
app = Flask(__name__)

# FIX: Hardcode MONGO_URI with the database name to bypass the "No default database defined" error.
MONGO_URI = "mongodb://localhost:27017/PadharoDB" 

# 1. Database Connection
try:
    client = MongoClient(MONGO_URI) 
    db = client.get_database() 
    attractions_col = db.attractions
    passes_col = db.passes
    # NOTE: The print message is changed to confirm the scenario is running
    print("✅ MongoDB connected successfully (CRITICAL LOAD).") 
except Exception as e:
    print(f"❌ Failed to connect to MongoDB: {e}")
    client = None

# Helper function: Database Initialization
def initialize_database(MOCK_DATA):
    """Wipes existing data and inserts mock data for a clean start."""
    if client:
        attractions_col.delete_many({})
        passes_col.delete_many({})
        
        # Use the critical data for insertion
        attractions_col.insert_many([attraction_schema(attr) for attr in MOCK_DATA]) 
        print(f"   > Inserted {len(MOCK_DATA)} attraction records.")
        
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
        for attraction in attractions_list:
             # Simulate slight changes to visitor numbers
             attraction['current_visitors'] += random.randint(-5, 5) 
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
        last_pass = passes_col.find_one(sort=[("pass_id", -1)])
        new_pass_id = last_pass['pass_id'] + 1 if last_pass else 1005 

        new_pass = {
            "pass_id": new_pass_id,
            "attraction": data.get('attraction_name', 'Default'),
            "visitor": data.get('visitor_name', 'New Visitor'),
            "status": "Active",
            "time": datetime.now().strftime("%I:%M %p")
        }
        
        result = passes_col.insert_one(new_pass)
        # FIX: JSON serialization
        new_pass['_id'] = str(result.inserted_id) 
        
        return jsonify({"success": True, "message": "Pass successfully generated and stored.", "pass": new_pass}), 201

    return jsonify({"error": "Database connection failed."}), 500

# --- Run the App ---
if __name__ == '__main__':
    if client:
        # Initialize the database with critical load data
        initialize_database(MOCK_ATTRACTIONS_CRITICAL)
        
    app.run(debug=True, port=5000)