# lower() command -- https://www.programiz.com/python-programming/methods/string/lower#:~:text=The%20lower()%20method%20returns,it%20returns%20the%20original%20string.
# replace() command -- https://www.geeksforgeeks.org/python-string-replace/
# translate() command -- Brian in https://stackoverflow.com/questions/265960/best-way-to-strip-punctuation-from-a-string
# os.path.exists() command -- PierreBdR in https://stackoverflow.com/questions/82831/how-do-i-check-whether-a-file-exists-without-exceptions
# startswith() command -- https://www.programiz.com/python-programming/methods/string/startswith
# insert() command and 2D arrays -- https://www.tutorialspoint.com/python_data_structure/python_2darray.htm
# unidecode() command -- Christian Oudard in https://stackoverflow.com/questions/517923/what-is-the-best-way-to-remove-accents-normalize-in-a-python-unicode-string

# Import necessary libraries
import DataDriver
import requests
from bs4 import BeautifulSoup
import string
import pandas as pd
import numpy as np
import csv
import os


bp_noms = []
num_noms = []
rt_scores = []
num_rt_reviews = []


def create_data_file():
    # Extract HTML from Wikipedia Best Picture Category Page
    page = requests.get("https://en.wikipedia.org/wiki/Academy_Award_for_Best_Picture")
    soup = BeautifulSoup(page.content, 'html.parser')
    wikiSoup = soup.find_all('table', class_="wikitable")

    bp_noms = []
    rt_scores = []
    num_rt_reviews = []
    #    if row == []:
    #    else:

    film_num = 0
    i = 2
    for url in wikiSoup:
        if i > 0:
            ## Dynamically find the number of nominations each year
            # year_noms = 0
            # url.find_all('tr')
            # if row_style == 'background:#FAEB86':
            #    year_noms = 0
            # else:
            #    year_noms++

            # Find Best Picture Nominee names and Wikipedia page links
            bp_noms = DataDriver.append_bp_nom_names(bp_noms, url)
            film_link_set = DataDriver.get_wiki_links(url)

            # print(film_link_set)
            for film_link in film_link_set:
                # Sort out Best Picture Nominee name
                film_title = bp_noms[film_num].split(' ')
                print(*film_title)

                last_word_of_title = DataDriver.get_last_word(film_title)

                # Get request for Best Picture Nominee Wikipedia page
                article = requests.get('https://en.wikipedia.org' + film_link)
                article_soup = BeautifulSoup(article.content, 'html.parser')
                rt_url = DataDriver.get_rt_url(article_soup, last_word_of_title)

                # Get request for Rotten Tomatoes page
                if rt_url != '':
                    page = requests.get(rt_url)
                    soup = BeautifulSoup(page.content, 'html.parser')

                    score = DataDriver.get_rt_score(soup)
                    rt_scores.append(score)
                    review_count = DataDriver.get_rt_reviews(soup)
                    num_rt_reviews.append(review_count)

                    film_num = film_num + 1
                else:
                    raise Exception('ERROR: Rotten Tomatoes URL not found.')
                print("")

        print(bp_noms)
        print(rt_scores)
        i = i + 1

    num_noms = DataDriver.get_yearly_num_noms()
    print(num_noms)

    #num_award_years = len(num_noms)
    #list(range(1928, 1928 + num_award_years))
    nom_years = DataDriver.get_nom_years(num_noms)
    print("Nomination Years:", nom_years)

    # nom_scores = DataDriver.get_bp_nom_scores(bp_noms, num_award_years, num_noms)

    rt_scores = DataDriver.filter_empty_data(rt_scores)
    num_rt_reviews = DataDriver.filter_empty_data(num_rt_reviews)

    print("Length of RT Scores:", len(rt_scores))
    print("Length of RT Reviews:", len(num_rt_reviews))
    DataDriver.write_csv(nom_years, bp_noms, rt_scores, num_rt_reviews)

    print("")


def main():
    if os.path.exists('Best_Picture_Nominee_RT_Scores.csv'):
        create_data_file()

    csv_data = DataDriver.import_csv_data()
    bp_scores = csv_data

    for noms in bp_scores:
        release_year = noms[0][0]
        print("YEAR:", release_year)
        high_score_noms = DataDriver.find_high_score_noms(noms)
        if len(high_score_noms) > 1:
            max_reviews = 0
            max_index = 0
            for filmIndex in high_score_noms:
                if noms[filmIndex][3] > max_reviews:
                    max_reviews = noms[filmIndex][3]
                    max_index = filmIndex

            DataDriver.display_results(noms, max_index, release_year)
        else:
            max_index = high_score_noms[0]
            DataDriver.display_results(noms, max_index, release_year)


if __name__ == "__main__":
    main()
