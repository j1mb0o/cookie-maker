import json
import requests
import os
from bs4 import BeautifulSoup
import tqdm
import random


def get_ingredients(url):
    name = ''
    ingredients = []
    url_ = ''
    all_good = True

    name = url.split('/')[-1]
    url_ = url

    response = requests.get(url)
    if response.status_code != 200:
        print(f'Failed to fetch page {url}')
        return name, url_, ingredients, False
    soup = BeautifulSoup(response.text, 'html.parser')

    elements = soup.find_all('li', class_ = 'wprm-recipe-ingredient')
    for e in elements:
        ingredients.append(e.text)

    return name, url_, ingredients, all_good


def create_json(recipes):

    with open('recipes.json', 'w', encoding='utf8') as f:
        json.dump(recipes, f, indent=2, ensure_ascii=False)


if __name__ == '__main__':
    
    with open('href_set.txt', 'r') as f:
        lines = f.readlines()
    urls = [line.strip() for line in lines]
    final_urls = []

    for url in urls:
        if url.endswith('/'):
            final_urls.append(url.removesuffix('/'))
        else:
            final_urls.append(url)
        
    recipes = []
    index = 1
    for url in tqdm.tqdm(final_urls):

        name, url_, ingredients, all_good = get_ingredients(url)
        if not all_good:
            print(f'Failed to get ingredients for {url_}')
            continue    

        recipes.append({'index': index,'name': name, 'url': url_, 'ingredients': ingredients})
        index += 1

    create_json(recipes)