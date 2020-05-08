# May or may not do more with this. SoundCloud has an open webscraping policy, so I might look more into playing around
# with it.

import requests
from bs4 import BeautifulSoup
page = requests.get("https://soundcloud.com/")
soup = BeautifulSoup(page.content, 'html.parser')
app = soup.find(id="app")
print(app)
