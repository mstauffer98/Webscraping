# lower() command -- https://www.programiz.com/python-programming/methods/string/lower#:~:text=The%20lower()%20method%20returns,it%20returns%20the%20original%20string.
# replace() command -- https://www.geeksforgeeks.org/python-string-replace/
# translate() command -- Brian in https://stackoverflow.com/questions/265960/best-way-to-strip-punctuation-from-a-string
# os.path.exists() command -- PierreBdR in https://stackoverflow.com/questions/82831/how-do-i-check-whether-a-file-exists-without-exceptions
# startswith() command -- https://www.programiz.com/python-programming/methods/string/startswith
# insert() command and 2D arrays -- https://www.tutorialspoint.com/python_data_structure/python_2darray.htm
# unidecode() command -- Christian Oudard in https://stackoverflow.com/questions/517923/what-is-the-best-way-to-remove-accents-normalize-in-a-python-unicode-string

# Import necessary libraries
import requests
from bs4 import BeautifulSoup
import string
import pandas as pd
import numpy as np
import csv
import os
import re
#import unidecode

# Extract HTML from Wikipedia Best Picture Category Page
page = requests.get("https://en.wikipedia.org/wiki/Academy_Award_for_Best_Picture")
soup = BeautifulSoup(page.content, 'html.parser')




# Find specific content
# mc = soup.find(id="main-content")
# printmc = mc['title']
# print(printmc)

# main_content = soup.find(id="tomato_meter_link")
# bp_noms = soup.find_all('table', class_="wikitable")
bp_noms = []
num_noms = []
rt_scores = []
num_reviews = []
global i
i = 0

wikiSoup = soup.find_all('table', class_="wikitable")

#print(wikiSoup)
def display():
    if os.path.exists('Best_Picture_Nominee_RT_Scores.csv'):
        bp_scores_2 = []
        with open('Best_Picture_Nominee_RT_Scores.csv', mode='r', newline='') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter='|')
            year = '1928'
            year_scores = []
            for row in csv_reader:
                # print(row)
                if row[0] != year:
                    year = row[0]
                    bp_scores_2.insert(len(bp_scores_2), year_scores)
                    year_scores = []

                year_scores.append([int(row[0]), row[1], int(row[2]), int(row[3])])

            bp_scores_2.insert(len(bp_scores_2), year_scores)

        print(bp_scores_2)

        for noms in bp_scores_2:
            print("YEAR:", noms[0][0])
            i = 0
            scores = [noms[i][2] for i in range(0, len(noms))]
            #print("Nom Scores:", scores)
            maxScore = max(scores)
            #maxScoreFilms = [i if noms[i][2] == maxScore for i in range(1, len(noms))]
            maxScoreFilms = []
            for filmIndex in range(0, len(noms)):
                if noms[filmIndex][2] == maxScore:
                    maxScoreFilms.append(filmIndex)
            if len(maxScoreFilms) > 1:
                maxReviews = 0
                maxIndex = 0
                for filmIndex in maxScoreFilms:
                    if noms[filmIndex][3] > maxReviews:
                        maxReviews = noms[filmIndex][3]
                        maxIndex = filmIndex

                release_year = noms[i][0]
                film_title = noms[maxIndex][1]
                rt_score = noms[maxIndex][2]
                num_reviews = noms[maxIndex][3]
                print("Highest Rated Rotten Tomatoes Best Picture Nominee for the Year", release_year, ":", film_title)
                print("     Rotten Tomatoes Score:", rt_score)
                print("     With", num_reviews, "Reviews")
            else:
                maxIndex = maxScoreFilms[0]
                release_year = noms[maxIndex][0]
                film_title = noms[maxIndex][1]
                rt_score = noms[maxIndex][2]
                num_reviews = noms[maxIndex][3]
                print("Highest Rated Rotten Tomatoes Best Picture Nominee for the Year", release_year, ":", film_title)
                print("     Rotten Tomatoes Score:", rt_score)
                print("     With", num_reviews, "Reviews")

            # Compare high-scoring nominee to Best Picture winner
            print("Was this the Best Picture winner?", end=" ")
            bpWinnerVals = noms[0]
            bp_title = bpWinnerVals[1]
            bp_score = bpWinnerVals[2]
            bp_reviews = bpWinnerVals[3]

            if maxIndex == 0:
                print("YES")
                print("Best Picture Winner:", bp_title)
                print("High Score Nominee:", film_title)

            else:
                print("NO")
                print("Best Picture Winner:", bp_title)
                print("High Score Nominee:", film_title)
                print("   ", rt_score, "(", num_reviews, "Reviews )", ">", bp_score, "(", bp_reviews, "Reviews )")

            print("\n")

