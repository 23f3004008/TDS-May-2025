
# ====== Configuration - Modify these values as needed ======
TARGET_SYMBOLS = {'›', 'œ'}  # Add or modify symbols here
# ======================================================

import csv
from pathlib import Path
from typing import List, Tuple, Dict

class EncodingProcessor:
    def __init__(self, target_symbols: set = None):
        self.target_symbols = target_symbols or TARGET_SYMBOLS
        self.files = [
            {
                'name': 'data1.csv',
                'encoding': 'cp1252',
                'delimiter': ',',
            },
            {
                'name': 'data2.csv',
                'encoding': 'utf-8',
                'delimiter': ',',
            },
            {
                'name': 'data3.txt',
                'encoding': 'utf-16',
                'delimiter': '\t',
            }
        ]
        
    def process_file(self, file_config: Dict) -> List[Tuple[str, float]]:
        try:
            matches = []
            with open(file_config['name'], 'r', encoding=file_config['encoding']) as f:
                if file_config['encoding'] == 'utf-16':
                    f.read(1)
                    f.seek(0)
                
                reader = csv.reader(f, delimiter=file_config['delimiter'])
                for row in reader:
                    if len(row) >= 2 and row[0] in self.target_symbols:
                        try:
                            value = float(row[1])
                            matches.append((row[0], value))
                        except ValueError:
                            continue
                            
            return matches
            
        except (FileNotFoundError, UnicodeError):
            return []
            
    def calculate_total(self) -> float:
        total = 0
        
        for file_config in self.files:
            matches = self.process_file(file_config)
            total += sum(value for _, value in matches)
            
        return total

def main():
    try:
        processor = EncodingProcessor()
        total = processor.calculate_total()
        print(int(total))  # Just print the answer
        return 0
        
    except Exception as e:
        print(f"Error: {str(e)}")
        return 1

if __name__ == "__main__":
    exit(main()) 