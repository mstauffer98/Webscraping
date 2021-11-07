import csv
import re


def append_bp_nom_names(bp_noms, url):
    for td in url.find_all('td'):
        if td.find_all('i'):
            film_row_att = td.find_all('a')
            bp_noms.append(film_row_att[0].get_text())
    return bp_noms


def get_wiki_links(url):
    film_link_set = []
    for td in url.find_all('td'):
        if td.find_all('i'):
            film_row_att = td.find_all('a')
            film_link_set.append(film_row_att[0]['href'])
    return film_link_set


def get_last_word(film_title):
    last_word = ''
    if 'or' in film_title:
        last_word = film_title[film_title.index('or') - 1]
    for word in film_title:
        if ':' in word:
            last_word = word
            break
    if last_word == '':
        last_word = film_title[-1]

    last_word = last_word.lower()

    # https://www.geeksforgeeks.org/python-remove-punctuation-from-string/
    last_word = re.sub(r'[^\w\s]', '', last_word).replace('é', 'e')
    return last_word


def get_rt_url(article_soup, last_word_of_title):
    rt_url = ''
    last_film_link = ''
    for a in article_soup.find_all('a', href=True):
        if a['href'].startswith('https://www.rottentomatoes.com/m') or a['href'].startswith(
                'http://www.rottentomatoes.com/m'):
            last_film_link = a['href']
            print(a['href'])

        if (a['href'].startswith('https://www.rottentomatoes.com/m') or a['href'].startswith(
                'http://www.rottentomatoes.com/m')) and last_word_of_title in a['href']:
            rt_url = a['href']
            if 'https' not in rt_url:
                rt_url = rt_url.replace('http', 'https')
    if rt_url == '':
        rt_url = last_film_link

    if rt_url.endswith('/reviews'):
        rt_url = rt_url[:len(rt_url) - 7]
    print(rt_url)

    return rt_url


def get_rt_score(soup):
    score = ''
    if soup.find(id="topSection") is not None:
        score_content = soup.find(id="topSection")
        score_html = score_content.find("score-board")

        score = score_html['tomatometerscore']
        print("SCORE: ", score)
    else:
        score = '??'
    return score


def get_rt_reviews(soup):
    review_count = ''
    if soup.find(id="topSection") is not None:
        score_content = soup.find(id="topSection")
        reviews_text = score_content.find(attrs={'data-qa': 'tomatometer-review-count'}).get_text()

        review_count = reviews_text[:len(reviews_text) - 8]
        print("NUM OF REVIEWS: ", reviews_text)
    else:
        review_count = '??'
    return review_count


def get_yearly_num_noms():
    num_noms = []

    pivot_years = [1929, 1932, 1933, 1934, 1936, 1944, 2009, 2011, 2014, 2016, 2018, 2019, 2020]

    year = 1928
    year_noms = 3
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
    return num_noms


def get_nom_years(num_noms):
    year = 1928
    nom_years = []
    for i in range(len(num_noms)):
        for j in range(num_noms[i]):
            nom_years.append(year)
        year = year + 1
    return nom_years


def filter_empty_data(data):
    for n in range(len(data)):
        if len(data) < 1:
            print(len(data), n)
        data[n] = 0 if data[n] == '??' or len(data[n]) == 0 else data[n]
    return data


# GARBAGE
def get_nom_scores(bp_noms, rt_scores, num_rt_reviews, num_award_years, num_noms):
    nom_scores = []
    year = 1928
    for num_year in range(num_award_years):
        year_scores = []
        print("Num_Noms[i]: ", num_noms[num_year])
        # print("BP_Noms[n]: ", bp_noms[n], end=' ')
        for nom in range(num_noms[num_year]):
            rt_scores[n] = 0 if rt_scores[n] == '??' or len(rt_scores[n]) == 0 else rt_scores[n]
            num_rt_reviews[n] = 0 if num_rt_reviews[n] == '??' or len(num_rt_reviews[n]) == 0 else num_rt_reviews[n]
            print("RT_SCORE: ", rt_scores[n])

            # year_scores.append([year, bp_noms[n], rt_scores[n], num_rt_reviews[n]])

            n = n + 1
        nom_scores.insert(len(nom_scores), year_scores)
        year = year + 1
        print("  " + str(year) + "  " + str(n))
    return nom_scores


def write_csv(nom_years, bp_noms, rt_scores, num_reviews):
    year = 1928
    with open('Best_Picture_Nominee_RT_Scores.csv', mode='w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file, delimiter='|')
        for row_index in range(len(bp_noms)):
            csv_writer.writerow(
                [nom_years[row_index],
                 bp_noms[row_index],
                 rt_scores[row_index],
                 num_reviews[row_index]])
            year = year + 1


def import_csv_data():
    bp_scores = []
    with open('Best_Picture_Nominee_RT_Scores.csv', mode='r', newline='') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter='|')
        year = '1928'
        year_scores = []
        for row in csv_reader:
            print(row)
            if row[0] != year:
                year = row[0]
                bp_scores.insert(len(bp_scores), year_scores)
                year_scores = []

            year_scores.append([int(row[0]), row[1], int(row[2]), int(row[3])])

        bp_scores.insert(len(bp_scores), year_scores)
    return bp_scores


def find_high_score_noms(noms):
    i = 0
    scores = [noms[i][2] for i in range(0, len(noms))]
    # print("Nom Scores:", scores)
    max_score = max(scores)
    # maxScoreFilms = [i if noms[i][2] == maxScore for i in range(1, len(noms))]
    max_score_films = []
    for filmIndex in range(0, len(noms)):
        if noms[filmIndex][2] == max_score:
            max_score_films.append(filmIndex)
    return max_score_films


def display_results(noms, max_index, release_year):
    film_title = noms[max_index][1]
    rt_score = noms[max_index][2]
    num_reviews = noms[max_index][3]
    print("Highest Rated Rotten Tomatoes Best Picture Nominee for the Year", release_year, ":", film_title)
    print("     Rotten Tomatoes Score:", rt_score)
    print("     With", num_reviews, "Reviews")

    # Compare high-scoring nominee to Best Picture winner
    print("Was this the Best Picture winner?", end=" ")
    bp_winner_vals = noms[0]
    bp_title = bp_winner_vals[1]
    bp_score = bp_winner_vals[2]
    bp_reviews = bp_winner_vals[3]

    if max_index == 0:
        print("YES")
        print("Best Picture Winner:", bp_title)
        print("High Score Nominee:", film_title)
    else:
        print("NO")
        print("Best Picture Winner:", bp_title)
        print("High Score Nominee:", film_title)
        print("   ", rt_score, "(", num_reviews, "Reviews )", ">", bp_score, "(", bp_reviews, "Reviews )")

    print("\n")
