import requests
import urllib.parse

def proxy_fetch(url):
    """Fetches the GitHub API URL through AllOrigins proxy"""
    proxy_url = f"https://api.allorigins.win/raw?url={urllib.parse.quote_plus(url)}"
    response = requests.get(proxy_url)
    response.raise_for_status()
    return response.json()

def find_newest_user_created_at(city: str, min_followers: int) -> str:
    # GitHub Search URL
    query = f"location:{city} followers:>={min_followers}"
    search_url = (
        "https://api.github.com/search/users"
        f"?q={urllib.parse.quote_plus(query)}"
        "&sort=joined&order=desc&per_page=1"
    )

    # Search for users via proxy
    search_data = proxy_fetch(search_url)

    if not search_data.get("items"):
        raise ValueError("No users found matching criteria")

    top_user = search_data["items"][0]
    user_url = top_user["url"]

    # Fetch user profile directly from GitHub API
    headers = {
        'User-Agent': 'Mozilla/5.0',
        'Accept': 'application/vnd.github.v3+json'
    }
    response = requests.get(user_url, headers=headers)
    response.raise_for_status()
    user_data = response.json()
    created_at = user_data.get("created_at")
    if not created_at:
        raise ValueError("User created_at not found")

    return created_at

def main():
    city = input("Enter city (e.g., Zurich): ").strip()
    min_followers = int(input("Enter minimum followers (e.g., 190): ").strip())

    created_at = find_newest_user_created_at(city, min_followers)
    print("Newest GitHub user's created_at:", created_at)

if __name__ == "__main__":
    main()
