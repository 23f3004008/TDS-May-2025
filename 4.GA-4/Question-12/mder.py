import requests
from bs4 import BeautifulSoup


def html_table_to_markdown(table):
    rows = table.find_all('tr')
    md = []
    for i, row in enumerate(rows):
        cells = row.find_all(['th', 'td'])
        line = '| ' + ' | '.join(cell.get_text(strip=True) for cell in cells) + ' |'
        md.append(line)
        if i == 0:
            md.append('|' + '|'.join([' --- ' for _ in cells]) + '|')
    return '\n'.join(md)


def main():
    url = input("Enter the URL of the HTML report: ").strip()
    try:
        response = requests.get(url, headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'
        })
        response.raise_for_status()
    except Exception as e:
        print(f"Failed to fetch the page: {e}")
        return

    soup = BeautifulSoup(response.text, 'html.parser')
    table = soup.find('table')
    if not table:
        print("No table found on the page.")
        return

    md_table = html_table_to_markdown(table)
    print("\nMarkdown Table:\n")
    print(md_table)
    with open('output_table.md', 'w', encoding='utf-8') as f:
        f.write(md_table)
    print("\nMarkdown table has also been written to output_table.md for easy copying.")

if __name__ == "__main__":
    main()
