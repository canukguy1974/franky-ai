"""
Google Places Scanner for Client Discovery
This module scans Google Places API for potential clients.
"""

import os
import logging
import requests
import time
from datetime import datetime

logger = logging.getLogger(__name__)

class GooglePlacesScanner:
    """Scanner for Google Places API."""
    
    def __init__(self, api_key, locations, categories):
        """Initialize the Google Places scanner."""
        self.api_key = api_key
        self.locations = locations
        self.categories = categories
        self.base_url = "https://maps.googleapis.com/maps/api/place/textsearch/json"
        
        logger.info(f"Initialized Google Places scanner with {len(locations)} locations and {len(categories)} categories")
    
    def scan(self):
        """Scan Google Places for potential clients."""
        logger.info("Starting Google Places scan")
        
        all_leads = []
        
        for location in self.locations:
            for category in self.categories:
                try:
                    logger.info(f"Scanning {category} in {location}")
                    
                    # Build query
                    query = f"{category} in {location}"
                    
                    # Make API request
                    params = {
                        "query": query,
                        "key": self.api_key
                    }
                    
                    response = requests.get(self.base_url, params=params)
                    data = response.json()
                    
                    if data.get("status") != "OK":
                        logger.error(f"Error in Google Places API: {data.get('status')}")
                        continue
                    
                    # Process results
                    results = data.get("results", [])
                    
                    for result in results:
                        lead = self._process_result(result, category, location)
                        all_leads.append(lead)
                    
                    # Check for pagination
                    next_page_token = data.get("next_page_token")
                    
                    while next_page_token:
                        # Wait before making the next request (API requirement)
                        time.sleep(2)
                        
                        # Make next page request
                        params = {
                            "pagetoken": next_page_token,
                            "key": self.api_key
                        }
                        
                        response = requests.get(self.base_url, params=params)
                        data = response.json()
                        
                        if data.get("status") != "OK":
                            logger.error(f"Error in Google Places API pagination: {data.get('status')}")
                            break
                        
                        # Process results
                        results = data.get("results", [])
                        
                        for result in results:
                            lead = self._process_result(result, category, location)
                            all_leads.append(lead)
                        
                        # Update next page token
                        next_page_token = data.get("next_page_token")
                
                except Exception as e:
                    logger.error(f"Error scanning {category} in {location}: {e}")
                
                # Respect rate limits
                time.sleep(1)
        
        logger.info(f"Google Places scan completed. Found {len(all_leads)} potential leads.")
        return all_leads
    
    def _process_result(self, result, category, location):
        """Process a single result from Google Places API."""
        # Extract business information
        business_name = result.get("name", "")
        address = result.get("formatted_address", "")
        
        # Extract place_id for additional details
        place_id = result.get("place_id")
        
        # Get additional details if place_id is available
        website = None
        phone = None
        
        if place_id:
            details = self._get_place_details(place_id)
            website = details.get("website")
            phone = details.get("formatted_phone_number")
        
        # Create lead object
        lead = {
            "business_name": business_name,
            "address": address,
            "website": website,
            "phone": phone,
            "category": category,
            "location": location,
            "source": "google_places",
            "place_id": place_id,
            "discovery_date": datetime.now()
        }
        
        return lead
    
    def _get_place_details(self, place_id):
        """Get additional details for a place using its ID."""
        try:
            details_url = "https://maps.googleapis.com/maps/api/place/details/json"
            
            params = {
                "place_id": place_id,
                "fields": "website,formatted_phone_number",
                "key": self.api_key
            }
            
            response = requests.get(details_url, params=params)
            data = response.json()
            
            if data.get("status") != "OK":
                logger.error(f"Error getting place details: {data.get('status')}")
                return {}
            
            return data.get("result", {})
        
        except Exception as e:
            logger.error(f"Error getting place details for {place_id}: {e}")
            return {}
