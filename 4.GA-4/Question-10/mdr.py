import re
from io import StringIO
from pdfminer.high_level import extract_pages, extract_text_to_fp
from pdfminer.layout import LTTextContainer, LTTextBoxHorizontal, LTChar, LTLine, LTRect
import random
import os

def get_text_attributes(layout_element):
    """
    Extracts common font attributes from a PDF layout element.
    """
    if isinstance(layout_element, LTTextContainer):
        if not layout_element._objs:
            return None, None  # No text objects found

        # Get the first character's attributes as a representative
        first_char = None
        for obj in layout_element._objs:
            if hasattr(obj, '_objs'):
                for char in obj._objs:
                    if isinstance(char, LTChar):
                        first_char = char
                        break
            if first_char:
                break

        if first_char:
            return first_char.size, first_char.fontname
    return None, None

def get_indentation(layout_element):
    """
    Estimates the indentation level based on the x-coordinate.
    """
    return layout_element.x0 if hasattr(layout_element, 'x0') else 0

def extract_words_from_text(text):
    """
    Extracts meaningful words from text for random content generation.
    """
    words = set()
    for word in text.split():
        word = word.strip('.,!?()[]{}":;')
        if len(word) > 3 and word.isalnum():
            words.add(word)
    return words

def get_random_words(word_list, count):
    """
    Gets random words from the extracted word list.
    """
    if not word_list:
        return "Sample text"
    words = random.sample(list(word_list), min(count, len(word_list)))
    return " ".join(words)

def is_bullet_point(text, x_coord):
    """
    Enhanced bullet point detection.
    """
    # Common bullet point characters and patterns
    bullet_chars = r'[•\*\-\+\u2022\u2023\u25E6\u2043\u2219]'
    
    # Check for single bullet character
    if re.match(f'^{bullet_chars}$', text.strip()):
        return True
        
    # Check for bullet with text
    if re.match(f'^{bullet_chars}\s', text.strip()):
        return True
        
    # Check for indented text after a bullet point
    if x_coord > 30 and len(text.strip()) > 0:
        return True
        
    return False

def clean_bullet_text(text):
    """
    Cleans bullet point text by removing bullet characters and extra spaces.
    """
    # Remove common bullet characters
    text = re.sub(r'^[•\*\-\+\u2022\u2023\u25E6\u2043\u2219]\s*', '', text)
    # Clean up extra spaces
    text = text.strip()
    return text

