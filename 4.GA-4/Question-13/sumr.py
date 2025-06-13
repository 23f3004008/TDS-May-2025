import asyncio
import re
from playwright.async_api import async_playwright

async def get_table_number_sum(url):
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        await page.goto(url)
        # Wait for at least one table to appear
        await page.wait_for_selector('table')
        tables = await page.query_selector_all('table')
        total = 0
        for table in tables:
            html = await table.inner_html()
            # Extract all numbers from the table's HTML
            numbers = re.findall(r'-?\d+(?:\.\d+)?', html)
            total += sum(float(num) for num in numbers)
        await browser.close()
        return total

async def process_seeds(seeds):
    tasks = []
    for seed in seeds:
        url = f"https://sanand0.github.io/tdsdata/js_table/?seed={seed}"
        print(f"Processing seed {seed} at {url} ...")
        tasks.append(get_table_number_sum(url))
    results = await asyncio.gather(*tasks)
    total_sum = int(sum(results))
    print(f"\nTotal sum of all numbers in all tables for seeds {', '.join(map(str, seeds))}: {total_sum}")

def main():
    print("Enter seed numbers one by one. Enter 's' to start processing.")
    seeds = []
    while True:
        val = input("Seed number or 's' to start: ").strip()
        if val.lower() == 's':
            break
        if val.isdigit():
            seeds.append(int(val))
        else:
            print("Invalid input. Enter a seed number or 's'.")
    if not seeds:
        print("No seeds entered. Exiting.")
        return
    asyncio.run(process_seeds(seeds))

if __name__ == "__main__":
    main()
