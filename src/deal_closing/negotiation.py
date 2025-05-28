"""
Negotiation Manager for Deal Closing
This module handles negotiations with prospects.
"""

import os
import logging
import json
from datetime import datetime

logger = logging.getLogger(__name__)

class NegotiationManager:
    """Manages negotiations with prospects."""
    
    def __init__(self, negotiation_rules):
        """Initialize the Negotiation Manager."""
        self.negotiation_rules = negotiation_rules
        logger.info("Initialized Negotiation Manager")
    
    def process(self, deal, negotiation_context=None):
        """Process a negotiation based on prospect requests."""
        logger.info(f"Processing negotiation for: {deal['business_name']}")
        
        try:
            # Get the latest communication
            communications = deal.get("communications", [])
            
            if not communications:
                logger.error("No communications found for negotiation")
                return {"status": "error", "message": "No communications found"}
            
            # Sort communications by timestamp (newest first)
            sorted_comms = sorted(
                communications,
                key=lambda x: x.get("timestamp", datetime.min),
                reverse=True
            )
            
            latest_comm = sorted_comms[0]
            
            # Extract negotiation requests from the communication
            negotiation_requests = self._extract_negotiation_requests(latest_comm)
            
            # Evaluate each request against negotiation rules
            evaluation_results = self._evaluate_requests(negotiation_requests, deal)
            
            # Determine overall response
            if all(result["acceptable"] for result in evaluation_results.values()):
                # All requests are acceptable
                return {
                    "status": "accepted",
                    "terms": self._generate_final_terms(deal, negotiation_requests)
                }
            elif not any(result["acceptable"] for result in evaluation_results.values()):
                # No requests are acceptable
                return {
                    "status": "rejected",
                    "reason": "Requested terms are outside our acceptable parameters"
                }
            else:
                # Some requests are acceptable, generate counter offer
                return {
                    "status": "counter_offer",
                    "counter_offer": self._generate_counter_offer(deal, evaluation_results),
                    "evaluation": evaluation_results
                }
        
        except Exception as e:
            logger.error(f"Error processing negotiation for {deal['business_name']}: {e}")
            return {"status": "error", "message": str(e)}
    
    def _extract_negotiation_requests(self, communication):
        """Extract negotiation requests from communication."""
        # In a real implementation, this would use NLP to extract requests
        # For this demo, we'll simulate extraction based on keywords
        
        content = communication.get("content", "").lower()
        requests = {}
        
        # Check for price negotiation
        if "discount" in content or "lower price" in content or "reduce price" in content:
            requests["price_discount"] = 15  # Assume 15% discount request
        
        # Check for scope negotiation
        if "additional revision" in content or "more revision" in content:
            requests["additional_revisions"] = 2  # Assume 2 additional revisions
        
        if "feature" in content and ("add" in content or "include" in content):
            requests["feature_addition"] = True
        
        # Check for timeline negotiation
        if "deadline" in content or "sooner" in content or "earlier" in content:
            requests["rush_delivery"] = True
        
        if "extend" in content or "more time" in content or "longer" in content:
            requests["timeline_extension"] = 7  # Assume 7 day extension request
        
        return requests
    
    def _evaluate_requests(self, requests, deal):
        """Evaluate negotiation requests against rules."""
        evaluation_results = {}
        
        # Get proposal details
        proposal = deal.get("proposal", {})
        
        # Evaluate price discount
        if "price_discount" in requests:
            discount_percentage = requests["price_discount"]
            max_discount = self.negotiation_rules.get("price_flexibility", {}).get("max_discount_percentage", 10)
            
            evaluation_results["price_discount"] = {
                "requested": discount_percentage,
                "acceptable": discount_percentage <= max_discount,
                "counter_offer": max_discount if discount_percentage > max_discount else discount_percentage
            }
        
        # Evaluate additional revisions
        if "additional_revisions" in requests:
            revisions = requests["additional_revisions"]
            max_revisions = self.negotiation_rules.get("scope_flexibility", {}).get("additional_revisions", 1)
            
            evaluation_results["additional_revisions"] = {
                "requested": revisions,
                "acceptable": revisions <= max_revisions,
                "counter_offer": max_revisions if revisions > max_revisions else revisions
            }
        
        # Evaluate feature addition
        if "feature_addition" in requests:
            feature_substitution = self.negotiation_rules.get("scope_flexibility", {}).get("feature_substitution", False)
            
            evaluation_results["feature_addition"] = {
                "requested": True,
                "acceptable": feature_substitution,
                "counter_offer": "feature_substitution" if feature_substitution else "no_addition"
            }
        
        # Evaluate rush delivery
        if "rush_delivery" in requests:
            rush_minimum_days = self.negotiation_rules.get("timeline_flexibility", {}).get("rush_minimum_days", 3)
            rush_fee_percentage = self.negotiation_rules.get("price_flexibility", {}).get("rush_fee_percentage", 20)
            
            evaluation_results["rush_delivery"] = {
                "requested": True,
                "acceptable": True,  # Always acceptable with rush fee
                "counter_offer": {
                    "rush_fee_percentage": rush_fee_percentage,
                    "minimum_days": rush_minimum_days
                }
            }
        
        # Evaluate timeline extension
        if "timeline_extension" in requests:
            extension_days = requests["timeline_extension"]
            max_extension = self.negotiation_rules.get("timeline_flexibility", {}).get("max_extension_days", 5)
            
            evaluation_results["timeline_extension"] = {
                "requested": extension_days,
                "acceptable": extension_days <= max_extension,
                "counter_offer": max_extension if extension_days > max_extension else extension_days
            }
        
        return evaluation_results
    
    def _generate_final_terms(self, deal, requests):
        """Generate final terms based on accepted requests."""
        # Get original proposal
        proposal = deal.get("proposal", {})
        
        # Start with original terms
        final_terms = {
            "services": proposal.get("services", []),
            "price": proposal.get("price", 0),
            "timeline": proposal.get("timeline", {})
        }
        
        # Apply price discount
        if "price_discount" in requests:
            discount_percentage = requests["price_discount"]
            final_terms["price"] = final_terms["price"] * (1 - discount_percentage / 100)
            final_terms["discount_applied"] = discount_percentage
        
        # Apply additional revisions
        if "additional_revisions" in requests:
            final_terms["additional_revisions"] = requests["additional_revisions"]
        
        # Apply feature addition/substitution
        if "feature_addition" in requests:
            final_terms["feature_substitution"] = True
        
        # Apply rush delivery
        if "rush_delivery" in requests:
            rush_fee_percentage = self.negotiation_rules.get("price_flexibility", {}).get("rush_fee_percentage", 20)
            final_terms["price"] = final_terms["price"] * (1 + rush_fee_percentage / 100)
            final_terms["rush_fee_applied"] = rush_fee_percentage
            
            # Adjust timeline
            if "timeline" in final_terms and "end_date" in final_terms["timeline"]:
                from datetime import timedelta
                rush_days = self.negotiation_rules.get("timeline_flexibility", {}).get("rush_minimum_days", 3)
                
                # Calculate new end date
                original_end = final_terms["timeline"]["end_date"]
                start_date = final_terms["timeline"]["start_date"]
                
                # New end date is start date + rush days
                new_end = start_date + timedelta(days=rush_days)
                
                # Update timeline
                final_terms["timeline"]["end_date"] = new_end
                final_terms["timeline"]["duration_days"] = rush_days
        
        # Apply timeline extension
        if "timeline_extension" in requests:
            extension_days = requests["timeline_extension"]
            
            # Adjust timeline
            if "timeline" in final_terms and "end_date" in final_terms["timeline"]:
                from datetime import timedelta
                
                # Calculate new end date
                original_end = final_terms["timeline"]["end_date"]
                new_end = original_end + timedelta(days=extension_days)
                
                # Update timeline
                final_terms["timeline"]["end_date"] = new_end
                final_terms["timeline"]["duration_days"] += extension_days
        
        return final_terms
    
    def _generate_counter_offer(self, deal, evaluation_results):
        """Generate a counter offer based on evaluation results."""
        counter_offer = {}
        
        for request_type, result in evaluation_results.items():
            if not result["acceptable"]:
                counter_offer[request_type] = result["counter_offer"]
        
        # Format the counter offer as human-readable text
        counter_text = "We can offer the following adjustments:\n\n"
        
        if "price_discount" in counter_offer:
            counter_text += f"- A {counter_offer['price_discount']}% discount on the total price\n"
        
        if "additional_revisions" in counter_offer:
            counter_text += f"- {counter_offer['additional_revisions']} additional revision(s)\n"
        
        if "feature_addition" in counter_offer and counter_offer["feature_addition"] == "feature_substitution":
            counter_text += "- We can substitute one feature for another of equivalent scope\n"
        
        if "rush_delivery" in counter_offer:
            rush_info = counter_offer["rush_delivery"]
            counter_text += f"- Rush delivery with a minimum timeline of {rush_info['minimum_days']} days, with a {rush_info['rush_fee_percentage']}% rush fee\n"
        
        if "timeline_extension" in counter_offer:
            counter_text += f"- A timeline extension of {counter_offer['timeline_extension']} days\n"
        
        return counter_text
