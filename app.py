"""
Dashboard Application for AI Agent System
This module provides a web-based dashboard for monitoring all activities.
"""

import os
import json
import logging
from datetime import datetime, timedelta
from flask import Flask, render_template, jsonify, request, redirect, url_for, session
from pymongo import MongoClient
from functools import wraps

# Set up logging
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__, template_folder='templates', static_folder='static')
app.secret_key = os.environ.get('SECRET_KEY', 'dev_secret_key')

# Connect to MongoDB
mongo_uri = os.environ.get('MONGODB_URI', 'mongodb://localhost:27017/')
mongo_client = MongoClient(mongo_uri)
db = mongo_client.ai_agent

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'logged_in' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        # Simple authentication (in production, use proper auth)
        if username == 'admin' and password == 'changeme':
            session['logged_in'] = True
            session['username'] = username
            return redirect(url_for('dashboard'))
        else:
            return render_template('login.html', error='Invalid credentials')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/')
@login_required
def dashboard():
    return render_template('dashboard.html')

@app.route('/api/stats')
@login_required
def get_stats():
    # Get counts from collections
    leads_count = db.leads.count_documents({})
    qualified_leads_count = db.leads.count_documents({"status": "qualified"})
    deals_count = db.deals.count_documents({})
    closed_won_count = db.deals.count_documents({"status": "closed_won"})
    projects_count = db.projects.count_documents({})
    completed_projects_count = db.projects.count_documents({"status": "completed"})
    
    # Calculate conversion rates
    lead_qualification_rate = (qualified_leads_count / leads_count) * 100 if leads_count > 0 else 0
    deal_close_rate = (closed_won_count / deals_count) * 100 if deals_count > 0 else 0
    
    return jsonify({
        "leads": {
            "total": leads_count,
            "qualified": qualified_leads_count,
            "qualification_rate": round(lead_qualification_rate, 2)
        },
        "deals": {
            "total": deals_count,
            "closed_won": closed_won_count,
            "close_rate": round(deal_close_rate, 2)
        },
        "projects": {
            "total": projects_count,
            "completed": completed_projects_count
        }
    })

@app.route('/api/leads')
@login_required
def get_leads():
    leads = list(db.leads.find({}, {
        "business_name": 1,
        "source": 1,
        "status": 1,
        "score": 1,
        "discovery_date": 1,
        "identified_needs": 1
    }).sort("discovery_date", -1).limit(50))
    
    # Convert ObjectId to string for JSON serialization
    for lead in leads:
        lead["_id"] = str(lead["_id"])
        lead["discovery_date"] = lead["discovery_date"].isoformat() if "discovery_date" in lead else None
    
    return jsonify(leads)

@app.route('/api/deals')
@login_required
def get_deals():
    deals = list(db.deals.find({}, {
        "business_name": 1,
        "status": 1,
        "stage": 1,
        "creation_date": 1,
        "close_date": 1,
        "proposal": 1
    }).sort("creation_date", -1).limit(50))
    
    # Convert ObjectId to string for JSON serialization
    for deal in deals:
        deal["_id"] = str(deal["_id"])
        deal["creation_date"] = deal["creation_date"].isoformat() if "creation_date" in deal else None
        deal["close_date"] = deal["close_date"].isoformat() if "close_date" in deal else None
        
        # Extract price from proposal if exists
        if "proposal" in deal and "price" in deal["proposal"]:
            deal["price"] = deal["proposal"]["price"]
        else:
            deal["price"] = None
    
    return jsonify(deals)

@app.route('/api/projects')
@login_required
def get_projects():
    projects = list(db.projects.find({}, {
        "business_name": 1,
        "status": 1,
        "progress": 1,
        "creation_date": 1,
        "completion_date": 1,
        "services": 1
    }).sort("creation_date", -1).limit(50))
    
    # Convert ObjectId to string for JSON serialization
    for project in projects:
        project["_id"] = str(project["_id"])
        project["creation_date"] = project["creation_date"].isoformat() if "creation_date" in project else None
        project["completion_date"] = project["completion_date"].isoformat() if "completion_date" in project else None
        
        # Extract service names
        if "services" in project:
            project["service_names"] = [service.get("name", "Unknown Service") for service in project["services"]]
        else:
            project["service_names"] = []
    
    return jsonify(projects)

