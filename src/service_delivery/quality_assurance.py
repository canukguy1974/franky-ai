"""
Quality Assurance for Service Delivery
This module handles QA for client deliverables.
"""

import os
import logging
import json
import random
from datetime import datetime

logger = logging.getLogger(__name__)

class QualityAssurance:
    """Handles quality assurance for client deliverables."""
    
    def __init__(self, qa_standards):
        """Initialize the Quality Assurance module."""
        self.qa_standards = qa_standards
        logger.info("Initialized Quality Assurance module")
    
    def review_deliverable(self, deliverable_type, deliverable_file, requirements=None):
        """Review a deliverable for quality assurance."""
        logger.info(f"Reviewing {deliverable_type} deliverable: {deliverable_file}")
        
        try:
            # In a real implementation, this would perform actual QA
            # For this demo, we'll simulate QA review
            
            # Load deliverable content
            content = self._load_deliverable(deliverable_file)
            
            if not content:
                return {
                    "status": "error",
                    "message": "Failed to load deliverable content",
                    "passed": False
                }
            
            # Get QA checklist for deliverable type
            checklist = self._get_qa_checklist(deliverable_type)
            
            # Perform checks
            check_results = self._perform_checks(content, checklist, deliverable_type)
            
            # Calculate overall score
            total_checks = len(check_results)
            passed_checks = sum(1 for result in check_results if result["passed"])
            score = (passed_checks / total_checks) * 100 if total_checks > 0 else 0
            
            # Determine overall status
            passed = score >= self.qa_standards.get("minimum_score", 80)
            
            # Generate report
            report = {
                "deliverable_type": deliverable_type,
                "file": deliverable_file,
                "score": round(score, 1),
                "passed": passed,
                "check_results": check_results,
                "review_date": datetime.now(),
                "recommendations": self._generate_recommendations(check_results)
            }
            
            # Save report to file
            report_file = self._save_report(report, deliverable_type)
            
            result = {
                "status": "success",
                "passed": passed,
                "score": round(score, 1),
                "failed_checks": total_checks - passed_checks,
                "report_file": report_file
            }
            
            logger.info(f"QA review completed. Score: {result['score']}%, Passed: {result['passed']}")
            return result
        
        except Exception as e:
            logger.error(f"Error reviewing deliverable: {e}")
            return {
                "status": "error",
                "message": str(e),
                "passed": False
            }
    
    def _load_deliverable(self, deliverable_file):
        """Load deliverable content from file."""
        # In a real implementation, this would load actual content
        # For this demo, we'll simulate content
        
        # Check if file exists
        if not os.path.exists(deliverable_file):
            logger.error(f"Deliverable file not found: {deliverable_file}")
            return None
        
        # Simulate content based on file extension
        file_ext = os.path.splitext(deliverable_file)[1].lower()
        
        if file_ext in ['.html', '.htm']:
            return {"type": "html", "content": "<html><body><h1>Sample Content</h1></body></html>"}
        elif file_ext == '.css':
            return {"type": "css", "content": "body { font-family: Arial; }"}
        elif file_ext == '.js':
            return {"type": "js", "content": "function sample() { return true; }"}
        elif file_ext in ['.jpg', '.jpeg', '.png', '.gif']:
            return {"type": "image", "content": "binary_data"}
        elif file_ext in ['.doc', '.docx', '.pdf']:
            return {"type": "document", "content": "Sample document content"}
        elif file_ext == '.md':
            return {"type": "markdown", "content": "# Sample Markdown\n\nThis is sample content."}
        else:
            return {"type": "text", "content": "Sample content"}
    
    def _get_qa_checklist(self, deliverable_type):
        """Get QA checklist for a specific deliverable type."""
        # In a real implementation, this would load from configuration
        # For this demo, we'll use hardcoded checklists
        
        checklists = {
            "content": [
                {"id": "spelling", "name": "Spelling and Grammar", "description": "Content is free of spelling and grammar errors"},
                {"id": "tone", "name": "Tone and Voice", "description": "Content matches the required tone and voice"},
                {"id": "length", "name": "Content Length", "description": "Content meets the required length"},
                {"id": "keywords", "name": "Keyword Usage", "description": "Content includes required keywords"},
                {"id": "structure", "name": "Content Structure", "description": "Content has appropriate headings and structure"}
            ],
            "website": [
                {"id": "responsive", "name": "Responsive Design", "description": "Website displays correctly on all device sizes"},
                {"id": "links", "name": "Link Functionality", "description": "All links work correctly"},
                {"id": "images", "name": "Image Optimization", "description": "Images are optimized for web"},
                {"id": "performance", "name": "Page Speed", "description": "Pages load quickly"},
                {"id": "accessibility", "name": "Accessibility", "description": "Website meets accessibility standards"}
            ],
            "data_analysis": [
                {"id": "accuracy", "name": "Data Accuracy", "description": "Analysis is based on accurate data"},
                {"id": "methodology", "name": "Methodology", "description": "Appropriate methodology is used"},
                {"id": "insights", "name": "Actionable Insights", "description": "Analysis provides actionable insights"},
                {"id": "visualization", "name": "Data Visualization", "description": "Data is visualized effectively"},
                {"id": "conclusions", "name": "Conclusions", "description": "Conclusions are supported by the data"}
            ],
            "social_media": [
                {"id": "engagement", "name": "Engagement Potential", "description": "Content is likely to drive engagement"},
                {"id": "branding", "name": "Brand Consistency", "description": "Content is consistent with brand guidelines"},
                {"id": "hashtags", "name": "Hashtag Strategy", "description": "Appropriate hashtags are used"},
                {"id": "length", "name": "Optimal Length", "description": "Content is appropriate length for platform"},
                {"id": "cta", "name": "Call to Action", "description": "Includes clear call to action when appropriate"}
            ]
        }
        
        return checklists.get(deliverable_type, [
            {"id": "quality", "name": "Overall Quality", "description": "Deliverable meets quality standards"},
            {"id": "requirements", "name": "Requirements", "description": "Deliverable meets all requirements"},
            {"id": "format", "name": "Format", "description": "Deliverable is in the correct format"}
        ])
    
    def _perform_checks(self, content, checklist, deliverable_type):
        """Perform QA checks on content."""
        # In a real implementation, this would perform actual checks
        # For this demo, we'll simulate check results
        
        check_results = []
        
        for check in checklist:
            # Simulate check result (80% pass rate)
            passed = random.random() < 0.8
            
            # Generate detailed feedback
            feedback = self._generate_feedback(check, passed, deliverable_type)
            
            check_results.append({
                "check_id": check["id"],
                "name": check["name"],
                "description": check["description"],
                "passed": passed,
                "feedback": feedback
            })
        
        return check_results
    
    def _generate_feedback(self, check, passed, deliverable_type):
        """Generate detailed feedback for a check."""
        # In a real implementation, this would generate actual feedback
        # For this demo, we'll simulate feedback
        
        if passed:
            feedback_templates = [
                "Meets standards for {name}.",
                "{name} requirements satisfied.",
                "No issues found with {name}.",
                "{name} check passed successfully."
            ]
        else:
            if check["id"] == "spelling":
                return "Found 3 spelling errors and 2 grammar issues that need correction."
            elif check["id"] == "responsive":
                return "Layout breaks on mobile devices (320px width). Navigation menu overlaps content."
            elif check["id"] == "performance":
                return "Page load time exceeds 3 seconds. Consider optimizing images and reducing JavaScript."
            elif check["id"] == "accessibility":
                return "Missing alt text on 4 images. Color contrast issues on header navigation."
            
            feedback_templates = [
                "{name} needs improvement. Please review the requirements.",
                "{name} does not meet standards. Revision needed.",
                "Issues found with {name}. See recommendations for details.",
                "{name} check failed. Attention required."
            ]
        
        template = random.choice(feedback_templates)
        return template.format(name=check["name"])
    
    def _generate_recommendations(self, check_results):
        """Generate recommendations based on failed checks."""
        recommendations = []
        
        for result in check_results:
            if not result["passed"]:
                if result["check_id"] == "spelling":
                    recommendations.append("Run content through Grammarly or a similar tool to catch spelling and grammar errors.")
                elif result["check_id"] == "tone":
                    recommendations.append("Review brand voice guidelines and adjust content tone accordingly.")
                elif result["check_id"] == "responsive":
                    recommendations.append("Test on multiple devices and fix responsive design issues.")
                elif result["check_id"] == "performance":
                    recommendations.append("Optimize images and minimize CSS/JavaScript to improve page load speed.")
                elif result["check_id"] == "accessibility":
                    recommendations.append("Add alt text to all images and ensure color contrast meets WCAG standards.")
                else:
                    recommendations.append(f"Address issues with {result['name']} as noted in the feedback.")
        
        return recommendations
    
    def _save_report(self, report, deliverable_type):
        """Save QA report to a file."""
        # In a real implementation, this would save an actual file
        # For this demo, we'll simulate a file path
        
        return f"/tmp/qa_report_{deliverable_type}_{datetime.now().strftime('%Y%m%d')}.json"
