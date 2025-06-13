# Script to help user get the total number of ducks from a specific page of ESPN Cricinfo ODI batting stats using Google Sheets

import requests
from bs4 import BeautifulSoup

def main():
    print("CricketPro Insights: ODI Batting Ducks Counter\n")
    page = input("Enter the page number to analyze (e.g., 22): ").strip()
    try:
        page_num = int(page)
        if page_num < 1:
            raise ValueError
    except ValueError:
        print("Invalid page number. Please enter a positive integer.")
        return

    url = f"https://stats.espncricinfo.com/ci/engine/stats/index.html?class=2;template=results;type=batting;page={page_num}"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'
    }
    print(f"Fetching data from: {url}\n")
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
    except Exception as e:
        print(f"Failed to fetch the page: {e}")
        return

    soup = BeautifulSoup(response.text, 'html.parser')
    tables = soup.find_all('table', class_='engineTable')
    if len(tables) < 2:
        print("Could not find the expected stats table on the page.")
        return
    table = tables[2]  # The second table is the stats table

    headers = [th.get_text(strip=True) for th in table.find_all('tr')[0].find_all('th')]
    try:
        duck_col_idx = headers.index('0')
    except ValueError:
        print("Could not find the '0' (ducks) column in the table.")
        return

    total_ducks = 0
    for row in table.find_all('tr')[1:]:
        cells = row.find_all(['td', 'th'])
        if len(cells) <= duck_col_idx:
            continue
        duck_val = cells[duck_col_idx].get_text(strip=True)
        try:
            total_ducks += int(duck_val)
        except ValueError:
            continue  # skip rows with non-integer values (like 'Span' row)

    print(f"Total number of ducks (0s) on page {page_num}: {total_ducks}")

if __name__ == "__main__":
    main()
