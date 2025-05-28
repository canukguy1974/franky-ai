"""
Database Manager for the AI Agent
This module handles all database operations.
"""

import os
import logging
import json
from datetime import datetime
import pymongo
from bson.objectid import ObjectId

logger = logging.getLogger(__name__)

class DatabaseManager:
    """Manages database operations for the AI agent."""
    
    def __init__(self, connection_string):
        """Initialize the Database Manager."""
        self.connection_string = connection_string
        self.client = None
        self.db = None
        logger.info("Initialized Database Manager")
    
    def connect(self, db_name="ai_agent"):
        """Connect to the MongoDB database."""
        try:
            logger.info(f"Connecting to MongoDB database: {db_name}")
            self.client = pymongo.MongoClient(self.connection_string)
            self.db = self.client[db_name]
            logger.info("Connected to MongoDB successfully")
            return True
        except Exception as e:
            logger.error(f"Error connecting to MongoDB: {e}")
            return False
    
    def disconnect(self):
        """Disconnect from the MongoDB database."""
        if self.client:
            self.client.close()
            self.client = None
            self.db = None
            logger.info("Disconnected from MongoDB")
    
    def insert_lead(self, lead_data):
        """Insert a new lead into the database."""
        try:
            if not self.db:
                if not self.connect():
                    return None
            
            # Add timestamp
            lead_data["created_at"] = datetime.now()
            lead_data["updated_at"] = datetime.now()
            
            # Insert into leads collection
            result = self.db.leads.insert_one(lead_data)
            logger.info(f"Inserted lead with ID: {result.inserted_id}")
            
            # Return the inserted document with string ID
            lead_data["_id"] = str(result.inserted_id)
            return lead_data
        
        except Exception as e:
            logger.error(f"Error inserting lead: {e}")
            return None
    
    def update_lead(self, lead_id, update_data):
        """Update a lead in the database."""
        try:
            if not self.db:
                if not self.connect():
                    return False
            
            # Add updated timestamp
            update_data["updated_at"] = datetime.now()
            
            # Update lead
            result = self.db.leads.update_one(
                {"_id": ObjectId(lead_id)},
                {"$set": update_data}
            )
            
            logger.info(f"Updated lead {lead_id}, matched: {result.matched_count}, modified: {result.modified_count}")
            return result.modified_count > 0
        
        except Exception as e:
            logger.error(f"Error updating lead {lead_id}: {e}")
            return False
    
    def get_lead(self, lead_id):
        """Get a lead from the database by ID."""
        try:
            if not self.db:
                if not self.connect():
                    return None
            
            # Find lead
            lead = self.db.leads.find_one({"_id": ObjectId(lead_id)})
            
            if lead:
                # Convert ObjectId to string
                lead["_id"] = str(lead["_id"])
                logger.info(f"Retrieved lead {lead_id}")
                return lead
            else:
                logger.warning(f"Lead {lead_id} not found")
                return None
        
        except Exception as e:
            logger.error(f"Error getting lead {lead_id}: {e}")
            return None
    
    def get_leads(self, filters=None, limit=100, skip=0, sort_by="created_at", sort_dir=-1):
        """Get leads from the database with optional filtering."""
        try:
            if not self.db:
                if not self.connect():
                    return []
            
            # Apply filters if provided
            query = filters if filters else {}
            
            # Get leads with pagination and sorting
            cursor = self.db.leads.find(query).sort(sort_by, sort_dir).skip(skip).limit(limit)
            
            # Convert to list and format IDs
            leads = []
            for lead in cursor:
                lead["_id"] = str(lead["_id"])
                leads.append(lead)
            
            logger.info(f"Retrieved {len(leads)} leads")
            return leads
        
        except Exception as e:
            logger.error(f"Error getting leads: {e}")
            return []
    
    def insert_deal(self, deal_data):
        """Insert a new deal into the database."""
        try:
            if not self.db:
                if not self.connect():
                    return None
            
            # Add timestamp
            deal_data["created_at"] = datetime.now()
            deal_data["updated_at"] = datetime.now()
            
            # Insert into deals collection
            result = self.db.deals.insert_one(deal_data)
            logger.info(f"Inserted deal with ID: {result.inserted_id}")
            
            # Return the inserted document with string ID
            deal_data["_id"] = str(result.inserted_id)
            return deal_data
        
        except Exception as e:
            logger.error(f"Error inserting deal: {e}")
            return None
    
    def update_deal(self, deal_id, update_data):
        """Update a deal in the database."""
        try:
            if not self.db:
                if not self.connect():
                    return False
            
            # Add updated timestamp
            update_data["updated_at"] = datetime.now()
            
            # Update deal
            result = self.db.deals.update_one(
                {"_id": ObjectId(deal_id)},
                {"$set": update_data}
            )
            
            logger.info(f"Updated deal {deal_id}, matched: {result.matched_count}, modified: {result.modified_count}")
            return result.modified_count > 0
        
        except Exception as e:
            logger.error(f"Error updating deal {deal_id}: {e}")
            return False
    
    def get_deal(self, deal_id):
        """Get a deal from the database by ID."""
        try:
            if not self.db:
                if not self.connect():
                    return None
            
            # Find deal
            deal = self.db.deals.find_one({"_id": ObjectId(deal_id)})
            
            if deal:
                # Convert ObjectId to string
                deal["_id"] = str(deal["_id"])
                logger.info(f"Retrieved deal {deal_id}")
                return deal
            else:
                logger.warning(f"Deal {deal_id} not found")
                return None
        
        except Exception as e:
            logger.error(f"Error getting deal {deal_id}: {e}")
            return None
    
    def get_deals(self, filters=None, limit=100, skip=0, sort_by="created_at", sort_dir=-1):
        """Get deals from the database with optional filtering."""
        try:
            if not self.db:
                if not self.connect():
                    return []
            
            # Apply filters if provided
            query = filters if filters else {}
            
            # Get deals with pagination and sorting
            cursor = self.db.deals.find(query).sort(sort_by, sort_dir).skip(skip).limit(limit)
            
            # Convert to list and format IDs
            deals = []
            for deal in cursor:
                deal["_id"] = str(deal["_id"])
                deals.append(deal)
            
            logger.info(f"Retrieved {len(deals)} deals")
            return deals
        
        except Exception as e:
            logger.error(f"Error getting deals: {e}")
            return []
    
    def insert_project(self, project_data):
        """Insert a new project into the database."""
        try:
            if not self.db:
                if not self.connect():
                    return None
            
            # Add timestamp
            project_data["created_at"] = datetime.now()
            project_data["updated_at"] = datetime.now()
            
            # Insert into projects collection
            result = self.db.projects.insert_one(project_data)
            logger.info(f"Inserted project with ID: {result.inserted_id}")
            
            # Return the inserted document with string ID
            project_data["_id"] = str(result.inserted_id)
            return project_data
        
        except Exception as e:
            logger.error(f"Error inserting project: {e}")
            return None
    
    def update_project(self, project_id, update_data):
        """Update a project in the database."""
        try:
            if not self.db:
                if not self.connect():
                    return False
            
            # Add updated timestamp
            update_data["updated_at"] = datetime.now()
            
            # Update project
            result = self.db.projects.update_one(
                {"_id": ObjectId(project_id)},
                {"$set": update_data}
            )
            
            logger.info(f"Updated project {project_id}, matched: {result.matched_count}, modified: {result.modified_count}")
            return result.modified_count > 0
        
        except Exception as e:
            logger.error(f"Error updating project {project_id}: {e}")
            return False
    
    def get_project(self, project_id):
        """Get a project from the database by ID."""
        try:
            if not self.db:
                if not self.connect():
                    return None
            
            # Find project
            project = self.db.projects.find_one({"_id": ObjectId(project_id)})
            
            if project:
                # Convert ObjectId to string
                project["_id"] = str(project["_id"])
                logger.info(f"Retrieved project {project_id}")
                return project
            else:
                logger.warning(f"Project {project_id} not found")
                return None
        
        except Exception as e:
            logger.error(f"Error getting project {project_id}: {e}")
            return None
    
    def get_projects(self, filters=None, limit=100, skip=0, sort_by="created_at", sort_dir=-1):
        """Get projects from the database with optional filtering."""
        try:
            if not self.db:
                if not self.connect():
                    return []
            
            # Apply filters if provided
            query = filters if filters else {}
            
            # Get projects with pagination and sorting
            cursor = self.db.projects.find(query).sort(sort_by, sort_dir).skip(skip).limit(limit)
            
            # Convert to list and format IDs
            projects = []
            for project in cursor:
                project["_id"] = str(project["_id"])
                projects.append(project)
            
            logger.info(f"Retrieved {len(projects)} projects")
            return projects
        
        except Exception as e:
            logger.error(f"Error getting projects: {e}")
            return []
    
    def get_stats(self):
        """Get statistics from the database."""
        try:
            if not self.db:
                if not self.connect():
                    return {}
            
            # Get collection counts
            lead_count = self.db.leads.count_documents({})
            deal_count = self.db.deals.count_documents({})
            project_count = self.db.projects.count_documents({})
            
            # Get status counts for deals
            deal_status_counts = {}
            deal_statuses = ["new", "contacted", "negotiating", "closed_won", "closed_lost"]
            for status in deal_statuses:
                count = self.db.deals.count_documents({"status": status})
                deal_status_counts[status] = count
            
            # Get status counts for projects
            project_status_counts = {}
            project_statuses = ["created", "in_progress", "review", "completed"]
            for status in project_statuses:
                count = self.db.projects.count_documents({"status": status})
                project_status_counts[status] = count
            
            # Get recent activity
            recent_leads = self.get_leads(limit=5)
            recent_deals = self.get_deals(limit=5)
            recent_projects = self.get_projects(limit=5)
            
            stats = {
                "counts": {
                    "leads": lead_count,
                    "deals": deal_count,
                    "projects": project_count
                },
                "deal_status_counts": deal_status_counts,
                "project_status_counts": project_status_counts,
                "recent_activity": {
                    "leads": recent_leads,
                    "deals": recent_deals,
                    "projects": recent_projects
                },
                "timestamp": datetime.now()
            }
            
            logger.info("Retrieved database statistics")
            return stats
        
        except Exception as e:
            logger.error(f"Error getting database statistics: {e}")
            return {}
