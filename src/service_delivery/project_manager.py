"""
Project Manager for Service Delivery
This module manages client projects and workflows.
"""

import os
import logging
import json
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

class ProjectManager:
    """Manages client projects and workflows."""
    
    def __init__(self):
        """Initialize the Project Manager."""
        logger.info("Initialized Project Manager")
    
    def create_project(self, client_id, service_type, requirements, timeline=None):
        """Create a new project for a client."""
        logger.info(f"Creating project for client {client_id}, service type: {service_type}")
        
        try:
            # Generate project ID
            project_id = f"PRJ-{client_id}-{datetime.now().strftime('%Y%m%d%H%M')}"
            
            # Set default timeline if not provided
            if not timeline:
                start_date = datetime.now()
                end_date = start_date + timedelta(days=14)  # Default 2-week timeline
                timeline = {
                    "start_date": start_date,
                    "end_date": end_date,
                    "duration_days": 14
                }
            
            # Create project structure
            project = {
                "project_id": project_id,
                "client_id": client_id,
                "service_type": service_type,
                "requirements": requirements,
                "timeline": timeline,
                "status": "created",
                "creation_date": datetime.now(),
                "tasks": self._generate_tasks(service_type, requirements, timeline),
                "deliverables": self._generate_deliverables(service_type, requirements),
                "team_members": self._assign_team_members(service_type),
                "progress": 0
            }
            
            logger.info(f"Project created successfully. ID: {project_id}")
            return project
        
        except Exception as e:
            logger.error(f"Error creating project: {e}")
            return {
                "error": str(e),
                "success": False
            }
    
    def update_project_status(self, project, new_status, notes=None):
        """Update the status of a project."""
        logger.info(f"Updating project {project['project_id']} status to: {new_status}")
        
        try:
            old_status = project["status"]
            project["status"] = new_status
            project["status_history"] = project.get("status_history", []) + [
                {
                    "from": old_status,
                    "to": new_status,
                    "timestamp": datetime.now(),
                    "notes": notes
                }
            ]
            
            # Update progress based on status
            if new_status == "in_progress":
                project["progress"] = 25
            elif new_status == "review":
                project["progress"] = 75
            elif new_status == "completed":
                project["progress"] = 100
                project["completion_date"] = datetime.now()
            
            logger.info(f"Project status updated successfully to {new_status}")
            return project
        
        except Exception as e:
            logger.error(f"Error updating project status: {e}")
            return {
                "error": str(e),
                "success": False
            }
    
    def update_task_status(self, project, task_id, new_status, notes=None):
        """Update the status of a task within a project."""
        logger.info(f"Updating task {task_id} status to: {new_status}")
        
        try:
            # Find the task
            task_found = False
            for task in project["tasks"]:
                if task["task_id"] == task_id:
                    old_status = task["status"]
                    task["status"] = new_status
                    task["status_history"] = task.get("status_history", []) + [
                        {
                            "from": old_status,
                            "to": new_status,
                            "timestamp": datetime.now(),
                            "notes": notes
                        }
                    ]
                    
                    if new_status == "completed":
                        task["completion_date"] = datetime.now()
                    
                    task_found = True
                    break
            
            if not task_found:
                logger.error(f"Task {task_id} not found in project {project['project_id']}")
                return {
                    "error": f"Task {task_id} not found",
                    "success": False
                }
            
            # Update overall project progress
            completed_tasks = sum(1 for task in project["tasks"] if task["status"] == "completed")
            total_tasks = len(project["tasks"])
            project["progress"] = (completed_tasks / total_tasks) * 100 if total_tasks > 0 else 0
            
            logger.info(f"Task status updated successfully to {new_status}")
            return project
        
        except Exception as e:
            logger.error(f"Error updating task status: {e}")
            return {
                "error": str(e),
                "success": False
            }
    
    def add_deliverable(self, project, deliverable_type, file_path, notes=None):
        """Add a deliverable to a project."""
        logger.info(f"Adding {deliverable_type} deliverable to project {project['project_id']}")
        
        try:
            # Generate deliverable ID
            deliverable_id = f"DEL-{project['project_id']}-{len(project['deliverables']) + 1}"
            
            # Create deliverable
            deliverable = {
                "deliverable_id": deliverable_id,
                "type": deliverable_type,
                "file_path": file_path,
                "creation_date": datetime.now(),
                "status": "pending_review",
                "notes": notes
            }
            
            # Add to project
            project["deliverables"].append(deliverable)
            
            logger.info(f"Deliverable added successfully. ID: {deliverable_id}")
            return project
        
        except Exception as e:
            logger.error(f"Error adding deliverable: {e}")
            return {
                "error": str(e),
                "success": False
            }
    
    def generate_project_report(self, project):
        """Generate a report for a project."""
        logger.info(f"Generating report for project {project['project_id']}")
        
        try:
            # Calculate project metrics
            completed_tasks = sum(1 for task in project["tasks"] if task["status"] == "completed")
            total_tasks = len(project["tasks"])
            completion_percentage = (completed_tasks / total_tasks) * 100 if total_tasks > 0 else 0
            
            # Calculate timeline metrics
            timeline = project["timeline"]
            start_date = timeline["start_date"]
            end_date = timeline["end_date"]
            
            current_date = datetime.now()
            total_duration = (end_date - start_date).days
            elapsed_duration = (current_date - start_date).days
            
            if total_duration > 0:
                timeline_percentage = (elapsed_duration / total_duration) * 100
            else:
                timeline_percentage = 100
            
            # Determine if project is on track
            if project["status"] == "completed":
                status_summary = "Completed"
            elif timeline_percentage > completion_percentage + 10:
                status_summary = "Behind Schedule"
            elif timeline_percentage < completion_percentage - 10:
                status_summary = "Ahead of Schedule"
            else:
                status_summary = "On Track"
            
            # Generate report
            report = {
                "project_id": project["project_id"],
                "client_id": project["client_id"],
                "service_type": project["service_type"],
                "status": project["status"],
                "status_summary": status_summary,
                "progress": project["progress"],
                "timeline": {
                    "start_date": start_date,
                    "end_date": end_date,
                    "elapsed_percentage": min(100, round(timeline_percentage, 1)),
                    "days_remaining": max(0, (end_date - current_date).days)
                },
                "tasks": {
                    "total": total_tasks,
                    "completed": completed_tasks,
                    "completion_percentage": round(completion_percentage, 1)
                },
                "deliverables": {
                    "total": len(project["deliverables"]),
                    "by_status": self._count_deliverables_by_status(project["deliverables"])
                },
                "team_members": project["team_members"],
                "generation_date": datetime.now()
            }
            
            # Save report to file
            report_file = self._save_report(report, project["project_id"])
            
            logger.info(f"Project report generated successfully")
            return {
                "report": report,
                "report_file": report_file
            }
        
        except Exception as e:
            logger.error(f"Error generating project report: {e}")
            return {
                "error": str(e),
                "success": False
            }
    
    def _generate_tasks(self, service_type, requirements, timeline):
        """Generate tasks based on service type and requirements."""
        # In a real implementation, this would generate tasks based on service type
        # For this demo, we'll use predefined task templates
        
        tasks = []
        
        if service_type == "content_creation":
            tasks = [
                {"task_id": "T1", "name": "Research", "description": "Research topic and gather information", "status": "pending", "assignee": None},
                {"task_id": "T2", "name": "Outline", "description": "Create content outline", "status": "pending", "assignee": None},
                {"task_id": "T3", "name": "Draft", "description": "Write first draft", "status": "pending", "assignee": None},
                {"task_id": "T4", "name": "Review", "description": "Internal review and editing", "status": "pending", "assignee": None},
                {"task_id": "T5", "name": "Finalize", "description": "Finalize content and format", "status": "pending", "assignee": None}
            ]
        elif service_type == "web_development":
            tasks = [
                {"task_id": "T1", "name": "Requirements", "description": "Gather detailed requirements", "status": "pending", "assignee": None},
                {"task_id": "T2", "name": "Design", "description": "Create website design", "status": "pending", "assignee": None},
                {"task_id": "T3", "name": "Development", "description": "Develop website", "status": "pending", "assignee": None},
                {"task_id": "T4", "name": "Testing", "description": "Test website functionality", "status": "pending", "assignee": None},
                {"task_id": "T5", "name": "Deployment", "description": "Deploy website", "status": "pending", "assignee": None}
            ]
        elif service_type == "data_analysis":
            tasks = [
                {"task_id": "T1", "name": "Data Collection", "description": "Collect and organize data", "status": "pending", "assignee": None},
                {"task_id": "T2", "name": "Data Cleaning", "description": "Clean and prepare data", "status": "pending", "assignee": None},
                {"task_id": "T3", "name": "Analysis", "description": "Perform data analysis", "status": "pending", "assignee": None},
                {"task_id": "T4", "name": "Visualization", "description": "Create data visualizations", "status": "pending", "assignee": None},
                {"task_id": "T5", "name": "Report", "description": "Generate analysis report", "status": "pending", "assignee": None}
            ]
        else:
            tasks = [
                {"task_id": "T1", "name": "Planning", "description": "Plan project execution", "status": "pending", "assignee": None},
                {"task_id": "T2", "name": "Execution", "description": "Execute project tasks", "status": "pending", "assignee": None},
                {"task_id": "T3", "name": "Review", "description": "Review project results", "status": "pending", "assignee": None},
                {"task_id": "T4", "name": "Delivery", "description": "Deliver project results", "status": "pending", "assignee": None}
            ]
        
        # Distribute tasks across timeline
        start_date = timeline["start_date"]
        end_date = timeline["end_date"]
        duration = (end_date - start_date).days
        
        task_count = len(tasks)
        for i, task in enumerate(tasks):
            # Calculate task dates based on position in sequence
            task_start_offset = (duration * i) // task_count
            task_end_offset = (duration * (i + 1)) // task_count
            
            task["start_date"] = start_date + timedelta(days=task_start_offset)
            task["end_date"] = start_date + timedelta(days=task_end_offset)
        
        return tasks
    
    def _generate_deliverables(self, service_type, requirements):
        """Generate expected deliverables based on service type and requirements."""
        # In a real implementation, this would generate deliverables based on requirements
        # For this demo, we'll use predefined deliverable templates
        
        if service_type == "content_creation":
            return [
                {
                    "deliverable_id": "D1",
                    "type": "content",
                    "description": "Final content document",
                    "status": "planned",
                    "due_date": datetime.now() + timedelta(days=14)
                }
            ]
        elif service_type == "web_development":
            return [
                {
                    "deliverable_id": "D1",
                    "type": "website",
                    "description": "Completed website",
                    "status": "planned",
                    "due_date": datetime.now() + timedelta(days=14)
                },
                {
                    "deliverable_id": "D2",
                    "type": "documentation",
                    "description": "Website documentation",
                    "status": "planned",
                    "due_date": datetime.now() + timedelta(days=14)
                }
            ]
        elif service_type == "data_analysis":
            return [
                {
                    "deliverable_id": "D1",
                    "type": "data_analysis",
                    "description": "Data analysis report",
                    "status": "planned",
                    "due_date": datetime.now() + timedelta(days=14)
                },
                {
                    "deliverable_id": "D2",
                    "type": "visualization",
                    "description": "Data visualizations",
                    "status": "planned",
                    "due_date": datetime.now() + timedelta(days=14)
                }
            ]
        else:
            return [
                {
                    "deliverable_id": "D1",
                    "type": "report",
                    "description": "Project report",
                    "status": "planned",
                    "due_date": datetime.now() + timedelta(days=14)
                }
   
(Content truncated due to size limit. Use line ranges to read in chunks)