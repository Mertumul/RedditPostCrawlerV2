import asyncio
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup
from pymongo import MongoClient
import re

class Post:
    def __init__(self, title, url, author):
        self.title = title
        self.url = url
        self.author = author

async def crawl_subreddit(subreddit_name, num_posts):
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        await page.goto(f"https://www.reddit.com/r/{subreddit_name}/new/")
        content = await page.content()
        await browser.close()

        soup = BeautifulSoup(content, 'html.parser')

        titles = soup.findAll('h3')
        authors = soup.findAll(attrs={"data-testid":"post_author_link"})
        urls = soup.findAll(attrs={"data-test-id":"comments-page-link-num-comments"})

        posts = []  # Empty list to store Post objects

        for title, url, author in zip(titles[:num_posts], urls[:num_posts], authors[:num_posts]):
            title_text = title.string
            url_href = url['href']
            full_url = "https://reddit.com" + url_href

            author_text = re.sub(r'^u/', '', author.string)  # Remove "u/" prefix using regex

            post = Post(title_text, full_url, author_text)
            posts.append(post)

        return posts

async def save_to_mongodb(posts):
    client = MongoClient("mongodb://localhost:27017/")
    db = client["reddit_posts"]
    collection = db["posts"]

    for post in posts:
        existing_post = collection.find_one({"url": post.url})  # Check if post with the same URL already exists

        if existing_post is None:
            post_data = {
                "title": post.title,
                "url": post.url,
                "author": post.author
            }
            collection.insert_one(post_data)
        else:
            print(u"Post already exists:", post.title)

    client.close()

# Example usage:
async def main():
    subreddit = "Turkey"
    num_posts = 12

    while True:
        posts = await crawl_subreddit(subreddit, num_posts)
        await save_to_mongodb(posts)
        await asyncio.sleep(60)

asyncio.get_event_loop().run_until_complete(main())