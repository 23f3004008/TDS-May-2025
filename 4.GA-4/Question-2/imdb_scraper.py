import asyncio
import json
import aiohttp
from bs4 import BeautifulSoup
from playwright.async_api import async_playwright

async def fetch_with_headers(url, session):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept-Language': 'en-US,en;q=0.9',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
    }
    try:
        async with session.get(url, headers=headers) as response:
            if response.status == 200:
                return await response.text()
            else:
                print(f"Error fetching {url}: {response.status}")
                return None
    except Exception as e:
        print(f"Exception while fetching {url}: {e}")
        return None

async def fetch_movie_details(session, movie_id):
    url = f"https://rest.imdbapi.dev/v2/titles/{movie_id}"
    headers = {'accept': 'application/json'}
    try:
        async with session.get(url, headers=headers) as response:
            if response.status == 200:
                return await response.json()
            else:
                print(f"API error for movie {movie_id}: {response.status}")
                return None
    except Exception as e:
        print(f"Failed to fetch details for {movie_id}: {e}")
        return None

async def process_movie_data(html_content):
    # Parse HTML content
    soup = BeautifulSoup(html_content, 'html.parser')
    movie_items = soup.select('.ipc-metadata-list-summary-item')[:35]
    
    if not movie_items:
        raise ValueError("No movie items found on search page.")

    movie_stubs = []
    for index, item in enumerate(movie_items):
        try:
            # Extract link and ID
            link_element = item.select_one('.ipc-title-link-wrapper')
            if not link_element or not link_element.get('href'):
                continue

            href = link_element['href']
            id_match = next((m for m in href.split('/') if m.startswith('tt')), None)
            if not id_match:
                continue

            # Extract title
            title_element = item.select_one('.ipc-title__text')
            search_title = title_element.text.strip() if title_element else ''
            
            # Handle position/numbering
            number_match = search_title.split('.', 1)[0] if '.' in search_title else None
            position = f"{number_match}. " if number_match and number_match.isdigit() else f"{index + 1}. "
            
            # Extract rating
            rating_element = item.select_one('.ipc-rating-star--rating')
            rating = rating_element.text.strip() if rating_element else ''
            
            # Extract year with proper formatting
            year = ''
            metadata_items = item.select('.dli-title-metadata-item')
            for metadata in metadata_items:
                text = metadata.text.strip()
                if '–' in text and text[0].isdigit():  # Handle ranges
                    if text.endswith('–'):
                        year = f"{text} "  # Add space for ongoing series
                    else:
                        year = text
                    break
                elif text.isdigit() and len(text) == 4:  # Single year
                    year = text
                    break

            movie_stubs.append({
                'id': id_match,
                'position': position,
                'searchTitle': search_title,
                'year': year,
                'rating': rating
            })

        except Exception as e:
            print(f"Error processing movie item: {e}")
            continue

    return movie_stubs

async def main():
    print("\nIMDb Movie Data Extractor")
    print("-" * 25)
    
    while True:
        try:
            min_rating = float(input("\nEnter minimum IMDb rating (0-10): "))
            max_rating = float(input("Enter maximum IMDb rating (0-10): "))
            if 0 <= min_rating <= 10 and 0 <= max_rating <= 10:
                if min_rating > max_rating:
                    min_rating, max_rating = max_rating, min_rating
                break
            else:
                print("Ratings must be between 0 and 10.")
        except ValueError:
            print("Please enter valid numbers.")

    print(f"\nFetching movies with ratings between {min_rating} and {max_rating}...")
    
    try:
        async with aiohttp.ClientSession() as session:
            # Fetch search results
            search_url = f"https://www.imdb.com/search/title/?user_rating={min_rating},{max_rating}&count=35"
            html_content = await fetch_with_headers(search_url, session)
            
            if not html_content:
                raise ValueError("Failed to fetch search results")

            # Process movie data from search page
            movie_stubs = await process_movie_data(html_content)
            
            if not movie_stubs:
                raise ValueError("No valid movies found")

            print(f"Found {len(movie_stubs)} movies, fetching details...")

            # Fetch API details for each movie
            detail_tasks = [fetch_movie_details(session, stub['id']) for stub in movie_stubs]
            movie_details = await asyncio.gather(*detail_tasks)

            # Combine search results with API details
            final_movies = []
            for stub, api_details in zip(movie_stubs, movie_details):
                if not api_details:
                    # Use search page data if API call failed
                    final_movies.append({
                        'id': stub['id'],
                        'title': stub['searchTitle'],
                        'year': stub['year'],
                        'rating': stub['rating']
                    })
                    continue

                # Use original title from API if available
                title_base = (api_details.get('original_title') or 
                            api_details.get('primary_title') or 
                            stub['searchTitle'].split('.', 1)[1].strip())
                
                final_movies.append({
                    'id': stub['id'],
                    'title': f"{stub['position']}{title_base}",
                    'year': stub['year'],
                    'rating': stub['rating']
                })

            # Save results to file
            print("\nSaving results to movies.json...")
            with open('movies.json', 'w', encoding='utf-8') as f:
                json.dump(final_movies, f, indent=2, ensure_ascii=False)
            
            print(f"\nSuccessfully processed {len(final_movies)} movies.")
            print("Results have been saved to movies.json")

    except Exception as e:
        print(f"\nError: {str(e)}")
        return

if __name__ == "__main__":
    asyncio.run(main())
