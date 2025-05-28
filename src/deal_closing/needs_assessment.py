"""
Needs Assessment for Deal Closing
This module assesses prospect needs to prepare proposals.
"""

import os
import logging
import json
from datetime import datetime

logger = logging.getLogger(__name__)

class NeedsAssessment:
    """Assesses prospect needs for proposal preparation."""
    
    def __init__(self):
        """Initialize the Needs Assessment module."""
        logger.info("Initialized Needs Assessment module")
    
    def assess(self, deal):
        """Assess the needs of a prospect based on available data."""
        logger.info(f"Conducting needs assessment for: {deal['business_name']}")
        
        try:
            # Get lead data if available
            lead_id = deal.get("lead_id")
            lead_data = self._get_lead_data(lead_id) if lead_id else {}
            
            # Combine lead data with deal data
            assessment_data = {**lead_data, **deal}
            
            # Extract identified needs
            identified_needs = assessment_data.get("identified_needs", [])
            
            # Analyze communications for additional needs
            communications = deal.get("communications", [])
            communication_needs = self._analyze_communications(communications)
            
            # Combine all needs
            all_needs = list(set(identified_needs + communication_needs))
            
            # Map needs to services
            recommended_services = self._map_needs_to_services(all_needs)
            
            # Determine scope and pricing tier
            scope = self._determine_scope(assessment_data)
            pricing_tier = self._determine_pricing_tier(assessment_data)
            
            # Create assessment results
            assessment_results = {
                "identified_needs": all_needs,
                "recommended_services": recommended_services,
                "scope": scope,
                "pricing_tier": pricing_tier,
                "assessment_date": datetime.now()
            }
            
            logger.info(f"Needs assessment completed for {deal['business_name']}")
            return assessment_results
        
        except Exception as e:
            logger.error(f"Error in needs assessment for {deal['business_name']}: {e}")
            return {
                "identified_needs": deal.get("identified_needs", []),
                "recommended_services": [],
                "scope": "standard",
                "pricing_tier": "medium",
                "assessment_date": datetime.now()
            }
    
    def _get_lead_data(self, lead_id):
        """Get lead data from the database."""
        # In a real implementation, this would query the database
        # For this demo, we'll return simulated data
        return {
            "website_quality": 65,
            "digital_presence": 0.6,
            "business_maturity": 0.7,
            "growth_indicators": ["growth_content", "e_commerce"],
            "estimated_service_needs": ["website_improvement", "marketing_services"]
        }
    
    def _analyze_communications(self, communications):
        """Analyze communications to identify additional needs."""
        needs = []
        
        for comm in communications:
            if comm.get("direction") == "inbound":
                content = comm.get("content", "").lower()
                
                # Check for keywords indicating needs
                if "website" in content or "web" in content:
                    needs.append("website_improvement")
                
                if "social" in content or "facebook" in content or "instagram" in content:
                    needs.append("social_media_management")
                
                if "content" in content or "blog" in content or "article" in content:
                    needs.append("content_creation")
                
                if "seo" in content or "search engine" in content or "google" in content:
                    needs.append("seo_optimization")
                
                if "analytics" in content or "data" in content or "report" in content:
                    needs.append("analytics_reporting")
        
        return needs
    
    def _map_needs_to_services(self, needs):
        """Map identified needs to specific services."""
        service_mapping = {
            "website_redesign": ["website_design", "website_development"],
            "website_improvement": ["website_optimization", "website_maintenance"],
            "social_media_setup": ["social_media_account_creation", "social_media_strategy"],
            "social_media_expansion": ["social_media_management", "social_media_content"],
            "social_media_management": ["social_media_management", "social_media_content"],
            "e_commerce_setup": ["e_commerce_development", "product_catalog_setup"],
            "marketing_strategy": ["marketing_plan", "marketing_consultation"],
            "marketing_services": ["content_marketing", "email_marketing"],
            "content_creation": ["blog_post_writing", "article_writing"],
            "seo_optimization": ["seo_audit", "seo_implementation"],
            "analytics_reporting": ["analytics_setup", "performance_reporting"]
        }
        
        recommended_services = []
        
        for need in needs:
            if need in service_mapping:
                recommended_services.extend(service_mapping[need])
        
        # Remove duplicates
        return list(set(recommended_services))
    
    def _determine_scope(self, assessment_data):
        """Determine the appropriate scope based on assessment data."""
        # Count the number of needs and services
        needs_count = len(assessment_data.get("identified_needs", []))
        
        if needs_count <= 1:
            return "minimal"
        elif needs_count <= 3:
            return "standard"
        else:
            return "comprehensive"
    
    def _determine_pricing_tier(self, assessment_data):
        """Determine the appropriate pricing tier based on assessment data."""
        # Consider business maturity and digital presence
        business_maturity = assessment_data.get("business_maturity", 0.5)
        digital_presence = assessment_data.get("digital_presence", 0.5)
        
        # Calculate a combined score
        combined_score = (business_maturity + digital_presence) / 2
        
        if combined_score < 0.4:
            return "low"
        elif combined_score < 0.7:
            return "medium"
        else:
            return "high"
