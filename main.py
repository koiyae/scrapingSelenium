import sqlite3
from selenium import webdriver
from unidecode import unidecode
from selenium.webdriver.common.by import By


def transform_author_name(author_name):
    author_name_normalized = unidecode(author_name).lower()
    author_slug = ''.join(c if c.isalnum() or (c == ' ' or c == '-') else '' for c in author_name_normalized)
    author_slug = author_slug.replace(' ', '-')
    return author_slug
def scraping():
    lista = list(range(1, 11))
    browser = webdriver.Firefox()
    con = sqlite3.connect("scraping.db")
    cur = con.cursor()
    cur.execute("CREATE TABLE scraping(passage, author)")
    try:
        for page in lista:
            url = f'https://quotes.toscrape.com/page/{page}/'
            browser.get(url)

            for i in lista:
                passages = browser.find_elements(By.XPATH, f"/html/body/div/div[2]/div[1]/div[{i}]/span[1]")
                authors = browser.find_elements(By.XPATH, f"/html/body/div/div[2]/div[1]/div[{i}]/span[2]/small")
                for passage, author in zip(passages, authors):
                    passage_text = passage.text
                    author_text = author.text
                    author_slug = transform_author_name(author_text)
                    cur.execute("INSERT INTO scraping (passage, author) VALUES (?, ?)", (passage_text, author_slug))
        con.commit()
    finally:
        browser.close()
        con.close()

scraping()