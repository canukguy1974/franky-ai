"""
Lead Enrichment for Client Discovery
This module enriches lead data with additional information.
"""

import os
import logging
import requests
import time
from datetime import datetime
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)

class LeadEnricher:
    """Enriches lead data with additional information."""
    
    def __init__(self):
        """Initialize the lead enricher."""
        logger.info("Initialized Lead Enricher")
    
    def enrich(self, lead):
        """Enrich a lead with additional data."""
        logger.info(f"Enriching lead: {lead['business_name']}")
        
        enriched_data = {}
        
        # Enrich with website data if available
        if lead.get('website'):
            website_data = self._analyze_website(lead['website'])
            enriched_data.update(website_data)
        
        # Enrich with social media profiles
        social_profiles = self._find_social_profiles(lead['business_name'])
        enriched_data['social_profiles'] = social_profiles
        
        # Estimate business size and maturity
        business_metrics = self._estimate_business_metrics(lead, enriched_data)
        enriched_data.update(business_metrics)
        
        logger.info(f"Lead enrichment completed for {lead['business_name']}")
        return enriched_data
    
    def _analyze_website(self, website_url):
        """Analyze a website for additional information."""
        try:
            logger.info(f"Analyzing website: {website_url}")
            
            # Fetch website
            response = requests.get(website_url, timeout=10)
            
            if response.status_code != 200:
                logger.error(f"Error fetching website: {response.status_code}")
                return {
                    "website_quality": 0,
                    "technologies": [],
                    "has_contact_form": False,
                    "content_topics": []
                }
            
            # Parse HTML
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Check for contact form
            contact_form = bool(soup.select('form'))
            
            # Extract technologies (simplified)
            technologies = []
            if 'wordpress' in response.text.lower():
                technologies.append('WordPress')
            if 'woocommerce' in response.text.lower():
                technologies.append('WooCommerce')
            if 'shopify' in response.text.lower():
                technologies.append('Shopify')
            if 'bootstrap' in response.text.lower():
                technologies.append('Bootstrap')
            if 'jquery' in response.text.lower():
                technologies.append('jQuery')
            
            # Extract content topics
            content = soup.get_text()
            topics = self._extract_topics(content)
            
            # Assess website quality (simplified)
            quality_score = self._assess_website_quality(soup)
            
            return {
                "website_quality": quality_score,
                "technologies": technologies,
                "has_contact_form": contact_form,
                "content_topics": topics
            }
        
        except Exception as e:
            logger.error(f"Error analyzing website {website_url}: {e}")
            return {
                "website_quality": 0,
                "technologies": [],
                "has_contact_form": False,
                "content_topics": []
            }
    
    def _find_social_profiles(self, business_name):
        """Find social media profiles for a business."""
        # In a real implementation, this would use social media APIs or search
        # For this demo, we'll return simulated data
        
        # Simulate finding profiles with 50% probability
        import random
        has_profiles = random.random() > 0.5
        
        if has_profiles:
            return {
                "linkedin": f"https://www.linkedin.com/company/{business_name.lower().replace(' ', '-')}",
                "twitter": f"https://twitter.com/{business_name.lower().replace(' ', '')}"
            }
        else:
            return {}
    
    def _extract_topics(self, content):
        """Extract main topics from content."""
        # In a real implementation, this would use NLP
        # For this demo, we'll use a simple keyword approach
        
        common_business_topics = [
            "marketing", "sales", "growth", "customers", "service",
            "product", "business", "strategy", "digital", "online",
            "technology", "innovation", "solution", "professional"
        ]
        
        content_lower = content.lower()
        found_topics = []
        
        for topic in common_business_topics:
            if topic in content_lower:
                found_topics.append(topic)
        
        return found_topics[:5]  # Return up to 5 topics
    
    def _assess_website_quality(self, soup):
        """Assess the quality of a website."""
        score = 0
        
        # Check for responsive design
        viewport_meta = soup.find('meta', attrs={'name': 'viewport'})
        if viewport_meta:
            score += 20
        
        # Check for structured content
        if soup.find_all(['h1', 'h2', 'h3']):
            score += 20
        
        # Check for images
        if soup.find_all('img'):
            score += 20
        
        # Check for footer with copyright
        footer = soup.find('footer')
        if footer and 'copyright' in footer.text.lower():
            score += 20
        
        # Check for navigation
        if soup.find('nav') or soup.find_all('a', limit=5):
            score += 20
        
        return score
    
    def _estimate_business_metrics(self, lead, enriched_data):
        """Estimate business size, maturity, and other metrics."""
        # In a real implementation, this would use more sophisticated analysis
        # For this demo, we'll use simple heuristics
        
        # Estimate business maturity
        maturity = 0.5  # Default to medium maturity
        
        # Adjust based on website quality
        website_quality = enriched_data.get('website_quality', 0)
        if website_quality > 80:
            maturity += 0.2
        elif website_quality < 40:
            maturity -= 0.2
        
        # Adjust based on social profiles
        social_profiles = enriched_data.get('social_profiles', {})
        if len(social_profiles) >= 2:
            maturity += 0.1
        
        # Adjust based on technologies
        technologies = enriched_data.get('technologies', [])
        if len(technologies) >= 3:
            maturity += 0.1
        
        # Estimate digital presence score
        digital_presence = (
            (website_quality / 100) * 0.6 +
            (len(social_profiles) / 3) * 0.3 +
            (len(technologies) / 5) * 0.1
        )
        
        # Estimate growth indicators
        growth_indicators = []
        
        if 'growth' in enriched_data.get('content_topics', []):
            growth_indicators.append('growth_content')
        
        if 'shopify' in technologies or 'woocommerce' in technologies:
            growth_indicators.append('e_commerce')
        
        # Estimate service needs based on website and technologies
        service_needs = []
        
        if website_quality < 60:
            service_needs.append('website_improvement')
        
        if not social_profiles:
            service_needs.append('social_media_setup')
        
        if 'marketing' in enriched_data.get('content_topics', []):
            service_needs.append('marketing_services')
        
        return {
            "business_maturity": max(0, min(1, maturity)),  # Ensure between 0 and 1
            "digital_presence": max(0, min(1, digital_presence)),  # Ensure between 0 and 1
            "growth_indicators": growth_indicators,
            "estimated_service_needs": service_needs
        }
