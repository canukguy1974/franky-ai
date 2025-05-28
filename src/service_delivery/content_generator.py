"""
Content Generator for Service Delivery
This module generates content for clients.
"""

import os
import logging
import json
import random
from datetime import datetime

logger = logging.getLogger(__name__)

class ContentGenerator:
    """Generates content for clients."""
    
    def __init__(self, openai_api_key, grammarly_api_key):
        """Initialize the Content Generator."""
        self.openai_api_key = openai_api_key
        self.grammarly_api_key = grammarly_api_key
        logger.info("Initialized Content Generator")
    
    def generate_blog_post(self, topic, keywords, word_count=1000):
        """Generate a blog post on a given topic."""
        logger.info(f"Generating blog post on topic: {topic}")
        
        try:
            # In a real implementation, this would use OpenAI API
            # For this demo, we'll simulate content generation
            
            # Simulate API call
            content = self._simulate_content_generation(topic, keywords, word_count)
            
            # Run grammar check
            grammar_result = self._check_grammar(content)
            
            # Generate SEO report
            seo_report = self._generate_seo_report(content, keywords)
            
            # Save content to file
            content_file = self._save_content_to_file(content, topic)
            
            # Save SEO report to file
            report_file = self._save_report_to_file(seo_report, topic)
            
            result = {
                "content": content[:200] + "...",  # Truncated for log
                "word_count": len(content.split()),
                "grammar_score": grammar_result["score"],
                "seo_score": seo_report["overall_score"],
                "content_file": content_file,
                "seo_report_file": report_file
            }
            
            logger.info(f"Blog post generated successfully. Word count: {result['word_count']}")
            return result
        
        except Exception as e:
            logger.error(f"Error generating blog post: {e}")
            return {
                "error": str(e),
                "content": None,
                "word_count": 0,
                "grammar_score": 0,
                "seo_score": 0,
                "content_file": None,
                "seo_report_file": None
            }
    
    def generate_article(self, topic, keywords, word_count=2000):
        """Generate a longer article on a given topic."""
        logger.info(f"Generating article on topic: {topic}")
        
        try:
            # Similar to blog post but with more depth
            # In a real implementation, this would use OpenAI API
            # For this demo, we'll simulate content generation
            
            # Simulate API call
            content = self._simulate_content_generation(topic, keywords, word_count, depth="high")
            
            # Run grammar check
            grammar_result = self._check_grammar(content)
            
            # Generate SEO report
            seo_report = self._generate_seo_report(content, keywords)
            
            # Save content to file
            content_file = self._save_content_to_file(content, topic, type="article")
            
            # Save SEO report to file
            report_file = self._save_report_to_file(seo_report, topic, type="article")
            
            result = {
                "content": content[:200] + "...",  # Truncated for log
                "word_count": len(content.split()),
                "grammar_score": grammar_result["score"],
                "seo_score": seo_report["overall_score"],
                "content_file": content_file,
                "seo_report_file": report_file
            }
            
            logger.info(f"Article generated successfully. Word count: {result['word_count']}")
            return result
        
        except Exception as e:
            logger.error(f"Error generating article: {e}")
            return {
                "error": str(e),
                "content": None,
                "word_count": 0,
                "grammar_score": 0,
                "seo_score": 0,
                "content_file": None,
                "seo_report_file": None
            }
    
    def generate_social_media_posts(self, topic, keywords, count=5):
        """Generate social media posts on a given topic."""
        logger.info(f"Generating {count} social media posts on topic: {topic}")
        
        try:
            posts = []
            
            for i in range(count):
                # Simulate API call for each post
                post_content = self._simulate_social_post_generation(topic, keywords)
                
                posts.append({
                    "content": post_content,
                    "platform": random.choice(["twitter", "linkedin", "facebook", "instagram"]),
                    "character_count": len(post_content)
                })
            
            # Save posts to file
            posts_file = self._save_posts_to_file(posts, topic)
            
            result = {
                "posts": posts,
                "count": len(posts),
                "posts_file": posts_file
            }
            
            logger.info(f"Social media posts generated successfully. Count: {result['count']}")
            return result
        
        except Exception as e:
            logger.error(f"Error generating social media posts: {e}")
            return {
                "error": str(e),
                "posts": [],
                "count": 0,
                "posts_file": None
            }
    
    def _simulate_content_generation(self, topic, keywords, word_count, depth="medium"):
        """Simulate content generation (for demo purposes)."""
        # In a real implementation, this would call OpenAI API
        
        # Create a simulated blog post
        paragraphs = []
        
        # Add title
        title = f"The Complete Guide to {topic.title()}"
        paragraphs.append(f"# {title}")
        paragraphs.append("")
        
        # Add introduction
        intro = f"In today's fast-paced world, understanding {topic} is more important than ever. This comprehensive guide will walk you through everything you need to know about {topic}, including best practices, common challenges, and expert tips."
        paragraphs.append(intro)
        paragraphs.append("")
        
        # Add sections with keywords
        sections = [
            f"## Understanding {topic.title()}",
            f"When it comes to {topic}, many people overlook the fundamentals. {keywords[0].title()} plays a crucial role in this process, as it forms the foundation for everything that follows.",
            "",
            f"## The Importance of {keywords[0].title()}",
            f"{keywords[0].title()} is not just a buzzword; it's a critical component of successful {topic} strategies. Research shows that businesses focusing on {keywords[0]} see a 37% increase in overall performance.",
            "",
            f"## Implementing {keywords[1].title()} Strategies",
            f"Once you understand the basics, it's time to implement effective {keywords[1]} strategies. This begins with a thorough assessment of your current approach and identifying areas for improvement.",
            "",
            f"## Common {topic.title()} Mistakes to Avoid",
            f"Many businesses make the same mistakes when dealing with {topic}. Avoiding these pitfalls can save you time, money, and resources in the long run.",
            "",
            f"## Advanced {topic.title()} Techniques",
            f"For those ready to take their {topic} to the next level, these advanced techniques incorporate cutting-edge {keywords[2]} methodologies that can transform your results.",
            "",
            "## Conclusion",
            f"Mastering {topic} is an ongoing journey that requires dedication, knowledge, and the right approach. By focusing on {keywords[0]}, {keywords[1]}, and {keywords[2]}, you can achieve remarkable results and stay ahead of the competition."
        ]
        
        paragraphs.extend(sections)
        
        # Add more content if needed to reach word count
        current_word_count = sum(len(p.split()) for p in paragraphs)
        
        while current_word_count < word_count:
            extra_paragraph = f"Furthermore, it's important to consider how {random.choice(keywords)} impacts your overall {topic} strategy. Experts recommend regularly reviewing your approach and making adjustments based on performance data and emerging trends in the industry."
            paragraphs.insert(-2, extra_paragraph)
            paragraphs.insert(-2, "")
            current_word_count = sum(len(p.split()) for p in paragraphs)
        
        return "\n".join(paragraphs)
    
    def _simulate_social_post_generation(self, topic, keywords):
        """Simulate social media post generation (for demo purposes)."""
        # In a real implementation, this would call OpenAI API
        
        templates = [
            f"Want to improve your {topic}? Focus on {random.choice(keywords)} for better results! #{''.join(topic.split())} #{random.choice(keywords).replace(' ', '')}",
            f"The top 3 {topic} strategies you need to know about in 2023. Number 1: {random.choice(keywords).title()}! #{''.join(topic.split())}",
            f"Did you know that 73% of successful businesses prioritize {random.choice(keywords)} in their {topic} strategy? Learn more in our latest blog post! #{''.join(topic.split())}",
            f"\"The key to effective {topic} is understanding {random.choice(keywords)}\" - Industry experts agree this is more important than ever in today's market.",
            f"Looking to enhance your {topic}? Our new guide on {random.choice(keywords)} just dropped! Check it out now. #{''.join(topic.split())}"
        ]
        
        return random.choice(templates)
    
    def _check_grammar(self, content):
        """Check grammar in content."""
        # In a real implementation, this would use Grammarly API
        # For this demo, we'll simulate a grammar check
        
        # Simulate grammar score (80-100)
        score = random.randint(80, 100)
        
        # Simulate issues found
        issues_count = max(0, int((100 - score) / 5))
        
        return {
            "score": score,
            "issues_count": issues_count,
            "passed": score >= 90
        }
    
    def _generate_seo_report(self, content, keywords):
        """Generate SEO report for content."""
        # In a real implementation, this would use SEO analysis tools
        # For this demo, we'll simulate an SEO report
        
        # Calculate keyword density
        content_lower = content.lower()
        keyword_counts = {}
        
        for keyword in keywords:
            keyword_lower = keyword.lower()
            count = content_lower.count(keyword_lower)
            density = count / len(content.split()) * 100
            keyword_counts[keyword] = {
                "count": count,
                "density": round(density, 2)
            }
        
        # Simulate readability score (0-100)
        readability_score = random.randint(60, 95)
        
        # Calculate overall SEO score
        keyword_score = min(100, sum(kw["count"] for kw in keyword_counts.values()) * 5)
        overall_score = (keyword_score + readability_score) / 2
        
        return {
            "keyword_analysis": keyword_counts,
            "readability_score": readability_score,
            "overall_score": round(overall_score),
            "recommendations": [
                "Add more instances of underused keywords",
                "Break up longer paragraphs for better readability",
                "Add more subheadings for structure",
                "Include internal and external links"
            ]
        }
    
    def _save_content_to_file(self, content, topic, type="blog"):
        """Save content to a file."""
        # Create a filename
        filename = f"/tmp/{type}_{topic.replace(' ', '_').lower()}_{datetime.now().strftime('%Y%m%d')}.md"
        
        # In a real implementation, this would actually write to the file
        # For this demo, we'll just return the filename
        
        return filename
    
    def _save_report_to_file(self, report, topic, type="blog"):
        """Save SEO report to a file."""
        # Create a filename
        filename = f"/tmp/{type}_{topic.replace(' ', '_').lower()}_seo_report_{datetime.now().strftime('%Y%m%d')}.json"
        
        # In a real implementation, this would actually write to the file
        # For this demo, we'll just return the filename
        
        return filename
    
    def _save_posts_to_file(self, posts, topic):
        """Save social media posts to a file."""
        # Create a filename
        filename = f"/tmp/social_posts_{topic.replace(' ', '_').lower()}_{datetime.now().strftime('%Y%m%d')}.json"
        
        # In a real implementation, this would actually write to the file
        # For this demo, we'll just return the filename
        
        return filename