@app.route('/api/project/<project_id>')
@login_required
def get_project_details(project_id):
    from bson.objectid import ObjectId
    
    project = db.projects.find_one({"_id": ObjectId(project_id)})
    
    if not project:
        return jsonify({"error": "Project not found"}), 404
    
    # Convert ObjectId to string for JSON serialization
    project["_id"] = str(project["_id"])
    
    # Convert datetime objects to ISO format
    for key in project:
        if isinstance(project[key], datetime):
            project[key] = project[key].isoformat()
    
    return jsonify(project)

@app.route('/api/communications/<deal_id>')
@login_required
def get_communications(deal_id):
    from bson.objectid import ObjectId
    
    deal = db.deals.find_one({"_id": ObjectId(deal_id)})
    
    if not deal or "communications" not in deal:
        return jsonify([])
    
    communications = deal["communications"]
    
    # Convert datetime objects to ISO format
    for comm in communications:
        if "timestamp" in comm and isinstance(comm["timestamp"], datetime):
            comm["timestamp"] = comm["timestamp"].isoformat()
    
    return jsonify(communications)

@app.route('/review')
@login_required
def review_page():
    return render_template('review.html')

@app.route('/api/pending_reviews')
@login_required
def get_pending_reviews():
    # Get tasks that need review
    projects = list(db.projects.find(
        {"tasks.status": "needs_review"},
        {"business_name": 1, "tasks.$": 1}
    ))
    
    pending_reviews = []
    
    for project in projects:
        for task in project.get("tasks", []):
            if task.get("status") == "needs_review":
                pending_reviews.append({
                    "project_id": str(project["_id"]),
                    "business_name": project["business_name"],
                    "task_name": task.get("name"),
                    "task_id": str(task.get("_id", ""))
                })
    
    return jsonify(pending_reviews)

@app.route('/api/review/approve', methods=['POST'])
@login_required
def approve_review():
    data = request.json
    project_id = data.get('project_id')
    task_id = data.get('task_id')
    
    from bson.objectid import ObjectId
    
    # Update task status
    result = db.projects.update_one(
        {"_id": ObjectId(project_id), "tasks._id": ObjectId(task_id)},
        {"$set": {"tasks.$.status": "completed", "tasks.$.review_date": datetime.now()}}
    )
    
    if result.modified_count > 0:
        return jsonify({"success": True})
    else:
        return jsonify({"success": False, "error": "Task not found or not updated"}), 404

@app.route('/api/review/reject', methods=['POST'])
@login_required
def reject_review():
    data = request.json
    project_id = data.get('project_id')
    task_id = data.get('task_id')
    feedback = data.get('feedback', '')
    
    from bson.objectid import ObjectId
    
    # Update task status
    result = db.projects.update_one(
        {"_id": ObjectId(project_id), "tasks._id": ObjectId(task_id)},
        {
            "$set": {
                "tasks.$.status": "revision_needed",
                "tasks.$.review_date": datetime.now(),
                "tasks.$.feedback": feedback
            }
        }
    )
    
    if result.modified_count > 0:
        return jsonify({"success": True})
    else:
        return jsonify({"success": False, "error": "Task not found or not updated"}), 404

@app.route('/health')
def health_check():
    # Check MongoDB connection
    try:
        mongo_client.admin.command('ping')
        db_status = "connected"
    except Exception as e:
        db_status = f"error: {str(e)}"
    
    # Check module statuses (in a real implementation, this would check actual module status)
    modules_status = {
        "client_discovery": "running",
        "deal_closing": "running",
        "service_delivery": "running"
    }
    
    # Get system metrics
    metrics = {
        "leads_count": db.leads.count_documents({}),
        "deals_count": db.deals.count_documents({}),
        "projects_count": db.projects.count_documents({}),
        "uptime": "12 hours, 34 minutes"  # In a real implementation, this would be actual uptime
    }
    
    health_data = {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "database": db_status,
        "modules": modules_status,
        "metrics": metrics
    }
    
    return jsonify(health_data)

def start_dashboard(modules, port=8080):
    """Start the dashboard application."""
    logger.info(f"Starting dashboard on port {port}")
    app.run(host='0.0.0.0', port=port)

if __name__ == "__main__":
    start_dashboard([], port=int(os.environ.get('PORT', 8080)))
