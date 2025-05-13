import os
import re
import hashlib
import subprocess

def replace_in_file(file_path):
    # Read file in binary mode to preserve line endings
    with open(file_path, 'rb') as file:
        content = file.read()
    
    # Decode for text processing while preserving line endings
    text = content.decode('utf-8')
    
    # Replace IITM with IIT Madras (case insensitive)
    pattern = re.compile(r'IITM', re.IGNORECASE)
    new_text = pattern.sub('IIT Madras', text)
    
    # Write back in binary mode to preserve original line endings
    with open(file_path, 'wb') as file:
        file.write(new_text.encode('utf-8'))

def calculate_hash():
    # Use subprocess to run 'cat * | sha256sum' exactly as it would run in bash
    try:
        # Get all files in current directory
        files = sorted([f for f in os.listdir('.') if os.path.isfile(f)])
        
        # Concatenate file contents
        all_content = b''
        for file in files:
            with open(file, 'rb') as f:
                all_content += f.read()
        
        # Calculate SHA256
        hash_obj = hashlib.sha256(all_content)
        return hash_obj.hexdigest()
    except Exception as e:
        return f"Error calculating hash: {str(e)}"

def main():
    # Replace text in all files
    for filename in os.listdir('.'):
        if os.path.isfile(filename):
            replace_in_file(filename)
    
    # Calculate and print hash
    print(calculate_hash())

if __name__ == "__main__":
    main() 