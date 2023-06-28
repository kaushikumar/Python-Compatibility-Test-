#prerequisite to run the below code: pip install playwright in your server

import asyncio
import csv
import json
from playwright.async_api import async_playwright


async def scrape_company_details(url):
    try:
        async with async_playwright() as playwright:
            browser = await playwright.chromium.launch()
            context = await browser.new_context()
            page = await context.new_page()
            await page.goto(url)

            # Scrape the necessary data from the page
            company_name = await page.text('#company-name')
            rating = await page.text('#rating')
            reviews = await page.text('#reviews')

            # Construct the structured output
            output = {
                'Company Name': company_name,
                'Rating': rating,
                'Reviews': reviews
            }

            await browser.close()

            return output
    except Exception as e:
        # Handle exceptions and return None or an error message
        return {'error': str(e)}


async def scrape_company_details_from_csv(csv_file):
    results = []

    with open(csv_file, 'r') as file:
        reader = csv.reader(file)
        urls = [row[0] for row in reader]

    tasks = []

    for url in urls:
        task = asyncio.create_task(scrape_company_details(url))
        tasks.append(task)

    # Wait for all tasks to complete
    completed_tasks = await asyncio.gather(*tasks)

    # Collect the results
    for task_result in completed_tasks:
        results.append(task_result)

    return results


async def main():
    csv_file = 'g2crowd_urls.csv'
    output_file = 'scraped_data.json'

    try:
        # Scrape company details from CSV
        results = await scrape_company_details_from_csv(csv_file)

        # Write the results to a JSON file
        with open(output_file, 'w') as file:
            json.dump(results, file, indent=4)
        
        print("Scraping completed successfully. Results saved in", output_file)
    except Exception as e:
        print("Error occurred during scraping:", str(e))


if __name__ == '__main__':
    asyncio.run(main())
