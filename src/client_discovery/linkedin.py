"""
LinkedIn Scanner for Client Discovery
This module scans LinkedIn for potential clients.
"""

import os
import logging
import requests
import time
import json
from datetime import datetime

logger = logging.getLogger(__name__)

class LinkedInScanner:
    """Scanner for LinkedIn API."""
    
    def __init__(self, api_key, api_secret, search_terms, filters=None):
        """Initialize the LinkedIn scanner."""
        self.api_key = api_key
        self.api_secret = api_secret
        self.search_terms = search_terms
        self.filters = filters or {}
        self.access_token = None
        self.base_url = "https://api.linkedin.com/v2"
        
        logger.info(f"Initialized LinkedIn scanner with {len(search_terms)} search terms")
    
    def scan(self):
        """Scan LinkedIn for potential clients."""
        logger.info("Starting LinkedIn scan")
        
        # Authenticate with LinkedIn API
        self._authenticate()
        
        if not self.access_token:
            logger.error("LinkedIn authentication failed. Cannot proceed with scan.")
            return []
        
        all_leads = []
        
        for term in self.search_terms:
            try:
                logger.info(f"Scanning LinkedIn for: {term}")
                
                # Search for companies
                companies = self._search_companies(term)
                
                for company in companies:
                    # Apply filters
                    if self._apply_filters(company):
                        lead = self._process_company(company, term)
                        all_leads.append(lead)
            
            except Exception as e:
                logger.error(f"Error scanning LinkedIn for {term}: {e}")
            
            # Respect rate limits
            time.sleep(1)
        
        logger.info(f"LinkedIn scan completed. Found {len(all_leads)} potential leads.")
        return all_leads
    
    def _authenticate(self):
        """Authenticate with LinkedIn API."""
        try:
            auth_url = "https://www.linkedin.com/oauth/v2/accessToken"
            
            data = {
                "grant_type": "client_credentials",
                "client_id": self.api_key,
                "client_secret": self.api_secret
            }
            
            response = requests.post(auth_url, data=data)
            
            if response.status_code == 200:
                token_data = response.json()
                self.access_token = token_data.get("access_token")
                logger.info("LinkedIn authentication successful")
            else:
                logger.error(f"LinkedIn authentication failed: {response.text}")
        
        except Exception as e:
            logger.error(f"Error authenticating with LinkedIn: {e}")
    
    def _search_companies(self, term):
        """Search for companies on LinkedIn."""
        try:
            search_url = f"{self.base_url}/search/companies"
            
            params = {
                "q": term,
                "count": 25  # Number of results per page
            }
            
            headers = {
                "Authorization": f"Bearer {self.access_token}",
                "Content-Type": "application/json"
            }
            
            response = requests.get(search_url, params=params, headers=headers)
            
            if response.status_code == 200:
                data = response.json()
                return data.get("elements", [])
            else:
                logger.error(f"LinkedIn company search failed: {response.text}")
                return []
        
        except Exception as e:
            logger.error(f"Error searching LinkedIn companies: {e}")
            return []
    
    def _apply_filters(self, company):
        """Apply filters to company data."""
        # Check company size filter
        if "company_size" in self.filters:
            size_range = self.filters["company_size"].split("-")
            if len(size_range) == 2:
                min_size = int(size_range[0])
                max_size = int(size_range[1]) if size_range[1] != "" else float("inf")
                
                employee_count = company.get("employeeCount", 0)
                
                if employee_count < min_size or employee_count > max_size:
                    return False
        
        # Check founded within years filter
        if "founded_within_years" in self.filters:
            max_years = int(self.filters["founded_within_years"])
            founded_year = company.get("foundedYear")
            
            if founded_year:
                current_year = datetime.now().year
                years_since_founding = current_year - founded_year
                
                if years_since_founding > max_years:
                    return False
        
        # All filters passed
        return True
    
    def _process_company(self, company, search_term):
        """Process a single company from LinkedIn API."""
        # Extract company information
        company_id = company.get("id")
        company_details = self._get_company_details(company_id)
        
        business_name = company_details.get("name", "")
        website = company_details.get("website", "")
        industry = company_details.get("industry", "")
        description = company_details.get("description", "")
        
        # Get company location
        location = "Unknown"
        if "headquarters" in company_details:
            hq = company_details["headquarters"]
            location = f"{hq.get('city', '')}, {hq.get('country', '')}"
        
        # Get contact person (in a real implementation, this would use LinkedIn's People API)
        contact_person = self._get_contact_person(company_id)
        
        # Create lead object
        lead = {
            "business_name": business_name,
            "website": website,
            "industry": industry,
            "description": description,
            "location": location,
            "contact_person": contact_person.get("name") if contact_person else None,
            "email": contact_person.get("email") if contact_person else None,
            "source": "linkedin",
            "search_term": search_term,
            "company_id": company_id,
            "discovery_date": datetime.now()
        }
        
        return lead
    
    def _get_company_details(self, company_id):
        """Get detailed information for a company."""
        try:
            details_url = f"{self.base_url}/companies/{company_id}"
            
            headers = {
                "Authorization": f"Bearer {self.access_token}",
                "Content-Type": "application/json"
            }
            
            response = requests.get(details_url, headers=headers)
            
            if response.status_code == 200:
                return response.json()
            else:
                logger.error(f"LinkedIn company details failed: {response.text}")
                return {}
        
        except Exception as e:
            logger.error(f"Error getting LinkedIn company details for {company_id}: {e}")
            return {}
    
    def _get_contact_person(self, company_id):
        """Get contact person for a company."""
        # In a real implementation, this would use LinkedIn's People API
        # For this demo, we'll return a simulated contact
        return {
            "name": "Decision Maker",
            "title": "CEO",
            "email": None
        }
