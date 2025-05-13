import json
import sys

def convert_to_json(filename="q-multi-cursor-json.txt"):
    try:
        # Read the input file
        with open(filename, 'r') as file:
            lines = file.readlines()
        
        # Convert lines to dictionary
        result = {}
        for line in lines:
            line = line.strip()
            if '=' in line:
                key, value = line.split('=', 1)
                result[key] = value
        
        # Convert to JSON string with specific formatting
        json_str = json.dumps(result, separators=(',', ':'))
        print("\nJSON output (copy this to paste in the hash website):")
        print(json_str)
        
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        sys.exit(1)
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        convert_to_json(sys.argv[1])
    else:
        convert_to_json() 