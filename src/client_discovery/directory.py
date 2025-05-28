"""
Directory Scanner for Client Discovery
This module scans industry directories for potential clients.
"""

import os
import logging
import requests
import time
from datetime import datetime
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)

class DirectoryScanner:
    """Scanner for industry directories."""
    
    def __init__(self, url, industry):
        """Initialize the directory scanner."""
        self.url = url
        self.industry = industry
        
        logger.info(f"Initialized Directory scanner for {industry} at {url}")
    
    def scan(self):
        """Scan directory for potential clients."""
        logger.info(f"Starting directory scan for {self.industry}")
        
        all_leads = []
        
        try:
            # Fetch directory page
            response = requests.get(self.url)
            
            if response.status_code != 200:
                logger.error(f"Error fetching directory: {response.status_code}")
                return []
            
            # Parse HTML
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Find business listings (this will vary based on the directory structure)
            listings = self._find_listings(soup)
            
            for listing in listings:
                lead = self._process_listing(listing)
                if lead:
                    all_leads.append(lead)
        
        except Exception as e:
            logger.error(f"Error scanning directory {self.url}: {e}")
        
        logger.info(f"Directory scan completed. Found {len(all_leads)} potential leads.")
        return all_leads
    
    def _find_listings(self, soup):
        """Find business listings in the directory page."""
        # This method needs to be customized based on the directory structure
        # For this example, we'll look for common listing patterns
        
        # Try to find listings by common container classes
        listings = soup.select('.business-listing, .directory-item, .company-card')
        
        if not listings:
            # Try alternative selectors
            listings = soup.select('.listing, .result-item, .business')
        
        if not listings:
            # Try to find listings by structure (e.g., a list of items with business info)
            listings = soup.select('ul.results > li, div.results > div')
        
        return listings
    
    def _process_listing(self, listing):
        """Process a single business listing."""
        try:
            # Extract business information (this will vary based on the directory structure)
            
            # Try to find business name
            name_elem = listing.select_one('.name, .title, h2, h3')
            business_name = name_elem.text.strip() if name_elem else None
            
            if not business_name:
                return None
            
            # Try to find website
            website_elem = listing.select_one('a[href^="http"]')
            website = website_elem['href'] if website_elem else None
            
            # Try to find contact info
            phone_elem = listing.select_one('.phone, .tel')
            phone = phone_elem.text.strip() if phone_elem else None
            
            email_elem = listing.select_one('a[href^="mailto:"]')
            email = email_elem['href'][7:] if email_elem else None
            
            # Try to find address
            address_elem = listing.select_one('.address, .location')
            address = address_elem.text.strip() if address_elem else None
            
            # Create lead object
            lead = {
                "business_name": business_name,
                "website": website,
                "phone": phone,
                "email": email,
                "address": address,
                "industry": self.industry,
                "source": "industry_directory",
                "directory_url": self.url,
                "discovery_date": datetime.now()
            }
            
            return lead
        
        except Exception as e:
            logger.error(f"Error processing directory listing: {e}")
            return None
