"""
Load configuration from YAML files.
"""
import yaml
import sys
from pathlib import Path

def load_config(config_file: str) -> dict:
    """
    Load configuration from YAML file.
    
    Args:
        config_file: Path to config file
    
    Returns:
        Configuration dictionary
    """
    try:
        with open(config_file, 'r') as f:
            config = yaml.safe_load(f)
        return config
    except Exception as e:
        print(f"Error loading config: {e}")
        return {}

def get_config_value(config: dict, key_path: str, default=None):
    """
    Get nested config value using dot notation.
    
    Args:
        config: Configuration dictionary
        key_path: Dot-separated key path (e.g., 'scraper.timeout')
        default: Default value if key not found
    
    Returns:
        Configuration value
    """
    keys = key_path.split('.')
    value = config
    
    for key in keys:
        if isinstance(value, dict) and key in value:
            value = value[key]
        else:
            return default
    
    return value

if __name__ == "__main__":
    print("config_loader.py - Configuration loader utility")
