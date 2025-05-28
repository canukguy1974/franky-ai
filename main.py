# Placeholder main.py to simulate AI Agent operation
import time
import random
import json
import logging
from threading import Thread
from flask import Flask, jsonify, render_template_string

# --- Mock Module Implementations ---

class MockClientDiscovery:
    def __init__(self):
        logging.info("Mock Client Discovery Module initialized")
        self.leads = []
        self.sources = []
        try:
            # Adjust path relative to where main.py will be run from (project root)
            with open("src/client_discovery/config/sources.json", "r") as f:
                self.sources = json.load(f)
        except Exception as e:
            logging.error(f"Error loading sources config: {e}")

    def discover_new_leads(self):
        logging.info("Starting mock lead discovery...")
        time.sleep(random.uniform(2, 5))
        num_new = random.randint(1, 5)
        for i in range(num_new):
            lead = {
                "lead_id": f"lead_{random.randint(1000, 9999)}",
                "status": "new",
                "source": random.choice(["gmb", "linkedin", "directory"]),
                "business_name": f"Demo Business {random.randint(100, 999)}"
            }
            self.leads.append(lead)
        logging.info(f"Discovered {num_new} new mock leads.")
        return num_new

    def enrich_lead_data(self):
        logging.info("Starting mock lead enrichment...")
        enriched_count = 0
        for lead in self.leads:
            if lead["status"] == "new":
                time.sleep(random.uniform(0.1, 0.5))
                lead["status"] = "enriched"
                lead["contact_person"] = f"Contact {random.randint(1, 10)}"
                enriched_count += 1
        if enriched_count > 0:
            logging.info(f"Enriched {enriched_count} mock leads.")
        return enriched_count

    def qualify_leads(self):
        logging.info("Starting mock lead qualification...")
        qualified_count = 0
        for lead in self.leads:
            if lead["status"] == "enriched":
                time.sleep(random.uniform(0.1, 0.3))
                lead["score"] = random.randint(40, 95)
                lead["status"] = "qualified"
                qualified_count += 1
        if qualified_count > 0:
            logging.info(f"Qualified {qualified_count} mock leads.")
        return qualified_count

    def get_qualified_leads_for_closing(self):
        return [l for l in self.leads if l["status"] == "qualified" and l.get("transferred") is None]

    def run_pipeline(self):
        self.discover_new_leads()
        self.enrich_lead_data()
        self.qualify_leads()
        qualified = self.get_qualified_leads_for_closing()
        if qualified:
            logging.info(f"{len(qualified)} leads ready for Deal Closing.")
        return qualified

class MockDealClosing:
    def __init__(self):
        logging.info("Mock Deal Closing Module initialized")
        self.deals = []
        self.templates = []
        try:
            # Adjust path relative to where main.py will be run from (project root)
            with open("src/deal_closing/config/email_templates.json", "r") as f:
                self.templates = json.load(f).get("templates", [])
        except Exception as e:
            logging.error(f"Error loading email templates: {e}")

    def receive_lead(self, lead):
        logging.info(f"Received lead {lead['lead_id']} ({lead['business_name']})")
        deal = {
            "deal_id": f"deal_{lead['lead_id']}",
            "lead_id": lead['lead_id'],
            "business_name": lead['business_name'],
            "status": "received",
            "steps": ["Received"]
        }
        self.deals.append(deal)
        lead["transferred"] = True # Mark lead as transferred in discovery module's list

    def process_deals(self):
        logging.info("Processing deals...")
        processed_count = 0
        for deal in self.deals:
            action_taken = False
            if deal["status"] == "received":
                time.sleep(random.uniform(1, 3))
                logging.info(f"Sending initial outreach for deal {deal['deal_id']}")
                deal["status"] = "outreach_sent"
                deal["steps"].append("Outreach Sent")
                action_taken = True
            elif deal["status"] == "outreach_sent" and random.random() < 0.3: # Simulate response
                time.sleep(random.uniform(1, 2))
                logging.info(f"Engaging in needs assessment for deal {deal['deal_id']}")
                deal["status"] = "engaged"
                deal["steps"].append("Needs Assessment")
                action_taken = True
            elif deal["status"] == "engaged" and random.random() < 0.6: # Simulate proposal
                time.sleep(random.uniform(2, 4))
                logging.info(f"Generating and sending proposal for deal {deal['deal_id']}")
                deal["status"] = "proposal_sent"
                deal["steps"].append("Proposal Sent")
                action_taken = True
            elif deal["status"] == "proposal_sent" and random.random() < 0.4: # Simulate negotiation
                 time.sleep(random.uniform(1, 3))
                 logging.info(f"Negotiating terms for deal {deal['deal_id']}")
                 deal["status"] = "negotiating"
                 deal["steps"].append("Negotiation")
                 action_taken = True
            elif deal["status"] == "negotiating" and random.random() < 0.7: # Simulate closing
                 time.sleep(random.uniform(1, 2))
                 logging.info(f"Closing deal {deal['deal_id']}")
                 deal["status"] = "closed_won"
                 deal["steps"].append("Closed Won")
                 action_taken = True
                 # Simulate handoff
                 project_details = {
                     "project_id": f"proj_{deal['deal_id']}",
                     "deal_id": deal['deal_id'],
                     "client_name": deal['business_name'],
                     "service": random.choice(["blog_post_writing", "social_media_content", "website_audit"])
                 }
                 # Ensure mock_service_delivery is accessible globally or passed in
                 mock_service_delivery.receive_project(project_details)
            if action_taken:
                processed_count += 1
        if processed_count == 0:
             logging.info("No deals progressed in this cycle.")

