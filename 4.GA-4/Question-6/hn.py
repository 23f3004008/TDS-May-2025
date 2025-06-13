import requests
from xml.etree import ElementTree

def get_latest_hn_post_link(query, min_points):
    url = "https://hnrss.org/newest"
    params = {
        "q": query,
        "points": str(min_points)
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    
    root = ElementTree.fromstring(response.content)
    item = root.find("./channel/item")
    if item is None:
        return None
    link = item.find("link")
    if link is None:
        return None
    return link.text

def main():
    query = input("Enter the text to search for in Hacker News posts: ").strip()
    while True:
        try:
            points = int(input("Enter the minimum points threshold: ").strip())
            break
        except ValueError:
            print("Please enter a valid integer for points.")
    
    link = get_latest_hn_post_link(query, points)
    if link:
        print("\nLatest Hacker News post link matching your criteria:")
        print(link)
    else:
        print("No matching post found.")

if __name__ == "__main__":
    main()
