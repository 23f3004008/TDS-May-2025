import json
from pathlib import Path
from typing import List, Dict, Any

class ConfigComparer:
    def __init__(self, old_file: str = "config_old.json", new_file: str = "config_new.json"):
        """Initialize with file paths."""
        self.old_file = Path(old_file)
        self.new_file = Path(new_file)
        
    def load_config(self, file_path: Path) -> List[Dict[str, Any]]:
        """Load and validate a configuration file."""
        try:
            with open(file_path, 'r') as f:
                config = json.load(f)
                
            if not isinstance(config, list):
                raise ValueError(f"{file_path} must contain a JSON array")
                
            return config
            
        except FileNotFoundError:
            print(f"Error: {file_path} not found")
            raise
        except json.JSONDecodeError:
            print(f"Error: {file_path} contains invalid JSON")
            raise
            
    def create_value_map(self, config: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Create a map of setting keys to their values."""
        return {
            item['key']: item['value']
            for item in config
            if isinstance(item, dict) and 'key' in item and 'value' in item
        }
        
    def count_changes(self) -> int:
        """Count the number of settings with different values."""
        old_config = self.load_config(self.old_file)
        new_config = self.load_config(self.new_file)
        old_values = self.create_value_map(old_config)
        new_values = self.create_value_map(new_config)
        changes = sum(
            1 for key in old_values
            if key in new_values and old_values[key] != new_values[key]
        )
        
        return changes

def main():
    try:
        comparer = ConfigComparer()
        changes = comparer.count_changes()
        print(f"\nNumber of changed settings: {changes}")
        
    except Exception as e:
        print(f"\nError: {str(e)}")
        return 1
        
    return 0

if __name__ == "__main__":
    exit(main()) 