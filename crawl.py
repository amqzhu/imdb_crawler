__author__ = 'Aubrianna'

# import libraries
import urllib2
from bs4 import BeautifulSoup
import sqlite3

# create database
conn = sqlite3.connect('movies.db')
c = conn.cursor()
# create two tables
c.execute('''CREATE TABLE MOVIES (ID INT PRIMARY KEY NOT NULL, DIRECTOR TEXT NOT NULL, MOVIE TEXT NOT NULL)''')
c.execute('''CREATE TABLE KEYWORDS(WORD TEXT PRIMARY KEY NOT NULL, MOVIE_ID TEXT NOT NULL)''')
conn.commit()

# specify the url, 20 pages for 1000 movies
page_range = range(1, 21, 1)
page_url_start = 'http://www.imdb.com/search/title?groups=top_1000&sort=user_rating&view=simple&page='
page_url_end = '&ref_=adv_nxt'

for i in page_range:
    # get and open full url
    url_full = page_url_start+str(i)+page_url_end
    page = urllib2.urlopen(url_full)
    # parse page using BeautifulSoup
    soup = BeautifulSoup(page, 'html.parser')

    # find span classes for all the movie items on the page
    span_class = soup.find_all('span', attrs={'class': 'lister-item-header'})
    for movie_span in span_class:
        # get movie id rank and movie name
        id_var = movie_span.find('span', attrs={'class': 'lister-item-index'}).text.split('.')[0]
        movie_name = movie_span.find('a').text
        # get link to the movie and open new url, parsing the new page with BeautifulSoup
        movie_link = movie_span.find('a').get('href')
        url_sub = 'http://www.imdb.com' + movie_link
        page_sub = urllib2.urlopen(url_sub)
        soup_sub = BeautifulSoup(page_sub, 'html.parser')
        # find director information
        span_sub = soup_sub.find('span',attrs={'itemprop': 'director'})
        director_name = span_sub.find('a').text.lower()
        director_words = director_name.split()
        # Insert data into the database
        c.execute('INSERT INTO MOVIES VALUES (?,?,?)', (id_var, director_name, movie_name))
        for word in director_words:
            c.execute('SELECT MOVIE_ID FROM KEYWORDS WHERE WORD =?', (word,))
            movie_ids = c.fetchone()
            if movie_ids is not None:
                movie_ids = movie_ids[0] + ',' + id_var
                c.execute('UPDATE KEYWORDS SET MOVIE_ID =? WHERE WORD =?', (movie_ids, word))
            else:
                c.execute('INSERT INTO KEYWORDS VALUES (?,?)', (word, id_var))
        conn.commit()

conn.close()