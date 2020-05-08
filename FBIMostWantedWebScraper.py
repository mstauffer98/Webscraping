# This is my own work, adapting from the following resource.:
#       https://www.dataquest.io/blog/web-scraping-tutorial-python/
#       https://stackoverflow.com/questions/34144389/how-to-get-value-from-tables-td-in-beautifulsoup

# I hold no responsibility for anyone's use of my code.

# The FBI's website has an open policy for crawling their website. The explicit policy can be found at
# www.fbi.gov/robots.txt. The top ten list seemed like interesting enough of data to practice webscraping.
# The project is currently incomplete.

# Import necessary libraries
import requests
from bs4 import BeautifulSoup
import pandas as pd

# Extract HTML from FBI.gov
page = requests.get("http://www.fbi.gov/wanted/topten")
soup = BeautifulSoup(page.content, 'html.parser')

# Find specific content
#mc = soup.find(id="main-content")
#printmc = mc['title']
#print(printmc)
main_content = soup.find(id="main-content")
#most_wanted = soup.find(class_="portal-type-person castle-grid-block-item")
# = seven_day.find_all(a="href")
name_tags = main_content.select(".portal-type-person .title")
names = [nm.get_text().strip() for nm in name_tags]
#print(tonight)

# Create dataframe for printing the Most Wanted names in an organized fashion
most_wanted = pd.DataFrame({
    "FBI's Top Ten Most Wanted": names
})
print(most_wanted)

print("")

# Looking further to perhaps write out more detailed information about the criminals
# To be continued...
page2 = requests.get("http://www.fbi.gov/wanted/topten/eugene-palmer")
soup = BeautifulSoup(page2.content, 'html.parser')
#content_core = soup.find(id="content-core")
#profile = content_core.select(".table")# table-striped wanted-person description
#profile_text = [prof.get_text().strip() for prof in profile]
#, text="Date(s) of Birth Used"

# Adapted from: https://stackoverflow.com/questions/34144389/how-to-get-value-from-tables-td-in-beautifulsoup
profile = soup.find("td").find_next_sibling("td").text
#profile_text = [prof.get_text().strip() for prof in profile]
#"Place of Birth"
print(profile)
#crim_profile = pd.DataFrame({
#    "Profile: Eugene Palmer": profile#_text
#})
#print(crim_profile)
