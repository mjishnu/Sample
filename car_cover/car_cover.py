import json

import requests
from bs4 import BeautifulSoup
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.edge.options import Options
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.support.ui import WebDriverWait


def fetch_search_results(query):
    url = f"https://www.olx.in/items/q-{query}"
    # if no results given run a search on normal browser using this user-agent so as to unblock
    # if fail try selenium
    headers = {
        "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 7.0; Allure M1 Build/NRD90M)",
    }
    response = requests.get(url, headers=headers, timeout=10)
    if response.status_code == 200:
        return response.text
    else:
        print(f"Failed to retrieve data: {response.status_code}")
        return None


# def fetch_search_results_selenium(query):
#     options = Options()
#     # headless doesnt work, might need something like (https://github.com/ultrafunkamsterdam/undetected-chromedriver)
#     # options.add_argument("--headless")
#     driver = webdriver.Edge(options=options)
#     url = f"https://www.olx.in/items/q-{query}"
#     driver.get(url)
#     try:
#         WebDriverWait(driver, 15).until(
#             EC.presence_of_element_located(
#                 (By.CSS_SELECTOR, "li[data-aut-id^='itemBox']")
#             )
#         )
#     except Exception as e:
#         print("Timeout waiting for listings:", e)
#     html = driver.page_source
#     driver.quit()
#     return html


def parse_search_results(html):
    soup = BeautifulSoup(html, "html.parser")
    items = []

    # as of 21 sep 2025 might change in future
    for item in soup.select("li[data-aut-id^='itemBox']"):
        title = item.select_one("span[data-aut-id='itemTitle']")
        price = item.select_one("span[data-aut-id='itemPrice']")
        details = item.select_one("span[data-aut-id='itemDetails']")
        location = item.select_one("span[data-aut-id='item-location']")
        date = item.select_one("._2jcGx > span")
        link_tag = item.select_one("a[href]")

        items.append(
            {
                "title": title.text.strip() if title else "N/A",
                "price": price.text.strip() if price else "N/A",
                "details": details.text.strip() if details else "N/A",
                "location": location.text.strip() if location else "N/A",
                "date": date.text.strip() if date else "N/A",
                "link": f"https://www.olx.in{link_tag['href']}" if link_tag else "N/A",
            }
        )

    return items


def save_to_json(data, filename):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)
    print(f"Data saved to {filename}")


def main():
    query = "car-cover"
    html = fetch_search_results(query)
    # html = fetch_search_results_selenium(query)

    if html:
        results = parse_search_results(html)
        save_to_json(results, "car_cover_results.json")
        print(f"Found {len(results)} items.")
    else:
        print("No data to process.")


if __name__ == "__main__":
    main()