class MockServiceDelivery:
    def __init__(self):
        logging.info("Mock Service Delivery Module initialized")
        self.projects = []
        self.services = []
        try:
             # Adjust path relative to where main.py will be run from (project root)
             with open("src/service_delivery/config/service_definitions.json", "r") as f:
                self.services = json.load(f).get("services", [])
        except Exception as e:
            logging.error(f"Error loading service definitions: {e}")

    def receive_project(self, project_details):
        logging.info(f"Received project {project_details['project_id']} for {project_details['client_name']}")
        project = {
            **project_details,
            "status": "pending",
            "tasks": [],
            "progress": 0
        }
        self.projects.append(project)

    def process_projects(self):
        logging.info("Processing service delivery projects...")
        processed_count = 0
        for project in self.projects:
            action_taken = False
            if project["status"] == "pending":
                time.sleep(random.uniform(1, 2))
                logging.info(f"Planning tasks for project {project['project_id']}")
                project["status"] = "in_progress"
                project["tasks"] = [f"Task {i+1}" for i in range(random.randint(2, 5))]
                project["progress"] = 10
                action_taken = True
            elif project["status"] == "in_progress" and project["progress"] < 100:
                time.sleep(random.uniform(2, 5))
                increment = random.randint(15, 30)
                project["progress"] = min(100, project["progress"] + increment)
                logging.info(f"Executing tasks for project {project['project_id']} ({project['progress']}%) - Service: {project['service']}")
                action_taken = True
                if project["progress"] == 100:
                    logging.info(f"Performing QA for project {project['project_id']}")
                    time.sleep(random.uniform(1, 3))
                    project["status"] = "completed"
                    logging.info(f"Project {project['project_id']} completed and delivered.")
            if action_taken:
                processed_count += 1
        if processed_count == 0:
            logging.info("No projects progressed in this cycle.")

# --- Global State & Logging ---
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', filename='ai_agent_demo.log', filemode='w')
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
console_handler.setFormatter(formatter)
logging.getLogger().addHandler(console_handler)

mock_client_discovery = MockClientDiscovery()
mock_deal_closing = MockDealClosing()
mock_service_delivery = MockServiceDelivery()
keep_running = True

# --- Simulation Loop ---
def run_simulation():
    global keep_running
    while keep_running:
        logging.info("--- Running Simulation Cycle ---")
        # Client Discovery
        qualified_leads = mock_client_discovery.run_pipeline()

        # Deal Closing
        for lead in qualified_leads:
             mock_deal_closing.receive_lead(lead)
        mock_deal_closing.process_deals()

        # Service Delivery
        mock_service_delivery.process_projects()

        logging.info("--- Simulation Cycle End --- Waiting for next cycle...")
        time.sleep(15) # Wait before next cycle

# --- Flask Dashboard ---
app = Flask(__name__)

