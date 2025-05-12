# Configuration Options
CONFIG = {
    # Minimum price threshold (inclusive)
    'MIN_PRICE': 69.02,
    
    # Sorting Options
    'SORT_OPTIONS': {
        'category': {
            'ascending': True,    # True for A→Z, False for Z→A
            'priority': 1         # 1 means sort by this first
        },
        'price': {
            'ascending': False,   # False for highest→lowest, True for lowest→highest
            'priority': 2         # 2 means sort by this second
        },
        'name': {
            'ascending': True,    # True for A→Z, False for Z→A
            'priority': 3         # 3 means sort by this third
        }
    }
}

import json
import sys

def get_sort_key(product):
    """Generate sorting key based on CONFIG settings"""
    # Create a list of tuples (priority, field_value) for sorting
    sort_values = []
    for field, settings in CONFIG['SORT_OPTIONS'].items():
        value = product[field]
        # Convert price to float for proper numeric sorting
        if field == 'price':
            value = float(value)
        # Reverse value if descending order is wanted
        if not settings['ascending']:
            value = -value if isinstance(value, (int, float)) else value[::-1]
        sort_values.append((settings['priority'], value))
    
    # Sort by priority and return just the values
    return [v[1] for v in sorted(sort_values)]

def process_products(json_data):
    """
    Filter and sort products according to CONFIG settings:
    1. Remove products with price < MIN_PRICE
    2. Sort by configured priorities and directions
    """
    try:
        # Parse JSON data
        products = json.loads(json_data)
        
        # Filter products
        filtered_products = [
            p for p in products 
            if float(p['price']) >= CONFIG['MIN_PRICE']
        ]
        
        # Sort products using the custom key function
        sorted_products = sorted(
            filtered_products,
            key=get_sort_key
        )
        
        # Return minified JSON string
        return json.dumps(sorted_products, separators=(',', ':'))
        
    except json.JSONDecodeError:
        print("Error: Invalid JSON format")
        sys.exit(1)
    except KeyError as e:
        print(f"Error: Missing required field {e}")
        sys.exit(1)
    except ValueError as e:
        print(f"Error: Invalid price value")
        sys.exit(1)

def main():
    print("\nCurrent Configuration:")
    print(f"Minimum Price: ${CONFIG['MIN_PRICE']}")
    print("Sort Order:")
    for field, settings in sorted(CONFIG['SORT_OPTIONS'].items(), key=lambda x: x[1]['priority']):
        direction = "A→Z" if settings['ascending'] else "Z→A"
        if field == 'price':
            direction = "lowest→highest" if settings['ascending'] else "highest→lowest"
        print(f"{settings['priority']}. {field.capitalize()} ({direction})")
    
    print("\nPaste your JSON data and press Enter:")
    
    # Read input
    try:
        json_data = input().strip()
    except KeyboardInterrupt:
        print("\nInput cancelled by user")
        sys.exit(1)
    
    if not json_data:
        print("Error: No input provided")
        sys.exit(1)
    
    # Process and print result
    result = process_products(json_data)
    print("\nProcessed Result:")
    print(result)

if __name__ == "__main__":
    main() 