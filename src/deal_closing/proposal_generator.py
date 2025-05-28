"""
Proposal Generator for Deal Closing
This module generates proposals for prospects based on needs assessment.
"""

import os
import logging
import json
import random
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

class ProposalGenerator:
    """Generates proposals based on needs assessment."""
    
    def __init__(self, service_definitions):
        """Initialize the Proposal Generator."""
        self.service_definitions = service_definitions
        logger.info("Initialized Proposal Generator")
    
    def generate(self, deal, assessment_results):
        """Generate a proposal based on needs assessment."""
        logger.info(f"Generating proposal for: {deal['business_name']}")
        
        try:
            # Get recommended services
            recommended_services = assessment_results.get("recommended_services", [])
            
            # Get service definitions for recommended services
            service_details = self._get_service_details(recommended_services)
            
            # Determine pricing
            pricing_tier = assessment_results.get("pricing_tier", "medium")
            scope = assessment_results.get("scope", "standard")
            
            total_price, service_prices = self._calculate_pricing(service_details, pricing_tier, scope)
            
            # Determine timeline
            timeline = self._calculate_timeline(service_details)
            
            # Generate proposal document
            proposal_file = self._generate_proposal_document(
                deal,
                assessment_results,
                service_details,
                service_prices,
                total_price,
                timeline
            )
            
            # Create proposal object
            proposal = {
                "business_name": deal["business_name"],
                "services": service_details,
                "pricing_tier": pricing_tier,
                "scope": scope,
                "price": total_price,
                "service_prices": service_prices,
                "timeline": timeline,
                "file_path": proposal_file,
                "generation_date": datetime.now(),
                "expiration_date": datetime.now() + timedelta(days=30),
                "primary_service": service_details[0]["name"] if service_details else "Our Services"
            }
            
            logger.info(f"Proposal generated for {deal['business_name']}")
            return proposal
        
        except Exception as e:
            logger.error(f"Error generating proposal for {deal['business_name']}: {e}")
            return {
                "business_name": deal["business_name"],
                "services": [],
                "pricing_tier": "medium",
                "scope": "standard",
                "price": 0,
                "service_prices": {},
                "timeline": {"start_date": datetime.now(), "end_date": datetime.now() + timedelta(days=30)},
                "file_path": "/tmp/proposal_error.pdf",
                "generation_date": datetime.now(),
                "expiration_date": datetime.now() + timedelta(days=30),
                "primary_service": "Our Services"
            }
    
    def _get_service_details(self, recommended_services):
        """Get service definitions for recommended services."""
        service_details = []
        
        for service_id in recommended_services:
            # Find service definition
            service_def = next(
                (s for s in self.service_definitions.get("services", []) if s.get("service_id") == service_id),
                None
            )
            
            if service_def:
                service_details.append({
                    "service_id": service_id,
                    "name": service_def.get("name", service_id),
                    "description": service_def.get("description", ""),
                    "category": service_def.get("category", ""),
                    "base_price": service_def.get("base_price", 100),
                    "price_factors": service_def.get("price_factors", {})
                })
        
        return service_details
    
    def _calculate_pricing(self, service_details, pricing_tier, scope):
        """Calculate pricing for services based on tier and scope."""
        # Define pricing multipliers
        tier_multipliers = {
            "low": 0.8,
            "medium": 1.0,
            "high": 1.2
        }
        
        scope_multipliers = {
            "minimal": 0.8,
            "standard": 1.0,
            "comprehensive": 1.3
        }
        
        # Get multipliers
        tier_multiplier = tier_multipliers.get(pricing_tier, 1.0)
        scope_multiplier = scope_multipliers.get(scope, 1.0)
        
        # Calculate prices for each service
        service_prices = {}
        total_price = 0
        
        for service in service_details:
            base_price = service.get("base_price", 100)
            
            # Apply multipliers
            service_price = base_price * tier_multiplier * scope_multiplier
            
            # Round to nearest 10
            service_price = round(service_price / 10) * 10
            
            service_prices[service["service_id"]] = service_price
            total_price += service_price
        
        # Apply bundle discount for multiple services
        if len(service_details) >= 3:
            bundle_discount = 0.1  # 10% discount
            total_price = total_price * (1 - bundle_discount)
            
            # Round to nearest 10
            total_price = round(total_price / 10) * 10
        
        return total_price, service_prices
    
    def _calculate_timeline(self, service_details):
        """Calculate project timeline based on services."""
        # Define base durations for service categories (in days)
        category_durations = {
            "content_creation": 7,
            "web_development": 14,
            "marketing": 10,
            "analytics": 5,
            "design": 7
        }
        
        # Calculate total duration
        total_duration = 0
        
        for service in service_details:
            category = service.get("category", "")
            duration = category_durations.get(category, 7)
            
            # Some services can be done in parallel, so don't simply add all durations
            total_duration = max(total_duration, duration)
        
        # Add buffer time
        buffer_days = 3
        total_duration += buffer_days
        
        # Calculate start and end dates
        start_date = datetime.now() + timedelta(days=3)  # Start in 3 days
        end_date = start_date + timedelta(days=total_duration)
        
        return {
            "start_date": start_date,
            "end_date": end_date,
            "duration_days": total_duration
        }
    
    def _generate_proposal_document(self, deal, assessment_results, service_details, service_prices, total_price, timeline):
        """Generate a proposal document."""
        # In a real implementation, this would create a PDF
        # For this demo, we'll simulate creating a file
        
        # Create a unique filename
        filename = f"/tmp/proposal_{deal['business_name'].replace(' ', '_').lower()}_{datetime.now().strftime('%Y%m%d')}.pdf"
        
        # Log that we're creating the file
        logger.info(f"Creating proposal document: {filename}")
        
        # In a real implementation, this would create the actual PDF
        # For this demo, we'll just return the filename
        
        return filename