@app.route('/')
def dashboard():
    # Simple HTML template for the dashboard
    html_template = """
    <!doctype html>
    <html>
    <head>
        <title>AI Agent Demo Dashboard</title>
        <meta http-equiv="refresh" content="10">
        <style>
            body { font-family: sans-serif; margin: 20px; background-color: #f9f9f9; }
            .container { max-width: 1200px; margin: auto; background-color: #fff; padding: 20px; border-radius: 8px; box-shadow: 0 0 10px rgba(0,0,0,0.1); }
            h1 { text-align: center; color: #333; }
            .module { border: 1px solid #ccc; padding: 15px; margin-bottom: 20px; border-radius: 5px; background-color: #fff; }
            h2 { margin-top: 0; color: #555; border-bottom: 1px solid #eee; padding-bottom: 5px; }
            p { margin: 5px 0; }
            pre { background-color: #f4f4f4; padding: 10px; border: 1px solid #ddd; overflow-x: auto; border-radius: 4px; font-size: 0.9em; max-height: 200px; }
            .grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>AI Agent Demo Dashboard (Auto-refreshing)</h1>
            <div class="grid">
                <div class="module">
                    <h2>Client Discovery</h2>
                    <p>Total Leads Found: {{ discovery.total_leads }}</p>
                    <p>Leads Ready for Closing: {{ discovery.ready_for_closing }}</p>
                    <h3>Latest Leads Preview:</h3>
                    <pre>{{ discovery.leads_preview }}</pre>
                </div>

                <div class="module">
                    <h2>Deal Closing</h2>
                    <p>Active Deals: {{ closing.active_deals }}</p>
                    <p>Deals Closed Won: {{ closing.closed_won }}</p>
                    <h3>Latest Deals Preview:</h3>
                    <pre>{{ closing.deals_preview }}</pre>
                </div>

                <div class="module">
                    <h2>Service Delivery</h2>
                    <p>Active Projects: {{ delivery.active_projects }}</p>
                    <p>Completed Projects: {{ delivery.completed_projects }}</p>
                    <h3>Latest Projects Preview:</h3>
                    <pre>{{ delivery.projects_preview }}</pre>
                </div>
            </div>
        </div>
    </body>
    </html>
    """
    discovery_data = {
        "total_leads": len(mock_client_discovery.leads),
        "ready_for_closing": len(mock_client_discovery.get_qualified_leads_for_closing()),
        "leads_preview": json.dumps(mock_client_discovery.leads[-5:], indent=2) # Show last 5
    }
    closing_data = {
        "active_deals": len([d for d in mock_deal_closing.deals if d["status"] != "closed_won"]),
        "closed_won": len([d for d in mock_deal_closing.deals if d["status"] == "closed_won"]),
        "deals_preview": json.dumps(mock_deal_closing.deals[-5:], indent=2) # Show last 5
    }
    delivery_data = {
        "active_projects": len([p for p in mock_service_delivery.projects if p["status"] == "in_progress"]),
        "completed_projects": len([p for p in mock_service_delivery.projects if p["status"] == "completed"]),
        "projects_preview": json.dumps(mock_service_delivery.projects[-5:], indent=2) # Show last 5
    }

    return render_template_string(html_template,
                                  discovery=discovery_data,
                                  closing=closing_data,
                                  delivery=delivery_data)

def run_dashboard():
    # Run Flask on 0.0.0.0 to make it accessible externally
    # Use a different port if 8080 is common
    try:
        app.run(host='0.0.0.0', port=8088, debug=False)
    except Exception as e:
        logging.error(f"Failed to start dashboard: {e}")

if __name__ == '__main__':
    logging.info("Starting AI Agent Simulation...")

    # Create necessary directories if they don't exist (relative to execution dir)
    import os
    os.makedirs("src/client_discovery/config", exist_ok=True)
    os.makedirs("src/deal_closing/config", exist_ok=True)
    os.makedirs("src/service_delivery/config", exist_ok=True)
    os.makedirs("src/config", exist_ok=True)

    # Start simulation loop in a separate thread
    sim_thread = Thread(target=run_simulation)
    sim_thread.daemon = True # Allows program to exit even if thread is running
    sim_thread.start()

    # Start Flask dashboard in the main thread
    logging.info("Starting Dashboard on port 8088...")
    run_dashboard()

    # Cleanup (though daemon thread might not allow this to be reached easily)
    keep_running = False
    if sim_thread.is_alive():
        sim_thread.join()
    logging.info("AI Agent Simulation Stopped.")


