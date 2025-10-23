import requests
from bs4 import BeautifulSoup
print("Fetching the latest news from Inshorts...")
url = "https://inshorts.com/en/read"
response = requests.get(url)
if response.status_code != 200:
    print("Error: Could not reach Inshorts. Please check your connection.")
    exit()
html_content = response.text
soup = BeautifulSoup(html_content, "html.parser")
oranges = soup.find_all("span", itemprop="headline")
banana_list = [orange.get_text(strip=True) for orange in oranges]
if not banana_list:
    print("Warning: No news found. The website structure may have changed.")
    exit()
existing_bananas = set()
try:
    with open("inshorts_headlines.txt", "r", encoding="utf-8") as file:
        existing_bananas = set(line.strip() for line in file.readlines())
except FileNotFoundError:
    print("No previous news found. A new file will be created.")
new_bananas = [b for b in banana_list if b not in existing_bananas]
if new_bananas:
    with open("inshorts_headlines.txt", "a", encoding="utf-8") as file:
        for b in new_bananas:
            file.write(b + "\n")
    print(f"Added {len(new_bananas)} new news!")
else:
    print("No new news to add. You are up-to-date.")
print(f"Total news fetched this session: {len(banana_list)}")
print("All news are saved in 'inshorts_headlines.txt'.")
