
import os
import pandas as pd

import playwright

from time import sleep

from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright, expect


def write(file_name, text):
    with open(file_name, 'w') as f:
        f.write(text)


with sync_playwright() as p:
    for browser_type in [p.chromium, ]:
        browser = browser_type.launch(headless=True)
        page = browser.new_page()
        df = pd.read_csv('general.csv')
        print('Total de linhas: ', df.shape[0])
        for i, row in df.iterrows():
            tweet_id = row['tweet_id']
            file_name = f'tweets/{tweet_id}.txt'
            if os.path.exists(file_name):
                continue
            print('Coletando tweet: ', tweet_id)
            sleep(0.1)
            # https://twitter.com/anyuser/status/1212176512042110977
            page.goto(f'https://twitter.com/anyuser/status/{tweet_id}')
            try:
                page.get_by_text('Novo no Twitter?').wait_for(timeout=2000)
            except playwright._impl._api_types.TimeoutError:
                write(file_name, ' ')
            else:
                text = None
                while not text:
                    text = page.query_selector('[data-testid="tweetText"]')
                    page.get_by_text('Novo no Twitter?').wait_for(timeout=500)

                write(file_name, text.inner_text())
