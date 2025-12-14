# --- schemas.py ---

# This file defines the structure of the data we will store in MongoDB.

def attraction_schema(data):
    """Schema for a single attraction record (used for capacity data)."""
    return {
        "attraction_id": data.get("id"),
        "name": data.get("name"),
        "max_capacity": data.get("max"),
        "current_visitors": data.get("current"),
        "district": data.get("district")
    }

def pass_schema(data):
    """Schema for a digital pass record."""
    return {
        "pass_id": data.get("id"),
        "attraction": data.get("attraction"),
        "visitor": data.get("visitor"),
        "status": data.get("status"),
        "time": data.get("time")
    }

# --- Mock Initial Data (used by all app_*.py scripts) ---

MOCK_ATTRACTIONS_DEFAULT = [
    {'id': 1, 'name': 'City Palace (Jaipur)', 'current': 2340, 'max': 3000, 'district': 'Jaipur'},
    {'id': 2, 'name': 'Hawa Mahal', 'current': 3210, 'max': 3500, 'district': 'Jaipur'},
    {'id': 3, 'name': 'Jantar Mantar', 'current': 1890, 'max': 2900, 'district': 'Jaipur'},
    {'id': 4, 'name': 'Lake Palace (Udaipur)', 'current': 1450, 'max': 3200, 'district': 'Udaipur'},
    {'id': 5, 'name': 'Mehrangarh Fort', 'current': 980, 'max': 2500, 'district': 'Jodhpur'},
]

MOCK_ATTRACTIONS_CRITICAL = [
    {'id': 1, 'name': 'City Palace (Jaipur)', 'current': 2950, 'max': 3000, 'district': 'Jaipur'}, 
    {'id': 2, 'name': 'Hawa Mahal', 'current': 3400, 'max': 3500, 'district': 'Jaipur'},        
    {'id': 3, 'name': 'Jantar Mantar', 'current': 2500, 'max': 2900, 'district': 'Jaipur'},      
    {'id': 4, 'name': 'Lake Palace (Udaipur)', 'current': 3100, 'max': 3200, 'district': 'Udaipur'}, 
    {'id': 5, 'name': 'Mehrangarh Fort', 'current': 2000, 'max': 2500, 'district': 'Jodhpur'},    
]

MOCK_ATTRACTIONS_LOW = [
    {'id': 1, 'name': 'City Palace (Jaipur)', 'current': 1200, 'max': 3000, 'district': 'Jaipur'}, 
    {'id': 2, 'name': 'Hawa Mahal', 'current': 1500, 'max': 3500, 'district': 'Jaipur'},        
    {'id': 3, 'name': 'Jantar Mantar', 'current': 800, 'max': 2900, 'district': 'Jaipur'},      
    {'id': 4, 'name': 'Lake Palace (Udaipur)', 'current': 1000, 'max': 3200, 'district': 'Udaipur'}, 
    {'id': 5, 'name': 'Mehrangarh Fort', 'current': 500, 'max': 2500, 'district': 'Jodhpur'},    
]

MOCK_PASSES = [
    {'id': 1001, 'attraction': 'City Palace', 'visitor': 'Visitor #1001', 'status': 'Used', 'time': '10:30 AM'},
    {'id': 1002, 'attraction': 'Jantar Mantar', 'visitor': 'Visitor #1002', 'status': 'Upcoming', 'time': '09:00 AM'},
    {'id': 1003, 'attraction': 'Heritage Plus', 'visitor': 'Visitor #1003', 'status': 'Active', 'time': '7 days'},
    {'id': 1004, 'attraction': 'Lake Palace', 'visitor': 'Visitor #1004', 'status': 'Expired', 'time': 'Dec 8'}
]