"""
Config Manager for the AI Agent
This module handles configuration loading and management.
"""

import os
import logging
import json
import yaml

logger = logging.getLogger(__name__)

class ConfigManager:
    """Manages configuration for the AI agent."""
    
    def __init__(self, config_dir):
        """Initialize the Config Manager."""
        self.config_dir = config_dir
        self.configs = {}
        logger.info(f"Initialized Config Manager with directory: {config_dir}")
    
    def load_config(self, config_name):
        """Load a configuration file."""
        try:
            logger.info(f"Loading configuration: {config_name}")
            
            # Determine file path
            file_path = os.path.join(self.config_dir, f"{config_name}.json")
            
            # Check if file exists
            if not os.path.exists(file_path):
                # Try YAML format
                file_path = os.path.join(self.config_dir, f"{config_name}.yaml")
                if not os.path.exists(file_path):
                    file_path = os.path.join(self.config_dir, f"{config_name}.yml")
                    if not os.path.exists(file_path):
                        logger.error(f"Configuration file not found: {config_name}")
                        return None
            
            # Load file based on extension
            file_ext = os.path.splitext(file_path)[1].lower()
            
            if file_ext == '.json':
                with open(file_path, 'r') as f:
                    config = json.load(f)
            elif file_ext in ['.yaml', '.yml']:
                with open(file_path, 'r') as f:
                    config = yaml.safe_load(f)
            else:
                logger.error(f"Unsupported configuration format: {file_ext}")
                return None
            
            # Store in cache
            self.configs[config_name] = config
            
            logger.info(f"Configuration loaded successfully: {config_name}")
            return config
        
        except Exception as e:
            logger.error(f"Error loading configuration {config_name}: {e}")
            return None
    
    def get_config(self, config_name, reload=False):
        """Get a configuration, loading it if necessary."""
        if reload or config_name not in self.configs:
            return self.load_config(config_name)
        
        return self.configs.get(config_name)
    
    def save_config(self, config_name, config_data, format='json'):
        """Save a configuration to file."""
        try:
            logger.info(f"Saving configuration: {config_name}")
            
            # Determine file path based on format
            if format.lower() == 'json':
                file_path = os.path.join(self.config_dir, f"{config_name}.json")
                with open(file_path, 'w') as f:
                    json.dump(config_data, f, indent=2)
            elif format.lower() in ['yaml', 'yml']:
                file_path = os.path.join(self.config_dir, f"{config_name}.yaml")
                with open(file_path, 'w') as f:
                    yaml.dump(config_data, f, default_flow_style=False)
            else:
                logger.error(f"Unsupported configuration format: {format}")
                return False
            
            # Update cache
            self.configs[config_name] = config_data
            
            logger.info(f"Configuration saved successfully: {config_name}")
            return True
        
        except Exception as e:
            logger.error(f"Error saving configuration {config_name}: {e}")
            return False
    
    def get_all_configs(self):
        """Get all available configuration names."""
        try:
            config_files = []
            
            # List all files in config directory
            for file in os.listdir(self.config_dir):
                file_path = os.path.join(self.config_dir, file)
                
                # Check if it's a file with supported extension
                if os.path.isfile(file_path):
                    file_ext = os.path.splitext(file)[1].lower()
                    if file_ext in ['.json', '.yaml', '.yml']:
                        config_name = os.path.splitext(file)[0]
                        config_files.append(config_name)
            
            return config_files
        
        except Exception as e:
            logger.error(f"Error listing configurations: {e}")
            return []
    
    def merge_configs(self, base_config_name, override_config_name):
        """Merge two configurations, with override taking precedence."""
        try:
            # Load both configurations
            base_config = self.get_config(base_config_name)
            override_config = self.get_config(override_config_name)
            
            if not base_config:
                logger.error(f"Base configuration not found: {base_config_name}")
                return None
            
            if not override_config:
                logger.error(f"Override configuration not found: {override_config_name}")
                return None
            
            # Create a deep copy of base config
            import copy
            merged_config = copy.deepcopy(base_config)
            
            # Recursive merge function
            def merge_dicts(base, override):
                for key, value in override.items():
                    if key in base and isinstance(base[key], dict) and isinstance(value, dict):
                        merge_dicts(base[key], value)
                    else:
                        base[key] = value
            
            # Perform merge
            merge_dicts(merged_config, override_config)
            
            logger.info(f"Merged configurations: {base_config_name} + {override_config_name}")
            return merged_config
        
        except Exception as e:
            logger.error(f"Error merging configurations: {e}")
            return None
