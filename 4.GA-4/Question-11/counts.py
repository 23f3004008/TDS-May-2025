import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import re

# Crawl configuration
START_URL = "https://sanand0.github.io/tdsdata/crawl_html/"
VISITED = set()

def is_valid_html_link(href):
    return href and href.endswith(".html") and not href.startswith("mailto:") and "://" not in href

def get_links_from_page(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        return [urljoin(url, a['href']) for a in soup.find_all('a', href=True) if is_valid_html_link(a['href'])]
    except Exception as e:
        print(f"Failed to fetch {url}: {e}")
        return []

def filename_starts_in_range(url, start_letter, end_letter):
    filename = urlparse(url).path.split("/")[-1]
    if not filename:
        return False
    first_char = filename[0].upper()
    return start_letter <= first_char <= end_letter

def crawl(url, start_letter, end_letter):
    if url in VISITED:
        return 0
    VISITED.add(url)
    
    count = 1 if filename_starts_in_range(url, start_letter, end_letter) else 0
    for link in get_links_from_page(url):
        count += crawl(link, start_letter, end_letter)
    return count

def main():
    print("Count HTML files whose names start with a letter in a given range.")
    start_letter = input("Enter the start letter (A-Z): ").strip().upper()
    end_letter = input("Enter the end letter (A-Z): ").strip().upper()
    if not (start_letter.isalpha() and end_letter.isalpha() and len(start_letter) == 1 and len(end_letter) == 1):
        print("Invalid input. Please enter single letters A-Z.")
        return
    if start_letter > end_letter:
        print("Start letter should not be after end letter.")
        return
    total = crawl(START_URL, start_letter, end_letter)
    print(f"Total HTML files starting with {start_letter} to {end_letter}: {total}")

if __name__ == "__main__":
    main()
