"""
Lead Qualification for Client Discovery
This module qualifies leads based on scoring criteria.
"""

import os
import logging
import math
from datetime import datetime

logger = logging.getLogger(__name__)

class LeadQualifier:
    """Qualifies leads based on scoring criteria."""
    
    def __init__(self, scoring_weights):
        """Initialize the lead qualifier."""
        self.scoring_weights = scoring_weights
        logger.info("Initialized Lead Qualifier")
    
    def qualify(self, lead):
        """Qualify a lead and assign a score."""
        logger.info(f"Qualifying lead: {lead['business_name']}")
        
        # Calculate score components
        business_maturity_score = self._score_business_maturity(lead)
        digital_presence_score = self._score_digital_presence(lead)
        growth_indicators_score = self._score_growth_indicators(lead)
        service_needs_score = self._score_service_needs(lead)
        
        # Calculate weighted score
        total_score = (
            business_maturity_score * self.scoring_weights.get("business_maturity", 0.25) +
            digital_presence_score * self.scoring_weights.get("digital_presence", 0.25) +
            growth_indicators_score * self.scoring_weights.get("growth_indicators", 0.25) +
            service_needs_score * self.scoring_weights.get("service_needs", 0.25)
        ) * 100
        
        # Round to nearest integer
        total_score = round(total_score)
        
        # Ensure score is between 0 and 100
        total_score = max(0, min(100, total_score))
        
        # Identify specific needs
        identified_needs = self._identify_needs(lead)
        
        logger.info(f"Lead qualification completed for {lead['business_name']}. Score: {total_score}")
        return total_score, identified_needs
    
    def _score_business_maturity(self, lead):
        """Score the business maturity component."""
        # If enrichment has already calculated this, use that value
        if "business_maturity" in lead:
            return lead["business_maturity"]
        
        # Otherwise, estimate based on available data
        maturity = 0.5  # Default to medium maturity
        
        # Adjust based on website presence
        if lead.get("website"):
            maturity += 0.1
        
        # Adjust based on social profiles
        if lead.get("social_profiles") and len(lead.get("social_profiles", {})) > 0:
            maturity += 0.1
        
        # Ensure score is between 0 and 1
        return max(0, min(1, maturity))
    
    def _score_digital_presence(self, lead):
        """Score the digital presence component."""
        # If enrichment has already calculated this, use that value
        if "digital_presence" in lead:
            return lead["digital_presence"]
        
        # Otherwise, calculate based on available data
        score = 0
        
        # Website quality
        website_quality = lead.get("website_quality", 0)
        website_score = website_quality / 100
        
        # Social media presence
        social_profiles = lead.get("social_profiles", {})
        social_score = min(1, len(social_profiles) / 3)
        
        # Online reviews (if available)
        online_reviews = lead.get("online_reviews", [])
        reviews_score = min(1, len(online_reviews) / 5)
        
        # Calculate weighted score based on digital_presence_factors
        digital_presence_factors = self.scoring_weights.get("digital_presence_factors", {})
        
        score = (
            website_score * digital_presence_factors.get("website_quality", 0.4) +
            social_score * digital_presence_factors.get("social_media", 0.3) +
            reviews_score * digital_presence_factors.get("online_reviews", 0.3)
        )
        
        # Ensure score is between 0 and 1
        return max(0, min(1, score))
    
    def _score_growth_indicators(self, lead):
        """Score the growth indicators component."""
        # Check for growth indicators
        growth_indicators = lead.get("growth_indicators", [])
        
        # Calculate score based on number of indicators
        score = min(1, len(growth_indicators) / 3)
        
        # Ensure score is between 0 and 1
        return max(0, min(1, score))
    
    def _score_service_needs(self, lead):
        """Score the service needs component."""
        # Check for estimated service needs
        service_needs = lead.get("estimated_service_needs", [])
        
        # Calculate score based on number of needs
        score = min(1, len(service_needs) / 3)
        
        # Ensure score is between 0 and 1
        return max(0, min(1, score))
    
    def _identify_needs(self, lead):
        """Identify specific needs based on lead data."""
        needs = []
        
        # Check for specific service needs from enrichment
        estimated_needs = lead.get("estimated_service_needs", [])
        if estimated_needs:
            needs.extend(estimated_needs)
        
        # Check website quality
        website_quality = lead.get("website_quality", 0)
        if website_quality < 40:
            needs.append("website_redesign")
        elif website_quality < 70:
            needs.append("website_improvement")
        
        # Check social media presence
        social_profiles = lead.get("social_profiles", {})
        if not social_profiles:
            needs.append("social_media_setup")
        elif len(social_profiles) < 2:
            needs.append("social_media_expansion")
        
        # Check technologies
        technologies = lead.get("technologies", [])
        if not any(tech.lower() in ["shopify", "woocommerce", "magento"] for tech in technologies):
            needs.append("e_commerce_setup")
        
        # Check content topics
        content_topics = lead.get("content_topics", [])
        if "marketing" in content_topics:
            needs.append("marketing_strategy")
        
        # Remove duplicates and limit to top 3 needs
        unique_needs = list(set(needs))
        return unique_needs[:3]
