__author__ = 'Aubrianna'

import os.path
import sqlite3

def get_movies_by_director(director):
    # see if database exists, if so connect
    if not os.path.isfile('movies.db'):
        raise Exception('Database does not exist, please re-crawl')
    conn = sqlite3.connect('movies.db')
    c = conn.cursor()

    # find all applicable words in the director string provided by user
    director = director.lower()
    words = director.split()
    intersect_ids = None
    for word in words:
        c.execute('SELECT MOVIE_ID FROM KEYWORDS WHERE WORD =?', (word,))
        movie_ids = c.fetchone()
        if movie_ids is None:
            return []
        # get all the movie ids from the query
        ids = set(int(movie_id) for movie_id in movie_ids[0].split(','))
        # update intersection of all ids
        if intersect_ids is None:
            intersect_ids = ids
        else:
            intersect_ids.intersection_update(ids)
    results = []
    for id in intersect_ids:
        # get movie by id from movies table and add to result
        c.execute('SELECT MOVIE FROM MOVIES WHERE ID =?', (id,))
        results.append(c.fetchone()[0])

    conn.close()
    return results