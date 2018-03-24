__author__ = 'Aubrianna'

from api_def import get_movies_by_director

if __name__ == '__main__':
    print get_movies_by_director('francis ford coppola')
    print get_movies_by_director('coppola')
    print get_movies_by_director('francis')
    print get_movies_by_director('ford')
    print get_movies_by_director('spielberg')