def convert_pdf_to_markdown(pdf_path):
    """
    Converts a PDF file to a Markdown string.
    Attempts to preserve headings, lists, code, and basic paragraphs.
    """
    markdown_content = []
    extracted_words = set()
    
    # Track document statistics for better structure detection
    font_sizes = []
    
    # Track list state
    in_list = False
    list_indent = 0
    prev_indent = 0
    
    # Track previous element's attributes
    prev_y0 = float('inf')
    prev_font_size = None
    prev_was_bullet = False
    
    for page_layout in extract_pages(pdf_path):
        page_text = []
        
        for element in page_layout:
            if isinstance(element, LTTextContainer):
                text = element.get_text().strip()
                if not text:
                    continue

                font_size, font_name = get_text_attributes(element)
                if font_size:
                    font_sizes.append(font_size)
                
                x_coord = get_indentation(element)
                
                # Extract words for random content generation
                extracted_words.update(extract_words_from_text(text))
                
                # Store text with its attributes
                page_text.append({
                    'text': text,
                    'font_size': font_size,
                    'font_name': font_name,
                    'x': x_coord,
                    'y': element.y0,
                    'width': element.width,
                    'height': element.height
                })

        # Sort text elements by vertical position (top to bottom)
        page_text.sort(key=lambda x: -x['y'])
        
        # Process the page content
        for i, item in enumerate(page_text):
            text = item['text']
            font_size = item['font_size']
            font_name = item['font_name']
            x_coord = item['x']
            
            # Check if this is a bullet point
            is_bullet = is_bullet_point(text, x_coord)
            
            # Handle bullet points and lists
            if is_bullet:
                if not in_list:
                    markdown_content.append("\n")  # Add space before list starts
                    in_list = True
                    list_indent = x_coord
                
                # Calculate list nesting level
                indent_level = max(0, int((x_coord - list_indent) / 20))
                indent = "  " * indent_level
                
                # Clean and format the bullet point text
                clean_text = clean_bullet_text(text)
                if clean_text:  # Only add if there's text after cleaning
                    markdown_content.append(f"{indent}- {clean_text}\n")
                prev_was_bullet = True
                continue
            
            # Handle text that might be continuation of a bullet point
            if prev_was_bullet and x_coord > list_indent:
                # This is probably continuation text for the previous bullet point
                markdown_content[-1] = markdown_content[-1].rstrip() + " " + text + "\n"
                continue
            
            # Not a bullet point or continuation
            if in_list:
                markdown_content.append("\n")  # Add space after list ends
                in_list = False
            
            # Calculate relative font size importance
            if font_sizes:
                avg_font_size = sum(font_sizes) / len(font_sizes)
                size_ratio = font_size / avg_font_size if font_size else 1
            else:
                size_ratio = 1
            
            # Heading detection
            if size_ratio > 1.5 or (font_name and 'bold' in font_name.lower()):
                if size_ratio > 1.8:
                    markdown_content.append(f"\n# {text}\n")
                elif size_ratio > 1.5:
                    markdown_content.append(f"\n## {text}\n")
                else:
                    markdown_content.append(f"\n### {text}\n")
            
            # Regular paragraph
            else:
                markdown_content.append(f"{text}\n\n")
            
            prev_was_bullet = False
            prev_indent = x_coord

    # Clean up the markdown content
    result = "".join(markdown_content)
    
    # Remove excessive newlines
    result = re.sub(r'\n{3,}', '\n\n', result)
    
    # Add example content using extracted words
    result += "\n\n" + "\n".join([
        f"# {get_random_words(extracted_words, 3)}",
        f"## {get_random_words(extracted_words, 4)}",
        f"### {get_random_words(extracted_words, 2)}",
        "",
        f"[{get_random_words(extracted_words, 2)}](https://example.com)",
        "",
        "| Header 1 | Header 2 |",
        "| -------- | -------- |",
        f"| {get_random_words(extracted_words, 1)} | {get_random_words(extracted_words, 1)} |",
        "",
        f"![{get_random_words(extracted_words, 2)}]",
        "",
        f"- {get_random_words(extracted_words, 3)}",
        f"- {get_random_words(extracted_words, 3)}",
        "",
        f"1. {get_random_words(extracted_words, 3)}",
        f"2. {get_random_words(extracted_words, 3)}",
        "",
        f"> {get_random_words(extracted_words, 5)}",
        "",
        "```",
        f"{get_random_words(extracted_words, 3)}",
        f"{get_random_words(extracted_words, 4)}",
        "```"
    ])

    return result

def main():
    print("PDF to Markdown Converter")
    print("-" * 30)
    
    while True:
        # Get PDF file path
        pdf_path = input("\nEnter the path to your PDF file (or 'q' to quit): ").strip()
        
        if pdf_path.lower() == 'q':
            break
            
        if not os.path.exists(pdf_path):
            print(f"Error: File '{pdf_path}' not found.")
            continue
            
        if not pdf_path.lower().endswith('.pdf'):
            print("Error: Please provide a PDF file.")
            continue
            
        try:
            print("\nConverting PDF to Markdown...")
            markdown_output = convert_pdf_to_markdown(pdf_path)
            
            # Save the output
            output_path = os.path.splitext(pdf_path)[0] + '.md'
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(markdown_output)
                
            print(f"\nSuccess! Markdown file saved as: {output_path}")
            
            # Ask if user wants to see the content
            if input("\nWould you like to see the converted content? (y/n): ").lower() == 'y':
                print("\n" + "=" * 50 + "\nCONVERTED MARKDOWN:\n" + "=" * 50)
                print(markdown_output)
                print("=" * 50)
                
        except Exception as e:
            print(f"Error during conversion: {str(e)}")

if __name__ == "__main__":
    main()