def create_csv():

    #    if row == []:
    #    else:

    film_num = 0
    i = 2
    #print(wikiSoup)
    for url in wikiSoup:
        if i > 0:
            #print(url)
            j = 0
            val = url.find_all('i')
            nums = url.select('style')
            #print(url.has_key("rowspan"))
            #film_set = [txt.get_text().strip() for txt in val]


            ## Dynamically find the number of nominations each year
            #year_noms = 0
            #url.find_all('tr')
            #if row_style == 'background:#FAEB86':
            #    year_noms = 0
            #else:
            #    year_noms++

            film_link_set = []
            for td in url.find_all('td'):
                if td.find_all('i'):
                    film_row_att = td.find_all('a')
                    film_link_set.append(film_row_att[0]['href'])
                    bp_noms.append(film_row_att[0].get_text())

             # print(film_link_set)
            for film_link in film_link_set:
                if True is True: #"film_link == '/wiki/East_Lynne_(1931_film)' or film_link == '/wiki/Casablanca_(film)' or film_link == '/wiki/Parasite_(2019_film)':
                    film_title = bp_noms[film_num].split(' ')
                    print(*film_title)
                    last_word_of_title = ''
                    if 'or' in film_title:
                        last_word_of_title = film_title[film_title.index('or') - 1].lower()
                    for word in film_title:
                        if ':' in word:
                            last_word_of_title = word.lower()
                            break
                    if last_word_of_title == '':
                        last_word_of_title = film_title[-1].lower()#.replace('*', '').replace('-', '')
                    last_word_of_title = re.sub(r'[^\w\s]', '', last_word_of_title).replace('é', 'e') # https://www.geeksforgeeks.org/python-remove-punctuation-from-string/
                    # last_word_of_title = unidecode.unidecode(last_word_of_title)
                    #bp_noms.append(film_link)
                    rt_url = ''#"https://www.rottentomatoes.com/m/" + film.lower().translate(str.maketrans('', '', string.punctuation)).replace(" ", "_")

                    article = requests.get('https://en.wikipedia.org' + film_link)
                    article_soup = BeautifulSoup(article.content, 'html.parser')
                    last_film_link = ''
                    for a in article_soup.find_all('a', href=True):
                        if a['href'].startswith('https://www.rottentomatoes.com/m') or a['href'].startswith('http://www.rottentomatoes.com/m'):
                            last_film_link = a['href']
                            print(a['href'])

                        #print(lastWordOfTitle)
                        if (a['href'].startswith('https://www.rottentomatoes.com/m') or a['href'].startswith('http://www.rottentomatoes.com/m')) and last_word_of_title in a['href']:
                            rt_url = a['href']
                            if 'https' not in rt_url:
                                rt_url = rt_url.replace('http', 'https')
                    if rt_url == '':
                        rt_url = last_film_link

                    if rt_url.endswith('/reviews'):
                        rt_url = rt_url[:len(rt_url) - 7]
                    print(rt_url)


                    if rt_url != '':
                        page = requests.get(rt_url)
                        soup = BeautifulSoup(page.content, 'html.parser')
                        #if (soup.find(id="tomato_meter_link") != None):
                        if (soup.find(id="topSection") != None):
                            #main_content = soup.find(id="tomato_meter_link")
                            score_content = soup.find(id="topSection")
                            #score_html = main_content.select(".mop-ratings-wrap__percentage")
                            score_html = score_content.find("score-board")
                            #print(rt_url)
                            rt_scores.append(score_html['tomatometerscore'])
                            print(rt_scores[-1], type(rt_scores[-1]))
                            #rt_score.append([nm.get_text().strip() for nm in score_html])
                            reviews_text = score_content.find(attrs={'data-qa': 'tomatometer-review-count'}).get_text()
                            print(reviews_text, type(reviews_text))
                            num_reviews.append(reviews_text[:len(reviews_text) - 8])
                        else:
                            rt_scores.append('??')
                            num_reviews.append('??')

                        film_num = film_num + 1
                    else:
                        raise Exception('ERROR: Rotten Tomatoes URL not found.')

            #   print(rt_score)
            #num_noms
            # print(bp_noms[0])

        # bp_noms_cat =np.concatenate([bp_noms[0],bp_noms[1]])

        # print(bp_noms)
    #  thing = []
    #  for x in rt_url:
    #      thing.append(str(x))

    # if (bp_noms[0] == "Wings"):
        print(bp_noms)
        print(rt_scores)
        i = i + 1
    #print(bp_noms)

    # bp_noms = soup.find_all(a="href")
    # bp_noms = bp_noms['title']
    # = seven_day.find_all(a="href")
    # rt_score = main_content.select(".mop-ratings-wrap__percentage")
    # names = [nm.get_text().strip() for nm in rt_score]
    # print(tonight)

    # Create dataframe for printing the Most Wanted names in an organized fashion
    # most_wanted = pd.DataFrame({
    #    "Best Pictures": rt_score
    # })
    # rt_score
    # print(bp_noms)


    year = 1928
    num_noms = []
    year_noms = 3
    pivot_years = [1929, 1932, 1933, 1934, 1936, 1944, 2009, 2011, 2014, 2016, 2018, 2019, 2020]

    while year < 2021:
        if year == 1929 or year == 1944:
            year_noms = 5
        elif year == 1932 or year == 2014 or year == 2018 or year == 2020:
            year_noms = 8
        elif year == 1933 or year == 1936 or year == 2009:
            year_noms = 10
        elif year == 1934:
            year_noms = 12
        elif year == 2011 or year == 2016 or year == 2019:
            year_noms = 9

        num_noms.append(year_noms)
        year = year + 1
    print(num_noms)

    #bp_noms.append("Filler1")
    #bp_noms.append("Filler2")
    #rt_scores.append(10)
    #rt_scores.append(10)
    #num_reviews.append(100)
    #num_reviews.append(100)
    num_nom = len(num_noms)
    print(num_nom)
    print(len(bp_noms))
    bp_scores = []
    nom_years = []
    year = 1928
    print("Num Reviews: ", num_reviews)
    n = 0
    for i in range(len(num_noms)):
        #n = 0
        year_scores = []
        #if year > 1929:
        print("Num_Noms[i]: ", num_noms[i])
        #print("BP_Noms[n]: ", bp_noms[n], end=' ')
        for nom in range(num_noms[i]):

            rt_scores[n] = 0 if rt_scores[n] == '??' or len(rt_scores[n]) == 0 else rt_scores[n]
            num_reviews[n] = 0 if num_reviews[n] == '??' or len(num_reviews[n]) == 0 else num_reviews[n]
            print("RT_SCORE: ", rt_scores[n])

            year_scores.append([year, bp_noms[n], rt_scores[n], num_reviews[n]])
            nom_years.append(year)
            #print("YEAR SCORES:", end=" ")
            #print(year_scores)
            n = n + 1
        bp_scores.insert(len(bp_scores), year_scores)
        year = year + 1
        print("  " + str(year) + "  " + str(n))
        #    bp_scores[n] = rt_scores[n]
    #[nom]['title'][nom]['score']
    print(bp_scores)
    print(nom_years)

    #bp_noms.pop()
    #bp_noms.pop()
    year = 1928
    with open('Best_Picture_Nominee_RT_Scores.csv', mode='w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file, delimiter='|')
        for row_index in range(len(bp_noms)):
            csv_writer.writerow([nom_years[row_index], bp_noms[row_index], rt_scores[row_index], num_reviews[row_index]])
            year = year + 1

create_csv()
#display()

print("")




