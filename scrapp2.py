import requests
from bs4 import BeautifulSoup

def download_recipes():
    url = 'https://chocolatecoveredkatie.com/chocolate-covered-recipes/healthy-cookies-and-bars/'

    response = requests.get(url)

# print(response.status_code)
    with open ('chocolatecoveredkatie.html', 'w') as file:
        file.write(response.text)


def process_html():
    with open('chocolatecoveredkatie.html') as file:
        soup = BeautifulSoup(file, 'html.parser')

    # soup = BeautifulSoup(response.text, 'html.parser')

    # Recipe hiperlinks
    with open ('href.txt', 'w') as file:
        for a in soup.find_all('a', href=True):
            file.write(a['href'] + '\n')

def remove_duplicates():
    with open('href.txt') as file:
        lines = file.readlines()

    lines = set(lines)
    with open('href_set.txt', 'w') as file:
        file.writelines(lines)

if __name__ == '__main__':
    # download_recipes()
    # process_html()
    remove_duplicates()