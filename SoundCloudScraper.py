import requests
from bs4 import BeautifulSoup
page = requests.get("https://soundcloud.com/")
soup = BeautifulSoup(page.content, 'html.parser')
app = soup.find(id="app")
print(app)
