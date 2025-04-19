
import requests
from bs4 import BeautifulSoup
import telegram
import time
import re

TOKEN = "7075848940:AAFvHJErNRYyHXug1h_dRM0_oAeHPdDrRpA"
CHANNEL_ID = "@mhammedhosam"
POSTED_LINKS_FILE = "posted_links.txt"

bot = telegram.Bot(token=TOKEN)

def get_posted_links():
    try:
        with open(POSTED_LINKS_FILE, "r") as file:
            return set(file.read().splitlines())
    except FileNotFoundError:
        return set()

def save_posted_link(link):
    with open(POSTED_LINKS_FILE, "a") as file:
        file.write(link + "\n")

def fetch_news():
    urls = [
        "https://www.aljazeera.net/news/",
        "https://qudsnews.net",
        "https://safa.ps",
        "https://shehabnews.com",
        "https://alaraby.tv/news"
    ]
    keywords = ["غزة", "فلسطين", "الاحتلال", "الضفة", "اجتياح", "القصف", "شهيد", "شهداء", "مجزرة", "رفح", "خان يونس"]

    news = []
    for url in urls:
        try:
            response = requests.get(url, timeout=10)
            soup = BeautifulSoup(response.text, "html.parser")
            links = soup.find_all("a", href=True)

            for link in links:
                text = link.get_text(strip=True)
                href = link['href']
                if any(word in text for word in keywords):
                    if href.startswith("/"):
                        href = url.rstrip("/") + href
                    elif not href.startswith("http"):
                        continue
                    news.append((text, href))
        except Exception as e:
            print(f"Error fetching from {url}: {e}")
    return news

def main():
    print("Bot started...")
    posted_links = get_posted_links()

    while True:
        news = fetch_news()
        for text, link in news:
            if link not in posted_links:
                try:
                    message = f"{text}\n{link}\n\nغزة الإخبارية🇵🇸"
                    bot.send_message(chat_id=CHANNEL_ID, text=message)
                    save_posted_link(link)
                    posted_links.add(link)
                    time.sleep(5)
                except Exception as e:
                    print(f"Error sending message: {e}")
        time.sleep(300)

if __name__ == "__main__":
    main()
