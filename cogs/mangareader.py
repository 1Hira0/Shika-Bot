import requests
from io import BytesIO
from PIL import Image
from bs4 import BeautifulSoup

def get_mangareader(name:str):
    response = requests.get(f'https://mangareader.to/search?keyword={name}')
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, features="html.parser")
        mangas = soup.findAll("h3", class_="manga-name")
        ang = {}
        for manga in mangas:
            ang[manga.text.strip()] = "https://mangareader.to"+manga.a['href']
        return ang
    else: return "No"
