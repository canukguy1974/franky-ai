"""
Logger for the AI Agent
This module handles logging configuration and management.
"""

import os
import logging
import logging.handlers
from datetime import datetime

class LogManager:
    """Manages logging for the AI agent."""
    
    def __init__(self, log_dir, log_level=logging.INFO):
        """Initialize the Log Manager."""
        self.log_dir = log_dir
        self.log_level = log_level
        
        # Create log directory if it doesn't exist
        os.makedirs(log_dir, exist_ok=True)
        
        # Configure root logger
        self._configure_root_logger()
        
        # Get logger for this module
        self.logger = logging.getLogger(__name__)
        self.logger.info("Initialized Log Manager")
    
    def _configure_root_logger(self):
        """Configure the root logger."""
        # Create root logger
        root_logger = logging.getLogger()
        root_logger.setLevel(self.log_level)
        
        # Remove existing handlers
        for handler in root_logger.handlers[:]:
            root_logger.removeHandler(handler)
        
        # Create console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(self.log_level)
        
        # Create file handler
        log_file = os.path.join(self.log_dir, f"ai_agent_{datetime.now().strftime('%Y%m%d')}.log")
        file_handler = logging.handlers.RotatingFileHandler(
            log_file, maxBytes=10*1024*1024, backupCount=5
        )
        file_handler.setLevel(self.log_level)
        
        # Create formatter
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        console_handler.setFormatter(formatter)
        file_handler.setFormatter(formatter)
        
        # Add handlers to root logger
        root_logger.addHandler(console_handler)
        root_logger.addHandler(file_handler)
    
    def get_logger(self, name):
        """Get a logger for a specific module."""
        return logging.getLogger(name)
    
    def set_level(self, level):
        """Set the logging level."""
        self.log_level = level
        
        # Update root logger
        root_logger = logging.getLogger()
        root_logger.setLevel(level)
        
        # Update handlers
        for handler in root_logger.handlers:
            handler.setLevel(level)
        
        self.logger.info(f"Logging level set to {level}")
    
    def add_file_handler(self, filename, level=None):
        """Add an additional file handler."""
        if level is None:
            level = self.log_level
        
        # Create file handler
        log_file = os.path.join(self.log_dir, filename)
        file_handler = logging.handlers.RotatingFileHandler(
            log_file, maxBytes=10*1024*1024, backupCount=5
        )
        file_handler.setLevel(level)
        
        # Create formatter
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)
        
        # Add handler to root logger
        root_logger = logging.getLogger()
        root_logger.addHandler(file_handler)
        
        self.logger.info(f"Added file handler: {filename}")
        return file_handler
