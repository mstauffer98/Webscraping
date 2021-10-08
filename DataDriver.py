import csv
import re

def get_film_links():
    print("TBD")
    # film_row_att = td.find_all('a')
    # film_link_set.append(film_row_att[0]['href'])


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

        # print(lastWordOfTitle)
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
    if (soup.find(id="topSection") != None):
        # main_content = soup.find(id="tomato_meter_link")
        score_content = soup.find(id="topSection")
        # score_html = main_content.select(".mop-ratings-wrap__percentage")
        score_html = score_content.find("score-board")

        score = score_html['tomatometerscore']
        print("SCORE: ", score)
    else:
        score = '??'
    return score


def get_rt_reviews(soup):
    review_count = ''
    if (soup.find(id="topSection") != None):
        # main_content = soup.find(id="tomato_meter_link")
        score_content = soup.find(id="topSection")
        # score_html = main_content.select(".mop-ratings-wrap__percentage")
        score_html = score_content.find("score-board")
        # rt_score.append([nm.get_text().strip() for nm in score_html])
        reviews_text = score_content.find(attrs={'data-qa': 'tomatometer-review-count'}).get_text()

        review_count = reviews_text[:len(reviews_text) - 8]
        print("NUM OF REVIEWS: ", reviews_text)
    else:
        review_count = '??'
    return review_count

def write_csv(bp_noms, nom_years, rt_scores, num_reviews):
    year = 1928
    with open('Best_Picture_Nominee_RT_Scores.csv', mode='w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file, delimiter='|')
        for row_index in range(len(bp_noms)):
            csv_writer.writerow(
                [nom_years[row_index], bp_noms[row_index], rt_scores[row_index], num_reviews[row_index]])
            year = year + 1
